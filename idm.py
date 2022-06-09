import numpy as np
from simple_pid import PID

class IDM:
    def __init__(self, s0: float = 2.0, th_target: float = 2.0, v_max: float = 40.0,
                 a_max: float = 1.50, a_min: float = 2.50, acc_factor: float = 4.0,
                 pid_kp: float = 0.25, pid_ki: float = 0.05, pid_kd: float = 0.01):
        self.s0 = s0
        self.th_target = th_target
        self.v_max = v_max
        self.a_max = a_max
        self.a_min = a_min
        self.acc_factor = acc_factor
        self.sqrt_ab = 2 * np.sqrt(self.a_max * self.a_min)
        self.pid = PID(pid_kp, pid_ki, pid_kd)
        self.pid.output_limits = (-1, 1)
        self.pid.setpoint = 0

    def calculate_acceleration(self, delta_x: float, delta_v: float, v: float):
        alpha = (self.s0 + max(0, self.th_target * v + delta_v * v / self.sqrt_ab)) / delta_x
        a = self.a_max * (1 - (v / self.v_max) ** self.acc_factor - alpha ** 2)

        return a

    def calculate_pedal_actions(self, a_current: float, a_target: float):
        self.pid.setpoint = a_target
        pedal_action = self.pid(a_current)
        #print(pedal_action)

        return pedal_action

    def get_action(self, delta_x: float, delta_v: float, v: float, a: float):
        #print(delta_x, delta_v, v, a)
        a_target = self.calculate_acceleration(delta_x, -delta_v, v)
        pedal_action = self.calculate_pedal_actions(a, a_target)
        #print(a, a_target)
        return pedal_action

