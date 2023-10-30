import pandas as pd

#Acquired data containing all mco data from 2015
all_mco_data = pd.read_excel('../all_mco_data.xlsx', header = 0)

#SEPARATED DATA FROM ALL MCO DATA
origins = all_mco_data['ORIGIN_AIRPORT']
all_locs = origins.unique()
all_airlines = all_mco_data.AIRLINE.unique()

origins_airlines_combo = []
#ALSO USING TIME OF DAY AS PREDICTIVE FACTOR
#3 = Night [20:00-4:00), 2 = Afternoon [12:00-20:00), 1 = Morning [4:00-12:00)
times = [1, 2, 3]
for loc in all_locs:
	for air in all_airlines:
		for time in times:
			origins_airlines_combo.append([loc, air, time])

freq_table = pd.DataFrame(origins_airlines_combo, columns = ['Origin', 'Airline', 'Time'])
freq_table['On_Time'] = 0
freq_table['Late'] = 0
freq_table['Probability_Late'] = 0

#Populates frequency table
for i in range(len(all_mco_data)):
	print(i)
	for z in range(len(freq_table)):
		if all_mco_data['ORIGIN_AIRPORT'][i] == freq_table['Origin'][z] and all_mco_data['AIRLINE'][i] == freq_table['Airline'][z]\
			and all_mco_data['arrival_time_bucket'][i] == freq_table['Time'][z]:

			if all_mco_data['bin_arrival_delay'][i] == 1:
				freq_table.loc[z, 'Late'] = freq_table.Late[z] + 1
			else:
				freq_table.loc[z, 'On_Time'] = freq_table.On_Time[z] + 1

#Finds probability that a flight is late based on frequency table data
for y in range(len(freq_table)):
	freq_table.loc[y, 'Probability_Late'] = freq_table.Late[y] / (freq_table.Late[y] + freq_table.On_Time[y])

print(freq_table)

freq_table.to_csv('./frequency_table.csv', index = False, header = True)