from threading import Semaphore, Thread
from time import sleep
import random
import timeit

# calculation for left and right fork id's
def left_fork(id):
	return id
def right_fork(id):
	return (id + 1) % num_philosophers

# acquiring locks to the forks being used
def get_forks(i):
	forks[(right_fork(i))].acquire()
	forks[(left_fork(i))].acquire()
# releasing locks to the forks after used
def put_forks(i):
	forks[(right_fork(i))].release()
	forks[(left_fork(i))].release()

# leftright
# acquiring lock on left first and then right fork
def get_left_forks(i) :
	forks[(left_fork(i))].acquire()
	forks[(right_fork(i))].acquire()

# tanenbaum
# acquiring lock
def get_fork_tan(phil_id):
	mutex.acquire()
	state[phil_id] = 'HUNGRY'
	test(phil_id)
	mutex.release()
# releasing lock
def put_fork_tan(phil_id):
	mutex.acquire()
	state[phil_id] = 'THINKING'
	test((phil_id+num_philosophers-1)%num_philosophers)
	test((phil_id-num_philosophers-1)%num_philosophers)
	mutex.release()
# testing whether the neighbours are eating
def test(id):
	if state[id]=='HUNGRY' and  state[(id+num_philosophers-1)%num_philosophers]!='EATING' \
			and state[(id+1)%num_philosophers]!='EATING':
		state[id]='EATING'
		mutex_one.release()

def tanenbaum_solution(philosopher_id):
	meals_count = 0
	rng.seed(100)
	prng=rng.random()
	while meals_count != meals:
		get_fork_tan(philosopher_id)
		sleep(prng)
		meals_count+=1
		put_fork_tan(philosopher_id)

# left right solution
def leftright_solution(philosopher_id):
	meals_count=0		# count of meals
	while meals_count!=meals:
		rng.seed(100)
		prng=rng.random()
		if philosopher_id==0 :		# only one philosopher takes left fork first
			get_left_forks(philosopher_id)
			sleep (prng)
		else :						# rest all philosophers takes right fork first
			get_forks(philosopher_id)
			sleep (prng)
		meals_count +=1				# keeping count of meals
		put_forks(philosopher_id)

# footman solution
def footman_solution(philosopher_id):
	meals_count=0		# count of meals
	while meals_count!=meals:
		rng.seed(100)
		prng=rng.random()
		get_forks(philosopher_id)
		meals_count +=1	# keeping count of meals
		sleep (prng)
		put_forks(philosopher_id)

# functions for time calculation
# tanenbaum
def Tanenbaum() :
	Tannenbaum_th=list()		# creating list to append threads
	start_time = timeit.default_timer()
	for i in range(num_philosophers):
		philosopher_th = Thread(target=tanenbaum_solution, args=[i]) # creating philosopher threads
		philosopher_th.start()
		Tannenbaum_th.append(philosopher_th)
	for i in Tannenbaum_th:
		i.join()			# joining all the threads
	stop_time = timeit.default_timer()
	print ('3.Tanenbaums solution, time elapsed',stop_time - start_time)

# Leftright
def Leftright() :
	Leftright_th= list()		# creating list to append threads
	start_time = timeit.default_timer()
	for i in range(num_philosophers):
		philosopher_th = Thread(target=leftright_solution, args=[i])  # creating philosopher threads
		philosopher_th.start()
		Leftright_th.append(philosopher_th)
	for i in Leftright_th:
		i.join()			# joining all the threads
	stop_time = timeit.default_timer()
	print ('2.LeftRight solution, time elapsed',stop_time - start_time)

#Footman
def Footman() :
	Footman_th=list()		# creating list to append threads
	start_time = timeit.default_timer()
	for i in range(num_philosophers):
		philosopher_th = Thread(target=footman_solution, args=[i])  # creating philosopher threads
		philosopher_th.start()
		Footman_th.append(philosopher_th)
	for i in Footman_th:
		i.join()			# joining all the threads
	stop_time = timeit.default_timer()
	print ('1.Footman solution, time elapsed',stop_time - start_time)

# main function
if __name__ == '__main__':
	# user input
	num_philosophers = int(input('Number of philosopher dining : '))
	meals=int(input('Number of meals each philosopher will eat : '))

	# initializing semaphores
	mutex = Semaphore(1)
	mutex_one = Semaphore(1)
	# intializing the state of the philosophers to Thinking
	state = ['THINKING']*num_philosophers
	# generating random numbers
	rng = random.Random()

	forks = [Semaphore(1) for i in range(num_philosophers)]
	# calling fucntions
	Footman()
	Leftright()
	Tanenbaum()
