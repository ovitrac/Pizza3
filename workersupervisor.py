#### Algorithm for supervisor - workers to automate running of working directory

# SUPERVISOR

while 
	check every 30 seconds
		if jobs added to folder
			while incompletejobs
				if sparecores # if there are spare cores available, try to run a job
					launch worker_function


# WORKER

worker fucntion:

go to jobs directory # jobs/job1 job2 ... jobn

for i in jobs
	if! TEMPi or DONEi
		make TEMPi
		execute jobi # launch function
		make DONEi
		remove DONEi

# LAUNCH



if multiplecores
	compute no. cores
else
	execute
