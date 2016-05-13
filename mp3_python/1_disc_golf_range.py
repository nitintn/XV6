from threading import Semaphore,Lock, Thread
from time import sleep
import random

#initializing semaphores
send_cart = Semaphore(0)
mutex = Semaphore(1)
cart = Semaphore(0)
mutex_ballinc = Semaphore(1)

rng = random.Random()  # used to generate random number

#initializing the variables, in case the user does not give any input
stash = 1   # number of discs in central stash
bucket = 1  # number od discs in bucket present with each frolfer
frolfer = 1 # number of frolfers playing
discs_on_field =0 # initially discs on the field

def disc_golf_range(frolfer_id):
    global stash, discs_on_field
    rng.seed(100)                       # generates random number
    prng=rng.random()                   # so that that value will
    while(True):
        mutex.acquire()                         # lock acquired to make changes in the stash value
        print('Frolfer',frolfer_id,'calling for bucket')
        if stash >= bucket:                     # initially the frolfer calls for bucket
            stash = stash-bucket
            print('Frolfer',frolfer_id,'got',bucket,'discs; ','Stash = ',stash)
        else:
            send_cart.release()                 # lock released to send cart to grab discs from filed
            cart.acquire()                      # lock acquired so as to send cart only once
            stash = stash-bucket
            print('Frolfer',frolfer_id,'got',bucket,'discs;','Stash =',stash)
        mutex.release()                         # lock released so that others can stash value

        for i in range(bucket):                 # frolfer starts throwing
            mutex_ballinc.acquire()             # lock acquired to count discs on the field
            print('Frolfer',frolfer_id,'threw disc ',i)
            discs_on_field +=1
            mutex_ballinc.release()             # lock released so that other frolfer can throw discs
            sleep (prng)                        # be used for random sleep

def collect_discs():                                # function to fill cart to refill central stash
    global stash, discs_on_field
    while(True):
        send_cart.acquire()                     # lock acquired not to allow cart to go on field
        print('#############################################')
        print('Stash = ', stash ,';Cart entering field')
        stash += discs_on_field
        print('Cart done, gathered ',discs_on_field,' discs ',' Stash = ',stash)
        discs_on_field = 0
        print('#############################################')
        cart.release()                          # lock released for next thread to execute

if __name__ == '__main__':
    # user inputs
    stash= int(input('Enter the number of discs in the Stash: '))
    bucket=int(input('Enter the number of discs in the bucket(for each Frolfer): '))
    frolfer=int(input('Enter the number of Frolfer playing : '))
    # creatng cart thread
    cart_thread = Thread(target= collect_discs)
    cart_thread.start()   #thread starts
    for i in range (frolfer):
        frolfer_thread = Thread(target=disc_golf_range,args=[i]) # creating frolfer thread
        frolfer_thread.start()                              # thread starts an has as many as number of frolfer