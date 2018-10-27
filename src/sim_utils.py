from random import sample


def frameToTime(frames):
    """ Converts frames (10 fps) into corresponding formattted
    string 'hh:mm:ss:msms'.
    >>> frameToTime(100)
    '0:00:10:00'
    >>> frameToTime(72000)
    '2:00:00:00'
    """
    frames = int(frames)
    msec = frames % 10 * 6
    frames //= 10 
    hour = frames // 3600
    frames %= 3600 
    min = frames // 60
    sec = frames % 60
    
    if min // 10 == 0:
        min = '0{}'.format(min)
    if sec // 10 == 0:
        sec = '0{}'.format(sec)
    if msec // 10 == 0:
        msec = '0{}'.format(msec)

    return '{:>4}:{}:{}:{}'.format(hour, min, sec, msec)


def print_status(time, status):
    print(f'{frameToTime(time)} - {status}')


def id_generator():
    id = 1
    while True:
        yield id
        id += 1
 

id_gen = id_generator()


class Request:
    def __init__(self, origin, destination, time):
        self.id = next(id_gen) 
        self.origin = origin
        self.dest = destination
        self.time = time
        self.wait_time = None
        self.done = False

 
def randreq(time, upper_bound, lower_bound=1):
    origin, dest = sample([i for i in range(lower_bound, upper_bound + 1)], 2)
    return Request(origin, dest, time)


def flag():
    print("========================FLAG========================")

