import traffic
import csv

for i in range(1, 126):
    # generate lead vehicle states
    T_lead, X_lead, V_lead, A_lead = traffic.lead_vehicle()

    # write lead vehicle profile to file
    with open('./traffic_data/' + str(i) + '.csv', 'w', newline='\n') as f:
        wr = csv.writer(f, delimiter=',')
        rows = zip(T_lead, X_lead, V_lead, A_lead)
        wr.writerow(['t', 'x', 'v', 'a'])
        wr.writerows(rows)