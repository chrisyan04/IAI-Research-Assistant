import pandas as pd
data = 'merged-w22-csc148.csv'
weeks = ['w1_opened', 'w2_opened', 'w3_opened', 'w4_opened',
         'w5_opened', 'w6_opened', 'w7_opened', 'w8_opened',
         'w9_opened', 'w10_opened', 'w11_opened']
         
d_email = pd.read_csv(data, usecols=weeks).values
d_treatment = pd.read_csv(data, usecols=['w1_text_A']).values
d_gender = pd.read_csv(data, usecols=['Q769_pre']).values

f_gender = 'she/herShe/HerwomanfemaleFemaleWoman'
m_gender = 'HeterosexualMalemalehe/himManmanHe/Himcis-gender'
treatment_obs = []
control_obs = []
total_obs = []
for i in range(len(d_treatment)):
    if not pd.isna(d_treatment[i][0]):
        treatment_obs.append(i)
    else:
        control_obs.append(i)
    total_obs.append(i)

def determine_rate(obs):
    rates = []
    totals = []
    opens = []
    m_opens = []
    f_opens = []
    other_opens = []
    for i in range(len(weeks)):
        tot = 0
        op = 0
        m = 0
        f = 0
        other = 0
        for j in obs:
            if not pd.isna(d_email[j][i]):
                tot += 1
                if d_email[j][i] == 'EMAIL_OPENED':
                    op += 1
                if not pd.isna(d_gender[j][0]):
                    if d_gender[j][0] in m_gender:
                        m += 1
                    elif d_gender[j][0] in f_gender:
                        f += 1
                    else:
                        other += 1
                else:
                    other += 1
        totals.append(tot)
        opens.append(op)
        m_opens.append(m)
        f_opens.append(f)
        other_opens.append(other)
        if tot != 0:
            rates.append(op / tot)
        else:
            rates.append(0)
    return [rates, opens, totals, m_opens, f_opens, other_opens]

results = pd.DataFrame(columns=weeks)

results_overall = determine_rate(total_obs)
results_treatment = determine_rate(treatment_obs)
results_control = determine_rate(control_obs)

for i in range(1, 7):
    results.loc[i] = results_overall[i - 1]
for i in range(7, 13):
    results.loc[i] = results_treatment[i - 7]
for i in range(13, 19):
    results.loc[i] = results_control[i - 13]

# print(results)

import numpy as np
import matplotlib.pyplot as plt

labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6',
          'Treatment 1', 'Treatment 2', 'Treatment 3',
          'Control 1', 'Control 2', 'Control 3']

overall_rates = results.loc[1:6, weeks].values
treatment_rates = results.loc[7:12, weeks].values
control_rates = results.loc[13:18, weeks].values

m_opens = results.loc[1:6, 3].values
f_opens = results.loc[1:6, 4].values
other_opens = results.loc[1:6, 5].values

totals = np.vstack((m_opens, f_opens, other_opens)).T
cumulative_totals = np.cumsum(totals, axis=1)
