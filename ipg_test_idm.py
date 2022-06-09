# =====================================================================================================================
# Author: Sampo Kuutti (s.j.kuutti@surrey.ac.uk)
# Organisation: University of Surrey

# much ipg testing. much wow. this time with a imd-pid model.
# =====================================================================================================================

import os
import tensorflow as tf
import sl_model
import argparse
import ctypes
import pythonapi
import safety_val
import csv
import time
import traffic
import random
import idm
import json

SAFETY_ON = 0  # 0 = no safety cages, 1 = safety cages on

DATA_DIR = './data/'
LOG_DIR = './ipg_idm_pid_testing_9/'


def get_arguments():
    parser = argparse.ArgumentParser(description='SL testing')
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
        help='Directory to log the result data.'
    )
    parser.add_argument(
        '--idm_s0',
        type=float,
        default=2.0
    )
    parser.add_argument(
        '--idm_th',
        type=float,
        default=2.0
    )
    parser.add_argument(
        '--idm_vmax',
        type=float,
        default=40.0
    )
    parser.add_argument(
        '--idm_amax',
        type=float,
        default=1.5
    )
    parser.add_argument(
        '--idm_amin',
        type=float,
        default=2.5
    )
    parser.add_argument(
        '--idm_accfactor',
        type=float,
        default=4.0
    )
    parser.add_argument(
        '--pid_kp',
        type=float,
        default=0.25
    )
    parser.add_argument(
        '--pid_ki',
        type=float,
        default=0.010
    )
    parser.add_argument(
        '--pid_kd',
        type=float,
        default=0.0
    )
    return parser.parse_args()


def main():
    # set up tf session and model
    args = get_arguments()
    # write results to file
    if not os.path.exists(args.log_dir):
        os.makedirs(args.log_dir)
    with open(args.log_dir + 'args.json', 'w') as f:
        json.dump(args.__dict__, f, indent=2)



    # initial threshold
    threshold = 0.86
    arr_scen = []

    for i in range(96, 121):
        # initialise idm model
        model = idm.IDM(s0=args.idm_s0, th_target=args.idm_th, v_max=args.idm_vmax,
                        a_max=args.idm_amax, a_min=args.idm_amin, acc_factor=args.idm_accfactor,
                        pid_kp=args.pid_kp, pid_ki=args.pid_ki, pid_kd=args.pid_kd)

        # set up connection to carmaker
        pythonapi.api_setup()

        # empty arrays
        A = []  # acceleration array
        J = []  # jerk array
        T = []  # time array
        X = []  # x_rel array
        V = []  # velocity array
        DV = [] # relative velocity array
        T_h = [] # time headway array
        Y_0 = []    # original output
        Y_SC = []   # safety cage output
        SC = []     # safety cage number

        V_leader = []   # lead vehicle velocity
        A_leader = []   # lead vehicle acceleration

        print('test no. %d' % i)
        # load test run
        #scen = random.randint(1,25)
        #arr_scen.append(scen)
        with open('./traffic_data/' + 'scens.csv') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                arr_scen.append(float(row['s']))  # test run id
        scen = int(arr_scen[i - 1])
        pythonapi.sim_loadrun2(scen)

        # subscribe quantities
        pythonapi.subscribe_quants()

        # while simulation is running feed states to nn and use outputs
        # set variables to 0
        b = 0
        v_rel = 0
        v = 0
        x_rel = 0
        a = 0
        t = 0

        # lead vehicle states
        #T_lead, X_lead, V_lead, A_lead = traffic.lead_vehicle()
        T_lead = []
        X_lead = []
        V_lead = []
        A_lead = []
        with open('./traffic_data/' + str(i) + '.csv') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                T_lead.append(float(row['t']))      # time
                X_lead.append(float(row['x']))      # long. position
                V_lead.append(float(row['v']))      # velocity
                A_lead.append(float(row['a']))      # acceleration

        # initialise pedals at 0
        pythonapi.set_gas(ctypes.c_double(0))
        pythonapi.set_brake(ctypes.c_double(0))

        # start simulation
        pythonapi.sim_start()
        pythonapi.sim_waitready()

        while pythonapi.sim_isrunning() != 0:       # check if simulation is running
            pythonapi.ApoClnt_PollAndSleep()        # poll client
            t = pythonapi.get_time()
            if t > 0:

                b += 1

                # read host states
                v = pythonapi.get_hostvel()         # host velocity
                a = pythonapi.get_longacc()         # host longitudinal acceleration
                x = pythonapi.get_hostpos()         # host longitudinal position

                # lead vehicle states
                t_iter = int(t // 0.02)             # current time step
                v_rel = V_lead[t_iter] - v          # relative velocity
                x_rel = X_lead[t_iter] - x          # relative distance

                # enter variables into arrays
                A.append(a)
                T.append(t)
                X.append(x_rel)
                V.append(v)
                DV.append(v_rel)

                V_leader.append(V_lead[t_iter])
                A_leader.append(A_lead[t_iter])

                # calculate time headway
                if v != 0:
                    t_h = x_rel / v
                else:
                    t_h = x_rel

                T_h.append(t_h)

                # stop simulation if a crash occurs
                if x_rel <= 0:
                    pythonapi.sim_stop()
                    print('crash occurred: simulation run stopped')

                # define inputs to neural network
                inputs = [v_rel, t_h, v]

                # evaluate neural network output
                y = model.get_action(x_rel, v_rel, v, a)

                # safety cage implementation
                if SAFETY_ON == 1:      # check if safety cages are enabled
                    sc, output = safety_val.safety_cage2(t, v_rel, t_h, v, x_rel, a, y, threshold)
                else:
                    output = y
                    sc = 0

                # clip outputs to [-1, 1]
                if output > 1:
                    output = 1
                elif output < -1:
                   output = -1

                Y_SC.append(float(output))
                Y_0.append(float(output))
                SC.append(sc)

                # convert normalised output to gas and brake signals
                if output < 0:          # output brake command
                    gas = 0
                    brake = abs(output)
                elif output > 0:        # output gas command
                    gas = output
                    brake = 0
                elif output == 0:       # both outputs are zero
                    gas = 0
                    brake = 0
                else:   # something has gone wrong
                    gas = 0
                    brake = 0
                    print('invalid control signal, setting pedal values to 0')

                #  send commands to carmaker
                pythonapi.set_gas(ctypes.c_double(gas))
                pythonapi.set_brake(ctypes.c_double(brake))

                # stop simulation if a crash occurs
                if x_rel <= 0:
                    pythonapi.sim_stop()
                    print('crash occurred: simulation run stopped')

        # calculate jerk array
        for k in range(0, 5):
            J.append(float(0))

        for k in range(5, len(T)):
            # calculate vehicle jerk
            if abs(T[k] - T[k-5]) != 0:
                J.append(((A[k]) - (A[k-5])) / (T[k] - T[k-5]))  # jerk
            else:
                J.append(0)


        headers = ['t', 'j', 'v', 'a', 'v_lead', 'a_lead', 'x_rel', 'v_rel', 'th', 'y_0', 'y_sc', 'sc']
        with open(args.log_dir + str(i) + '.csv', 'w', newline='\n') as f:
            wr = csv.writer(f, delimiter=',')
            rows = zip(T, J, V, A, V_leader, A_leader, X, DV, T_h, Y_0, Y_SC, SC)
            #for pls in range(len(Y_0)):
            #    print(pls)
            #    print(len(list(rows)[pls]))
            wr.writerow(headers)
            wr.writerows(rows)
            for l in range(len(T)):
                wr.writerow([T[l], J[l], V[l], A[l], V_leader[l], A_leader[l],
                             X[l], DV[l], T_h[l], Y_0[l], Y_SC[l], SC[l]])
                #print(len(row))

        # terminate api connection
        pythonapi.api_terminate()
        time.sleep(1)

    # print test stuff
    print('simulation run complete')

    # write scenarios used to file
    print('scenarios used:')
    print(arr_scen)
    #with open('./traffic_data/' + 'scens.csv', 'w', newline='\n') as f:
    #    wr = csv.writer(f, delimiter=',')
    #    rows = zip(arr_scen)
    #    wr.writerow('s')
    #    wr.writerows(rows)



if __name__ == '__main__':
    main()
