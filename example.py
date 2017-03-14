from tally import Tally
from more_itertools import repeatfunc, first
from itertools import islice
import silly
import random

t = Tally()


def print_results(t):
    for i, namevotes in enumerate(islice(t.descending(), 0, 3)):
        name, votes = namevotes
        print("#{} is {} with {} votes. ".format(i + 1, name, votes), end='\t')
    print()

an_infinite_stream_of_random_names = repeatfunc(silly.firstname)
for num in an_infinite_stream_of_random_names:
    t.tally(num)
    print_results(t)

    if random.random() < .01:
        name, votes = first(t.descending())
        t.remove(name)
        print('OH NO!!! {} JUST GOT BLUE-SHELLED'.format(name))
