import collections
import queue
import argparse
import random

DEFAULT_TAXI_NUM = 3
DEPARTURE_INTERVAL = 5
DEFAULT_END_TIME = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20



Event = collections.namedtuple('Event', 'time ident action')

def taxi_proc(ident, trips, start_time=0):
    time = yield Event(start_time, ident, 'leave garage')
    for i in range(trips):
        time = yield Event(time, ident, 'pick up passager')
        time = yield Event(time, ident, 'drop off passager')
    yield Event(time, ident, 'going home')

class Simulator:
    def __init__(self, procs):
        self.events = queue.PriorityQueue()
        #<dict()> to get copy version, to protect <procs>, 
        #which is transfered by users,  not to be modified
        self.procs = dict(procs) 
    def run(self, end_time):
        for _, proc in self.procs.items():
            first_event = next(proc)
            self.events.put(first_event)
        sim_time = 0

        while sim_time < end_time:
            if self.events.empty():
                print('***end of events***')
                break
            current_event = self.events.get()
            sim_time, proc_id, previous_action =  current_event
            print('taxi:', proc_id, proc_id * ' ', current_event)
            next_time = sim_time + compute_duration(previous_action) 
            active_proc = self.procs[proc_id]
            try:
                next_proc = active_proc.send(next_time)
            except StopIteration:
                del self.procs[proc_id]
            else:
                self.events.put(next_proc)
        else:
            print('***end of simulator time, {} events pending***'.format(self.events.qsize()))
            
def compute_duration(previous_action):
    if previous_action in ['leave garage', 'drop off passager']:
        interval = SEARCH_DURATION 
    elif previous_action == 'pick up passager':
        interval = TRIP_DURATION 
    elif previous_action == 'going home':
        interval = 1 
    else:
        raise ValueError('invalid action')

    return int(random.expovariate(1/interval) + 1)


def main(end_time = DEFAULT_END_TIME, seed = None):
    taxis = {i: taxi_proc(i, (i+1)*2, i*DEPARTURE_INTERVAL) 
            for i in range(DEFAULT_TAXI_NUM)}
    if seed is None:
        random.seed(seed)

    sim = Simulator(taxis)
    sim.run(end_time)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='args from cmd line')
    arg_parser.add_argument('-s', '--seed')
    args = arg_parser.parse_args()
    main(seed=args.seed)

