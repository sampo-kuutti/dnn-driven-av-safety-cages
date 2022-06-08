# Author:Author: Sampo Kuutti (s.j.kuutti@surrey.ac.uk)
# Organisation: University of Surrey
#
import os
import tensorflow as tf
import sl_model
import argparse
import data_reader

BATCH_SIZE = 100
DATA_DIR = './data'
LOG_DIR = './log'
CHECKPOINT_EVERY = 1000
NUM_STEPS = int(1e5)
CKPT_FILE = 'model.ckpt'
LEARNING_RATE = 1e-2
VALIDATION_EVERY = 1000
RESTORE_FROM = None
# KEEP_PROB = 0.8


def get_arguments():
    parser = argparse.ArgumentParser(description='SL training')
    parser.add_argument(
        '--learning_rate',
        type=float,
        default=LEARNING_RATE,
        help='Initial learning rate'
    )
    parser.add_argument(
        '--max_steps',
        type=int,
        default=NUM_STEPS,
        help='Number of steps to run trainer'
    )
    parser.add_argument(
        '--batch_size',
        type=int,
        default=BATCH_SIZE,
        help='Batch size. Must divide evenly into dataset sizes.'
    )
    parser.add_argument(
        '--checkpoint_every',
        type=int,
        default=CHECKPOINT_EVERY,
        help='Number of steps before checkpoint.'
    )
    parser.add_argument(
        '--validation_every',
        type=int,
        default=VALIDATION_EVERY,
        help='Number of steps after which the model is evaluated on validation data.'
    )
    parser.add_argument(
        '--input_data_dir',
        type=str,
        default=DATA_DIR,
        help='Directory to put the input data.'
    )
    parser.add_argument(
        '--log_dir',
        type=str,
        default=LOG_DIR,
        help='Directory to put the log data.'
    )
    parser.add_argument(
        '--store_metadata',
        type=bool,
        default=False,
        help='Storing debug information for TensorBoard.'
    )
    parser.add_argument(
        '--restore_from',
        type=str,
        default=RESTORE_FROM,
        help='Checkpoint file to restore model weights from.'
    )
    return parser.parse_args()


def main():
    args = get_arguments()
    sess = tf.Session()

    model = sl_model.SupervisedModel()

    # loss function (mse)
    with tf.name_scope('loss'):
        with tf.name_scope('total'):
            loss = tf.reduce_mean(tf.losses.mean_squared_error(
                labels=model.y_, predictions=model.y))
    tf.summary.scalar('loss', loss)

    # mean absolute error
    with tf.name_scope('mean_error'):
        mean_error = tf.reduce_mean(tf.abs(tf.subtract(model.y_, model.y)))
    tf.summary.scalar('mean error', mean_error)

    # training step
    with tf.name_scope('train'):
        train_step = tf.train.GradientDescentOptimizer(args.learning_rate).minimize(loss)

    #with tf.name_scope('accuracy'):
    #    accuracy, accuracy_op = tf.metrics.accuracy(labels=tf.argmax(model.y_, 0), predictions=tf.argmax(model.y, 0))
    #tf.summary.scalar('accuracy', accuracy)

    # tensorboard summary
    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter(args.log_dir + '/train', sess.graph)
    val_writer = tf.summary.FileWriter(args.log_dir + '/val')

    with sess.as_default():
        tf.local_variables_initializer().run()
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver()

    start_step = 0

    if args.restore_from is not None:
        # restore weights
        saver.restore(sess, args.restore_from)
        print('Restored model: %s' % args.restore_from)
    #if args.store_metadata:
        # store data here

    min_loss = 1.0
    min_loss_step = 0
    reader = data_reader.DataReader()

    # run training
    for i in range(start_step, start_step + args.max_steps):
        xs, ys = reader.load_train_batch(args.batch_size)
        summary, _ = sess.run([merged, train_step], feed_dict={model.x: xs, model.y_: ys})
        train_error = loss.eval(session=sess, feed_dict={model.x: xs, model.y_: ys})

        if i % 100 == 0:  #print training loss every 100 steps
            print("Step %d, train loss %g" % (i, train_error))

        # check validation error every 1000 steps
        if i % 1000 == 0:
            xs, ys = reader.load_val_batch(1000)
            val_error = loss.eval(session=sess, feed_dict={model.x: xs, model.y_: ys})
            summary_val = sess.run(merged, feed_dict={model.x: xs, model.y_: ys})

            val_writer.add_summary(summary_val, i)
            val_writer.flush()

            print("Step %d, val loss %g" % (i, val_error))

            # save checkpoint
            if i > 10 and i % args.checkpoint_every == 0:
                if not os.path.exists(args.log_dir):
                    os.makedirs(args.log_dir)
                    checkpoint_path = os.path.join(args.log_dir, "model-step-%d-val-%g.ckpt" % (i, val_error))
                    filename = saver.save(sess, checkpoint_path)
                    print("Model saved in file: %s" % filename)
                elif val_error < min_loss:
                    min_loss = val_error
                    min_loss_step = i
                    if not os.path.exists(args.log_dir):
                        os.makedirs(args.log_dir)
                    checkpoint_path = os.path.join(args.log_dir, "model-step-%d-val-%g.ckpt" % (i, val_error))
                    filename = saver.save(sess, checkpoint_path)
                    print("Model saved in file: %s" % filename)

        # Log Tensorboard data every 100 steps
        if i % 100 == 0:
            # Update the events file.
            train_writer.add_summary(summary, i)
            train_writer.flush()


    print('Minimum validation loss %g at step %d' % (min_loss, min_loss_step))


if __name__ == '__main__':
    main()
