#daemon = True
# 1 core should equal 2*1+1=3 workers
workers = 3
# we want to use threads for concurrency. we estimate that a maximum of 3*7=21 users will use the application simultaneously
worker_class = "gthread"
threads = 7
#accesslog = "logs/access.log"
#errorlog = "logs/error.log"
