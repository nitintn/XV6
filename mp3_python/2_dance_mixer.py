from threading import Semaphore,Lock,Thread
from time import sleep
from collections import deque
import random

# dance length for each dancer
dance_length = 5

#list of songs
songs_list = ['waltz', 'tango', 'foxtrot']

# semaphores
leaderArrived = Semaphore(0)
followerArrived = Semaphore(0)

# Loop condition for dance
DANCETIME = True

# Dancefloor
class Dancefloor:
    # Semaphores
    # Mutex to block access to dancefloor
    dancefloor_open = Semaphore(0)
    # Mutex protecting count variables
    dancefloor_mtx = Semaphore(1)
    # Mutex to wake up band leader then dance floor is empty
    dancefloor_empty = Semaphore(0)
    # keeping count of dancing couples
    count = 0
    closed = True

    @staticmethod
    def open():
        Dancefloor.dancefloor_open.release()

    @staticmethod
    def close():
        Dancefloor.dancefloor_open.acquire()
        Dancefloor.dancefloor_empty.acquire()

    @staticmethod
    def enter():
        Dancefloor.dancefloor_open.acquire()
        Dancefloor.dancefloor_mtx.acquire()
        Dancefloor.count += 1
        Dancefloor.dancefloor_mtx.release()
        Dancefloor.dancefloor_open.release()

    @staticmethod
    def exit():
        Dancefloor.dancefloor_mtx.acquire()
        Dancefloor.count -= 1
        if Dancefloor.count == 0 and Dancefloor.closed:
            Dancefloor.dancefloor_empty.release()
        Dancefloor.dancefloor_mtx.release()

# Queues for both leaders and followers
class Queues:
    leadersQ = deque()
    followersQ = deque()
    # to avoid empty queues, applying semaphores
    leaders = Semaphore(0)
    followers = Semaphore(0)

    @staticmethod
    def append(role, ticket):
        if role == "Leader":
            Queues.leadersQ.appendleft(ticket)
            Queues.leaders.release()
        else:
            Queues.followersQ.appendleft(ticket)
            Queues.followers.release()

    @staticmethod
    def pop():
        #acquire locks for leader & follwers, pop them from the QUEUE
        Queues.leaders.acquire()
        Queues.followers.acquire()

        popped_leader = Queues.leadersQ.pop()
        popped_leader.release()

        popped_follower = Queues.followersQ.pop()
        popped_follower.release()

# Dancer class
class Dancer:
    # constructor to know whether it is dancer or follower
    def __init__(self, role, idx):
        global leaderArrived, followerArrived
        self.role = role
        self.idx = idx
        self.name = role + " " + str(idx)
        self.queue_ticket = Semaphore(0)

        if role == "Leader":
            self.arrivedSem = leaderArrived
            self.partnerSem = followerArrived
        else:
            self.arrivedSem = followerArrived
            self.partnerSem = leaderArrived

    def run(self):
        global DANCETIME, dancefloor_open
        dancing_time = rng.random()

        while(True):
            # adding to QUEUE
            Queues.append(self.role, self.queue_ticket)
            self.queue_ticket.acquire()
            #enter dancefloor
            Dancefloor.enter()
            # checking condition before entering dancefloor
            if not DANCETIME:
                break
            print(self.name + " entering floor")

            if self.role == "Leader":
                follower_name = ""

                self.partnerSem.acquire()
                partner_name = follower_name
                self.arrivedSem.release()
                print(self.name + " and " + partner_name + " are dancing.")
                # call to Queue to pop next couple from waiting QUEUE
                Queues.pop()
            else:
                follower_name = self.name
                self.arrivedSem.release()
                self.partnerSem.acquire()
            sleep(dancing_time)

            Dancefloor.exit()
            print(self.name + " getting back in line.")

# Band leader
# switches between songs
class BandLeader:
    def __init__(self):
        global dance_length

    def run(self):
        global songs_list
        # pop first couple out of the waiting queue
        Queues.pop()
        for dance in songs_list:
            print("\n** Band Leader started playing " + dance + " **")
            Dancefloor.open()
            sleep(dance_length)
            Dancefloor.close()
            print("** Band Leader stopped playing " + dance + " **\n")


if __name__ == '__main__':
    num_leaders = int(input("Number of Leaders:"))
    num_followers = int(input("Number of followers:"))
    rng = random.Random()
    # Bandleader
    bl = BandLeader()
    bandleader_th = Thread(target= bl.run)
    dancers = []
    dancing_time = rng.random()
    # Leaders thread
    leaders_th = []
    for i in range(0, num_leaders):
        d = Dancer("Leader",i)
        dancers.append(d)
        leaders_th.append(Thread(target = d.run))
        leaders_th[i].start()

    # Followers thread
    followers_th = []
    for i in range(0, num_followers):
        d = Dancer("Follower",i)
        dancers.append(d)
        followers_th.append(Thread(target = d.run))
        followers_th[i].start()

    bandleader_th.start()
    bandleader_th.join()
    # wait for all dancers to finish dancing
    sleep(dancing_time)
    DANCETIME = False
    # wake up all dancers
    Dancefloor.open()
    for d in dancers:
        d.queue_ticket.release()

    # thread join on all dancers
    for i in range(0, num_leaders):
        leaders_th[i].join()
    for i in range(0, num_followers):
        followers_th[i].join()