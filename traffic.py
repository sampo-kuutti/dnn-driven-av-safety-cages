import math
import random
t_step = 0.02   # time step 20ms


def generate_velocity(t, v_init, rand):

    # case 1: periodical accelerations
    if rand[0] == 1:
        if t <= rand[1]:    # start at v_init
            v_new = v_init

        # maneuver 1
        elif t > rand[1] and t <= (rand[1] + rand[3]/rand[2]):    # start accelerating towards (v_init + rand[3])
            v_new = v_init + rand[2]*(t-rand[1])
        elif t > (rand[1] + rand[3]/rand[2]) and t <= (rand[1] + rand[3]/rand[2] + rand[14]):    # constant vel.
            v_new = v_init + rand[3]
        elif t > (rand[1] + rand[3]/rand[2] + rand[14]) \
                and t <= (rand[1] + 2*(rand[3]/rand[2]) + rand[14]):    # start decelerating
            v_new = v_init + rand[3] - rand[2]*(t - (rand[1] + rand[3]/rand[2] + rand[14]))
        elif t > (rand[1] + 2*(rand[3]/rand[2]) + rand[14]) and t <= rand[4]:     # stay at v_init
            v_new = v_init

        # maneuver 2
        elif t > rand[4] and t <= (rand[4] + rand[6]/rand[5]):    # start accelerating towards (v_init + rand[6])
            v_new = v_init + rand[5]*(t-rand[4])
        elif t > (rand[4] + rand[6]/rand[5]) and t <= (rand[4] + rand[6]/rand[5] + rand[14]):    # constant vel.
            v_new = v_init + rand[6]
        elif t > (rand[4] + rand[6]/rand[5] + rand[14]) \
                and t <= (rand[4] + 2*(rand[6]/rand[5]) + rand[14]):    # start decelerating
            v_new = v_init + rand[6] - rand[5]*(t - (rand[4] + rand[6]/rand[5] + rand[14]))

        # maneuver 3
        elif t > rand[7] and t <= (rand[7] + rand[9] / rand[8]):  # start accelerating towards (v_init + rand[9])
            v_new = v_init + rand[8] * (t - rand[7])
        elif t > (rand[7] + rand[9] / rand[8]) and t <= (rand[7] + rand[9] / rand[8] + rand[14]):  # constant vel.
            v_new = v_init + rand[9]
        elif t > (rand[7] + rand[9] / rand[8] + rand[14]) \
                and t <= (rand[7] + 2*(rand[9]/rand[8]) + rand[14]):  # start decelerating
            v_new = v_init + rand[9] - rand[8] * (t - (rand[7] + rand[9] / rand[8] + rand[14]))
        else:  # just in case
            v_new = v_init

    # case 2: periodical decelerations
    elif rand[0] == 2:
        if t <= rand[1]:  # start at v_init
            v_new = v_init

        # maneuver 1
        elif t > rand[1] and t <= (rand[1] + rand[3] / rand[2]):  # start decelerating towards (v_init - rand[3])
            v_new = v_init - rand[2] * (t - rand[1])
        elif t > (rand[1] + rand[3] / rand[2]) and t <= (rand[1] + rand[3] / rand[2] + rand[14]):  # constant vel.
            v_new = v_init - rand[3]
        elif t > (rand[1] + rand[3] / rand[2] + rand[14]) and t <= (
                rand[1] + 2 * (rand[3] / rand[2]) + rand[14]):  # start accelerating
            v_new = v_init - rand[3] + rand[2] * (t - (rand[1] + rand[3] / rand[2] + rand[14]))
        elif t > (rand[1] + 2 * (rand[3] / rand[2]) + rand[14]) and t <= rand[4]:  # stay at v_init
            v_new = v_init

        # maneuver 2
        elif t > rand[4] and t <= (rand[4] + rand[6] / rand[5]):  # start decelerating towards (v_init - rand[6])
            v_new = v_init - rand[5] * (t - rand[4])
        elif t > (rand[4] + rand[6] / rand[5]) and t <= (rand[4] + rand[6] / rand[5] + rand[14]):  # constant vel.
            v_new = v_init - rand[6]
        elif t > (rand[4] + rand[6] / rand[5] + rand[14]) and t <= (
                rand[4] + 2 * (rand[6] / rand[5]) + rand[14]):  # start accelerating
            v_new = v_init - rand[6] + rand[5] * (t - (rand[4] + rand[6] / rand[5] + rand[14]))

        # maneuver 3
        elif t > rand[7] and t <= (rand[7] + rand[9] / rand[8]):  # start decelerating towards (v_init - rand[9])
            v_new = v_init - rand[8] * (t - rand[7])
        elif t > (rand[7] + rand[9] / rand[8]) and t <= (rand[7] + rand[9] / rand[8] + rand[14]):  # constant vel.
            v_new = v_init - rand[9]
        elif t > (rand[7] + rand[9] / rand[8] + rand[14]) and t <= (
                rand[7] + 2 * (rand[9] / rand[8]) + rand[14]):  # start accelerating
            v_new = v_init - rand[9] + rand[8] * (t - (rand[7] + rand[9] / rand[8] + rand[14]))
        else:  # just in case
            v_new = v_init

    # case 3: periodical accelerations & accelerations
    elif rand[0] == 3:
        if t <= rand[1]:  # start at v_init
            v_new = v_init

        # maneuver 1
        elif t > rand[1] and t <= (rand[1] + rand[3] / rand[2]):  # start decelerating towards (v_init - rand[3])
            v_new = v_init - rand[2] * (t - rand[1])
        elif t > (rand[1] + rand[3] / rand[2]) and t <= (rand[1] + rand[3] / rand[2] + rand[14]):  # constant vel.
            v_new = v_init - rand[3]
        elif t > (rand[1] + rand[3] / rand[2] + rand[14]) and t <= (
                rand[1] + 2 * (rand[3] / rand[2]) + rand[14]):  # start accelerating
            v_new = v_init - rand[3] + rand[2] * (t - (rand[1] + rand[3] / rand[2] + rand[14]))
        elif t > (rand[1] + 2 * (rand[3] / rand[2]) + rand[14]) and t <= rand[4]:  # stay at v_init
            v_new = v_init

        # maneuver 2
        elif t > rand[4] and t <= (rand[4] + rand[6] / rand[5]):  # start accelerating towards (v_init + rand[6])
            v_new = v_init + rand[5] * (t - rand[4])
        elif t > (rand[4] + rand[6] / rand[5]) and t <= (rand[4] + rand[6] / rand[5] + rand[14]):  # constant vel.
            v_new = v_init + rand[6]
        elif t > (rand[4] + rand[6] / rand[5] + rand[14]) and t <= (
                rand[4] + 2 * (rand[6] / rand[5]) + rand[14]):  # start decelerating
            v_new = v_init + rand[6] - rand[5] * (t - (rand[4] + rand[6] / rand[5] + rand[14]))

        # maneuver 3
        elif t > rand[7] and t <= (rand[7] + rand[9] / rand[8]):  # start decelerating towards (v_init - rand[9])
            v_new = v_init - rand[8] * (t - rand[7])
        elif t > (rand[7] + rand[9] / rand[8]) and t <= (rand[7] + rand[9] / rand[8] + rand[14]):  # constant vel.
            v_new = v_init - rand[9]
        elif t > (rand[7] + rand[9] / rand[8] + rand[14]) and t <= (
                rand[7] + 2 * (rand[9] / rand[8]) + rand[14]):  # start accelerating
            v_new = v_init - rand[9] + rand[8] * (t - (rand[7] + rand[9] / rand[8] + rand[14]))
        else:  # just in case
            v_new = v_init

    # case 4: sin wave
    elif rand[0] == 4:
        v_new = v_init + math.sin((1 / rand[10]) * t) + 0.05 * math.sin(random.randint(0,315) / 100)

    # case 5: two superimposed sine waves
    elif rand[0] == 5:
        v_new = v_init + math.sin((1 / rand[10]) * t) + 0.5 * math.sin((1 / rand[11]) * t)

    # case 6: three superimposed sine waves
    elif rand[0] == 6:
        v_new = v_init + math.sin((1 / rand[10]) * t) + 0.5 * math.sin((1 / rand[11]) * t) + \
                0.25 * math.sin((1 / rand[15]) * t)

    # case 7: periodical accelerations with superimposed sine wave
    elif rand[0] == 7:
        if t <= rand[1]:    # start at v_init
            v_new = v_init + 0.2 * math.sin((1 / rand[10]) * t)

        # maneuver 1
        elif t > rand[1] and t <= (rand[1] + rand[3]/rand[2]):    # start accelerating towards (v_init + rand[3])
            v_new = v_init + rand[2]*(t-rand[1]) + 0.2 * math.sin((1 / rand[10]) * t)
        elif t > (rand[1] + rand[3]/rand[2]) and t <= (rand[1] + rand[3]/rand[2] + rand[14]):    # constant vel.
            v_new = v_init + rand[3] + 0.2 * math.sin((1 / rand[10]) * t)
        elif t > (rand[1] + rand[3]/rand[2] + rand[14]) \
                and t <= (rand[1] + 2*(rand[3]/rand[2]) + rand[14]):    # start decelerating
            v_new = v_init + rand[3] - rand[2]*(t - (rand[1] + rand[3]/rand[2] + rand[14])) \
                    + 0.2 * math.sin((1 / rand[10]) * t)
        elif t > (rand[1] + 2*(rand[3]/rand[2]) + rand[14]) and t <= rand[4]:     # stay at v_init
            v_new = v_init + 0.2 * math.sin((1 / rand[10]) * t)

        # maneuver 2
        elif t > rand[4] and t <= (rand[4] + rand[6]/rand[5]):    # start accelerating towards (v_init + rand[6])
            v_new = v_init + rand[5]*(t-rand[4]) + 0.2 * math.sin((1 / rand[10]) * t)
        elif t > (rand[4] + rand[6]/rand[5]) and t <= (rand[4] + rand[6]/rand[5] + rand[14]):    # constant vel.
            v_new = v_init + rand[6] + 0.2 * math.sin((1 / rand[10]) * t)
        elif t > (rand[4] + rand[6]/rand[5] + rand[14]) \
                and t <= (rand[4] + 2*(rand[6]/rand[5]) + rand[14]):    # start decelerating
            v_new = v_init + rand[6] - rand[5]*(t - (rand[4] + rand[6]/rand[5] + rand[14])) \
                    + 0.2 * math.sin((1 / rand[10]) * t)

        # maneuver 3
        elif t > rand[7] and t <= (rand[7] + rand[9] / rand[8]):  # start accelerating towards (v_init + rand[9])
            v_new = v_init + rand[8] * (t - rand[7]) + 0.2 * math.sin((1 / rand[10]) * t)
        elif t > (rand[7] + rand[9] / rand[8]) and t <= (rand[7] + rand[9] / rand[8] + rand[14]):  # constant vel.
            v_new = v_init + rand[9] + 0.2 * math.sin((1 / rand[10]) * t)
        elif t > (rand[7] + rand[9] / rand[8] + rand[14]) \
                and t <= (rand[7] + 2*(rand[9]/rand[8]) + rand[14]):  # start decelerating
            v_new = v_init + rand[9] - rand[8] * (t - (rand[7] + rand[9] / rand[8] + rand[14])) \
                    + 0.2 * math.sin((1 / rand[10]) * t)
        else:  # just in case
            v_new = v_init + 0.2 * math.sin((1 / rand[10]) * t)

    # case 8: velocity change to a lower velocity
    elif rand[0] == 8:
        if t <= rand[4]:
            v_new = v_init
        elif t > rand[4] and t <= (rand[4] + rand[6] / rand[5]):  # start decelerating towards (v_init - rand[6])
            v_new = v_init - rand[5] * (t - rand[4])
        elif t > (rand[4] + rand[6] / rand[5]):  # constant vel.
            v_new = v_init - rand[6]
        else:
            v_new = v_init

    # case 9: velocity change to a lower velocity with superimposed sine
    elif rand[0] == 9:
        if t <= rand[4]:
            v_new = v_init + 0.2 * math.sin((1 / rand[10]) * t)
        elif t > rand[4] and t <= (rand[4] + rand[6] / rand[5]):  # start decelerating towards (v_init - rand[6])
            v_new = v_init - rand[5] * (t - rand[4]) + 0.2 * math.sin((1 / rand[10]) * t)
        elif t > (rand[4] + rand[6] / rand[5]):  # constant vel.
            v_new = v_init - rand[6] + 0.2 * math.sin((1 / rand[10]) * t)
        else:
            v_new = v_init

    # case 10: velocity change to a higher velocity
    elif rand[0] == 10:
        if t <= rand[4]:
            v_new = v_init
        elif t > rand[4] and t <= (rand[4] + rand[6] / rand[5]):  # start decelerating towards (v_init - rand[6])
            v_new = v_init + rand[5] * (t - rand[4])
        elif t > (rand[4] + rand[6] / rand[5]):  # constant vel.
            v_new = v_init + rand[6]
        else:
            v_new = v_init

    # case 11: velocity change to a higher velocity with superimposed sine
    elif rand[0] == 11:
        if t <= rand[4]:
            v_new = v_init + 0.2 * math.sin((1 / rand[10]) * t)
        elif t > rand[4] and t <= (rand[4] + rand[6] / rand[5]):  # start decelerating towards (v_init - rand[6])
            v_new = v_init + rand[5] * (t - rand[4]) + 0.2 * math.sin((1 / rand[10]) * t)
        elif t > (rand[4] + rand[6] / rand[5]):  # constant vel.
            v_new = v_init + rand[6] + 0.2 * math.sin((1 / rand[10]) * t)
        else:
            v_new = v_init

    # case 12: emergency brake
    elif rand[0] == 12:

        if t <= rand[7]:        # start at v_init
            v_new = v_init

        elif t > rand[7] and t <= (rand[7] + rand[13] / rand[12]):         # start deceleration
            v_new = v_init - rand[12] * (t - rand[7])
        elif t > (rand[7] + rand[13] / rand[12]) and t <= (rand[7] + rand[13] / rand[12] + 20):  # constant vel. for 20s
            v_new = v_init - rand[13]
        elif t > (rand[7] + rand[13] / rand[12] + 20) and t <= (
                rand[7] + rand[13] / rand[12] + rand[13]/rand[2] + 20):  # start accelerating
            v_new = v_init - rand[13] + rand[2] * (t - (rand[7] + rand[13] / rand[12] + 20))
        else:  # just in case
            v_new = v_init

    else:
        v_new = v_init

    return v_new


def lead_vehicle(scenario_num=None):
    # lead vehicle state arrays
    T_lead = []     # time
    V_lead = []     # lead velocity
    A_lead = []     # lead acceleration
    X_lead = []     # lead long. position

    rand = []       # random array

    # fill arrays

    # time
    t_lead = 0
    while t_lead <= 300:
        T_lead.append(t_lead)
        t_lead = round(t_lead + t_step, 2)

    i = 1   # iteration variable

    # random numbers
    if scenario_num is None:
        rand.append(random.randint(1, 12))          # rand[0]: random seed for lead vehicle maneuver
    else:
        rand.append(scenario_num)

    rand.append(30 + random.randint(0, 20))     # rand[1]: maneuver 1 - start acceleration maneuver after 30-50s
    rand.append(random.randint(1, 4)/2)         # rand[2]: maneuver 1 - acceleration of 0.5-2 m/s^2
    rand.append(random.randint(20, 80)/10)      # rand[3]: maneuver 1 - total velocity change
    rand.append(100 + random.randint(0, 20))    # rand[4]: maneuver 2 - start acceleration maneuver after 100-120s
    rand.append(random.randint(1, 4)/2)         # rand[5]: maneuver 2 - acceleration of 0.5-2 m/s^2
    rand.append(random.randint(20, 80)/10)      # rand[6]: maneuver 2 - total velocity change
    rand.append(200 + random.randint(0, 20))    # rand[7]: maneuver 3 - start acceleration maneuver after 200-220s
    rand.append(random.randint(1, 4)/2)         # rand[8]: maneuver 3 - acceleration of 0.5-2 m/s^2
    rand.append(random.randint(20, 80)/10)      # rand[9]: maneuver 3 - total velocity change
    rand.append(random.randint(5, 10))          # rand[10]: frequency for sine wave 1
    rand.append(random.randint(10, 30))         # rand[11]: frequency for sine wave 2
    rand.append(random.randint(3, 6))           # rand[12]: emergency braking deceleration rate
    rand.append(random.randint(8, 18))          # rand[13]: emergency braking total velocity change
    rand.append(random.randint(0, 10))          # rand[14]: time spent at constant vel. for various maneuvers
    rand.append(random.randint(20, 40))         # rand[15]: frequency for sine wave 3
    rand.append(24 + random.randint(1,8))       # rand[16]: initial velocity

    print(rand)

    # initial states
    v_init = rand[16]  # generate random initial velocity between 25 and 32 m/s
    V_lead.append(v_init)
    X_lead.append(50)
    A_lead.append(0)

    # calculate all states
    for i in range(1, len(T_lead)):
        V_lead.append(generate_velocity(T_lead[i], v_init, rand))
        X_lead.append( (V_lead[i] * t_step) + X_lead[i-1] )
        A_lead.append( (V_lead[i]-V_lead[i-1]) / (T_lead[i]-T_lead[i-1]) )
    return T_lead, X_lead, V_lead, A_lead

def urban_driving_cycle(xrel_init):
    # lead vehicle state arrays
    T_lead = []  # time
    V_lead = []  # lead velocity
    A_lead = []  # lead acceleration
    X_lead = []  # lead long. position

    # fill arrays

    # time
    t = 0
    while t <= 780:
        T_lead.append(t)
        t = round(t + t_step, 2)

    # generate lead vehicle velocities
    V_lead.append(0)
    X_lead.append(xrel_init)
    A_lead.append(0)
    i = 1
    while t <= 0:
        V_lead.append(0)
        X_lead.append((V_lead[i] * t_step) + X_lead[i - 1])
        if (T_lead[i] - T_lead[i - 1]) != 0:
            A_lead.append((V_lead[i] - V_lead[i - 1]) / (T_lead[i] - T_lead[i - 1]))
        else:
            A_lead.append(0)
        i += 1




