import traffic
import matplotlib.pyplot as plt

for i in range(1, 13):
    # generate lead vehicle states
    T_lead, X_lead, V_lead, A_lead = traffic.lead_vehicle(scenario_num=i)

    # plot lead vehicle velocity
    plt.plot(T_lead, V_lead)
    plt.ylim([0, 45])
    plt.xlabel('time [s]')
    plt.ylabel('lead vehicle velocity [m/s]')
    plt.title('Vehicle Following Scenario %d' % i)
    plt.show()