import pandas as pd
import numpy as np
import scipy.stats
from sklearn.preprocessing import StandardScaler 
from warnings import simplefilter

simplefilter(action = 'ignore', category = RuntimeWarning)

freq_table = pd.read_csv(r'.\frequency_table.csv')

#Acquired data containing all mco data from 2015
all_mco_data = pd.read_excel('../all_mco_data.xlsx', header = 0, delimeter = ',')

#Creating dataframe based on predictors used only for more efficient looping
predictors = pd.DataFrame(columns = ['ORIGIN_AIRPORT', 'AIRLINE', 'arrival_time_bucket', 'ARRIVAL_DELAY', 'bin_arrival_delay'], \
						data = all_mco_data)

del all_mco_data

condition = predictors.bin_arrival_delay == 1
predictors = predictors[condition]

freq_table = freq_table.dropna()
late_list = pd.DataFrame(columns = ['Late List'])

#Populates frequency table with distribution data
def my_iter(origin_freq, airline_freq, time_freq, origin_data, airline_data, time_data, delay):
	for z in range(len(origin_freq)):
		l = []
		for i in range(len(origin_data)):
			if origin_freq[z] == origin_data[i] and airline_freq[z] == airline_data[i]\
				and time_freq[z] == time_data[i]:
					if delay[i] < 120:
						l.append(delay[i])

		late_list.at[z, 'Late List'] = l

my_iter(freq_table['Origin'].values, freq_table['Airline'].values, freq_table['Time'].values, \
		predictors['ORIGIN_AIRPORT'].values, predictors['AIRLINE'].values, \
		predictors['arrival_time_bucket'].values, predictors['ARRIVAL_DELAY'].values)

sc = StandardScaler()

dist_names = ['beta',
              'expon',
              'gamma',
              'lognorm',
              'norm',
              'triang',
              'uniform',
              'weibull_min', 
              'weibull_max']

distributions = []
parameters = []

for i in range(len(late_list)):
	print(i)
	dist_1 = late_list.loc[i].values
	dist_1 = dist_1[0]

	if dist_1 == []:
		set_dist = 'n/a'
		distributions.append(set_dist)
		continue

	new_dist = []
	for val in dist_1:
		new_dist.append(val)

	new_dist = np.array(new_dist)
	new_dist = new_dist.reshape(-1, 1)
	sc.fit(new_dist)

	size = len(new_dist)

	pct_bins = np.linspace(0, 100, 51)
	pct_vals = np.percentile(dist_1, pct_bins)
	print(pct_vals)
	observed_freq, bins = (np.histogram(dist_1, bins = pct_vals))
	cumulative_obs_freq = np.cumsum(observed_freq).astype('float64')

	chi_2 = []
	p_val = []

	z = 1
	for dist in dist_names:
		distribution = getattr(scipy.stats, dist)
		param = distribution.fit(new_dist)

		#P-Statistic
		p = scipy.stats.kstest(dist_1, dist, args = param)[1]
		p = np.round(p, 5)
		p_val.append(p)
		z += 1

		#CDF Used for Chi Squared 
		cdf = distribution.cdf(pct_vals, *param[:-2], loc = param[-2], scale = param[-1])
		exp_freq = []
		for bin in range(len(pct_bins) - 1):
			exp_cdf = cdf[bin + 1] - cdf[bin]
			exp_freq.append(exp_cdf)

		exp_freq = np.array(exp_freq) * size
		cum_exp_freq = np.cumsum(exp_freq)
		sq = 0
		i = 0
		for val in cumulative_obs_freq:
			if val != 0:
				sq += ((cum_exp_freq[i] - cumulative_obs_freq[i]) ** 2) / cumulative_obs_freq[i]
			i += 1
		chi_2.append(sq)

	rankings = pd.DataFrame()
	rankings['Distribution'] = dist_names
	rankings['Chi Squared'] = chi_2
	rankings['P-Value'] = p_val

	rankings.sort_values(['Chi Squared'], inplace = True)

	for i, row in rankings.iterrows():
		if row['P-Value'] > 0.05:
			set_dist = row['Distribution']
			
			break

	distributions.append(set_dist)

freq_table['Distributions'] = distributions

z = 0
for i, row in freq_table.iterrows():
	dist = row['Distributions']
	data_set = late_list.loc[z].values
	data_set = data_set[0]

	if dist == 'n/a':
		parameter = 'n/a'

	else:
		parameter = getattr(scipy.stats, dist).fit(data_set)

	parameters.append(parameter)
	z += 1

print('DONE')

freq_table['Parameters'] = parameters

freq_table.to_csv('./frequency_table_v3.csv', index = False, header = True)

'''
for z, row_ in freq_table.iterrows():
		print(z)
		l = []
		for i, row in predictors.iterrows():
			if row['ORIGIN_AIRPORT'] == row_['Origin'] and row['AIRLINE'] == row_['Airline']\
				and row['arrival_time_bucket'] == row_['Time']:
				l.append(row['ARRIVAL_DELAY'])

		late_list.at[z, 'Late List'] = l
'''
