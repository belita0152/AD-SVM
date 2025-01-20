import pandas as pd
import numpy as np

file = pd.read_excel("spss_eeg.xlsx", sheet_name='ANOVA_FC')
raw = file[['ANOVA', 'Unnamed: 5', 'Unnamed: 6']].dropna(axis=0)  # name, F-val, p-val + NaN 제거
# print(raw)
names = raw['ANOVA'].str.split('.')
ch_names = names.apply(lambda x: f"{x[0]}-{x[1]}")
band_names = names.apply(lambda x: x[2])
raw[['Channel', 'Frequency band']] = pd.DataFrame({
    'Channel': ch_names,
    'Frequency band': band_names
    })

raw = raw.rename(columns={'Unnamed: 5': 'F', 'Unnamed: 6': 'p-val'})
data = raw[['Channel', 'Frequency band', 'F', 'p-val']]

p_value = data[data['Frequency band'] == 'gamma']['p-val'].values
n=18
upper_triangular_matrix = np.zeros((n, n))
upper_triangular_matrix[np.triu_indices(n)] = p_value[:n * (n + 1) // 2]
pd.DataFrame(upper_triangular_matrix).to_excel("upper_triangular_matrix.xlsx", index=False)



f_value = data[data['Frequency band'] == 'gamma']['F'].values
lower_triangular_matrix = np.zeros((n, n))
lower_triangular_matrix[np.tril_indices(n)] = f_value[:n * (n + 1) // 2]
print(lower_triangular_matrix)

pd.DataFrame(lower_triangular_matrix).to_excel("lower_triangular_matrix.xlsx", index=False)


# raw[['Frequency band', 'Channel']] = raw['ANOVA'].str.split('.', expand=True)
# raw = raw.rename(columns={'Unnamed: 5': 'F', 'Unnamed: 6': 'p-val'})
# data = raw[['Frequency band', 'Channel', 'F', 'p-val']]

# data.to_excel("anova_pvals.xlsx", index=False)


#######################################################################

import pandas as pd
import numpy as np

file = pd.read_excel("spss_eeg.xlsx", sheet_name='Scheffe_FC')
raw = pd.DataFrame(file[["다중비교", 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 5']])

raw_delta = raw.iloc[3:1033]['Unnamed: 5'].reset_index(drop=True)
raw_theta = raw.iloc[1038:2068]['Unnamed: 5'].reset_index(drop=True)
raw_alpha = raw.iloc[2073:3103]['Unnamed: 5'].reset_index(drop=True)
raw_beta = raw.iloc[3108:4138]['Unnamed: 5'].reset_index(drop=True)
raw_gamma = raw.iloc[4143:5173]['Unnamed: 5'].reset_index(drop=True)

data = pd.concat([raw_delta, raw_theta, raw_alpha, raw_beta, raw_gamma], axis=1)
data.drop(index=[546, 547, 548, 549], inplace=True)
data.reset_index(drop=True, inplace=True)


# Preproc
# Data Preproc
def pval(data, num_groups):
    triangular_list = np.tril_indices(num_groups, -1)
    length = len(triangular_list[0])

    result = []

    for num in range(length):
        cn_ad = data[num * 6]
        ad_ftd = data[num * 6 + 1]
        ftd_cn = data[num * 6 + 3]
        cell = [cn_ad, ad_ftd, ftd_cn]

        result.append(cell)

    return result


# 1로 채워진 (19x19) 배열 만들기
triangular_list = np.tril_indices(19, -1)
idx_list = []

for i in range(len(triangular_list[0])):
    idx = [triangular_list[0][i], triangular_list[1][i]]
    idx_list.append(idx)


# 배열에 값 채우기
def fc_data(group):
    value = np.zeros((19, 19))

    for node_x in range(19):
        for node_y in range(19):
            if [node_x, node_y] in idx_list:
                num_idx = idx_list.index([node_x, node_y])
                value[node_x, node_y] = group.iloc[num_idx]

    return value


values = pd.DataFrame(pval(data.iloc[:, 4], 19))  # data.iloc[:, 4] -> 0~4 : five freq bands
ad_cn = fc_data(values.iloc[:, 0])
ad_ftd = fc_data(values.iloc[:, 1])
ftd_cn = fc_data(values.iloc[:, 2])
pd.DataFrame(ftd_cn).to_excel("fc.xlsx")
