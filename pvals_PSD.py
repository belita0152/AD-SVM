import pandas as pd
import numpy as np

file = pd.read_excel("spss_eeg.xlsx", sheet_name='ANOVA_PSD')
raw = file[['ANOVA', 'Unnamed: 5', 'Unnamed: 6']].dropna(axis=0)  # name, F-val, p-val + NaN 제거

# names = raw['ANOVA'].str.split('.')

raw[['Frequency band', 'Channel']] = raw['ANOVA'].str.split('.', expand=True)
raw = raw.rename(columns={'Unnamed: 5': 'F', 'Unnamed: 6': 'p-val'})
data = raw[['Frequency band', 'Channel', 'F', 'p-val']]

data.to_excel("anova_pvals.xlsx", index=False)

##############################################################

import pandas as pd
import numpy as np

file = pd.read_excel("spss_eeg.xlsx", sheet_name='Scheffe_PSD')
raw = pd.DataFrame(file[["다중비교", 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 5']])


raw_delta = raw.iloc[3:117]['Unnamed: 5'].reset_index(drop=True)  # 0~113
raw_theta = raw.iloc[122:236]['Unnamed: 5'].reset_index(drop=True)
raw_alpha = raw.iloc[241:355]['Unnamed: 5'].reset_index(drop=True)
raw_beta = raw.iloc[361:475]['Unnamed: 5'].reset_index(drop=True)
raw_gamma = raw.iloc[481:595]['Unnamed: 5'].reset_index(drop=True)


# Preproc
def pval(data, num_groups):
    result = []

    for num in range(num_groups):
        ad_cn = data[num * 6]
        ad_ftd = data[num * 6 + 1]
        ftd_cn = data[num * 6 + 3]
        cell = [ad_cn, ad_ftd, ftd_cn]

        result.append(cell)

    return result

col_names = ['AD_CN', 'AD_FTD', 'CN_FTD']
row_names = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T3', 'T4', 'T5', 'T6', 'Fz',
            'Cz', 'Pz']
bands = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']

delta_values = np.array(pval(raw_delta, 19)).reshape(19, 3)
theta_values = np.array(pval(raw_theta, 19)).reshape(19, 3)
alpha_values = np.array(pval(raw_alpha, 19)).reshape(19, 3)
beta_values = np.array(pval(raw_beta, 19)).reshape(19, 3)
gamma_values = np.array(pval(raw_gamma, 19)).reshape(19, 3)

values = np.concatenate((delta_values, theta_values, alpha_values, beta_values, gamma_values))
# print(values.shape)  # (95, 3) = (19, 3) * 5 bands
pd.DataFrame(values).to_excel("psds.xlsx")
