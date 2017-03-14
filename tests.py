from operator import itemgetter
from itertools import chain, starmap, islice
from collections import Counter
from itertools import groupby
from operator import eq
import time
from more_itertools import unique_everseen
from cardinality import at_least
from tally import Tally


def it_should_match_counters_results_for_complete_ranking(seq):
    def grouped(records, key):
        """a helper because groupby requires sorted elements"""
        sorted_records = sorted(records, key=key)
        yield from groupby(sorted_records, key=key)

    def rankings_match(ranking_left, ranking_right):
        """if there's a tie, counter will return elements in random order
        so here i'm just grouping by count and comparing sets of keys"""
        def item_sets(ranking):
            return [set(map(itemgetter(1), group)) for score, group in grouped(ranking, key=itemgetter(1))]

        return all(starmap(eq, zip(item_sets(ranking_left), item_sets(ranking_right))))

    t = Tally()
    c = Counter()
    for num in seq:
        t.tally(num)
        c[num] += 1
        assert rankings_match(list(c.most_common()), list(t.descending()))
        assert rankings_match(
            list(reversed(list(c.most_common()))), list(t.ascending()))


def it_should_be_faster_than_counter_for_getting_the_extremes(seq):
    """
    Counter.most_common() uses a heap
    so each call, it should be nlogn to sort the results

    Tally keeps elements in sorted order, so getting the top-k results should be constant (k) time
    """
    assert at_least(100, unique_everseen(
        seq))  # if the cardinality is low, the the sorting cost Counter requires is negilable

    t = Tally()
    tally_start = time.time()
    for num in seq:
        t.tally(num)
        _ = list(islice(t.descending(), 0, 1))
    tally_time = time.time() - tally_start

    c = Counter()
    counter_start = time.time()
    for num in seq:
        c[num] += 1
        _ = c.most_common(1)
    counter_time = time.time() - counter_start

    assert tally_time < counter_time

if __name__ == '__main__':
    import random
    seq = [random.randint(0, 1000) for _ in range(20000)]
    it_should_match_counters_results_for_complete_ranking(seq)
    it_should_be_faster_than_counter_for_getting_the_extremes(seq)
