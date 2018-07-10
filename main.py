# Script for reading in BLM data from LHC logging database based on PyTIMBER
# https://github.com/rdemaria/pytimber/
#
# BLM variables
#
# :DOSE_INT_HH
# :LOSS_FAST
# :LOSS_RS01 ... RS12
# :THRES_RS01 ... RS12
#
# mikael.mieskolainen@cern.ch, 2016


# Read in csv file with BLM labels and distance from IP1 (ATLAS) towards ALICE (m)
import csv

with open('DCUM-090516.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

# import PyTimber
import pytimber


# Create database access
ldb = pytimber.LoggingDB()

# Fill number
fillnro = 5117

# BLM integrator length
BLM_integrator = 'LOSS_RS02'

# Open output file
output_filename = 'FILL_' + str(fillnro) + '.out'
f = open(output_filename, 'w')

print('Reading data from fill', fillnro)

# Get data
fill = ldb.getLHCFillData(fillnro)
t1 = fill['startTime']
t2 = fill['endTime']

i = 1;

print('Start time', t1)
print('End time', t2)
print('Writing data...')

# Loop over BLMs from the .csv file list
for item in your_list:
	BLM_name = item[0] + ':' + BLM_integrator
	s_distance = item[1]
	d = ldb.get(BLM_name, t1, t2)

	# If there was data for this BLM
	if d:
		
		# Here we just index with k == 1, because above we select single BLM by BLM
		for k in d:
			output_string = BLM_name + ',' + s_distance
			time_stamps = d[k][0] # 0 = time stamps
			values      = d[k][1] # 1 = measurement values

			# Loop over time series values
			for numval in values:
				strval = "%.6f" % numval # conver to string
				output_string = output_string + ',' + strval
			
			output_string = output_string + '\n'

			print(i, BLM_name)
			f.write(output_string)

			i = i + 1
	else:
		output_string = BLM_name + ',' + s_distance + ',0' + '\n'
		print(i, BLM_name, 'Not Found!')
		f.write(output_string)
		
		i = i + 1


# Close the file
f.close()

#
## Find variables
#vars = ldb.search('BLM%DOSE_INT_HH')
#print(vars)
#
#for x in vars:
#	d = ldb.get(x, t1, t2)
#	print(d)
