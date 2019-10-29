from fifo import fifo
from lru import lru
from prepare import prepare
from load import load

# exit codes:
# 0 - correct execution
# 1 - unexpected outcome in lru
# 3 - input data file not found


def run(select="both", frames=3, pages=20, verbose="no"):
    if select == "fifo":
        chain = load()
        average = 0
        for i in chain:
            w = fifo(i, frames, pages, verbose=verbose)
            print("\nPage faults for second chance FIFO:", w, end='')
            average += w
        average /= len(chain)
        print("\nAverage page faults for second chance FIFO", average)
        with open("output_fifo.csv", "a") as f:
            f.write("\nAverage page faults for FIFO " + str(average))

    elif select == "lru":
        chain = load()
        average = 0
        for i in chain:
            w = lru(i, frames, pages, verbose)
            print("\nPage faults for LRU:", w, end='')
            average += w
        average /= len(chain)
        print("\nAverage page faults for LRU", average)
        with open("output_lru.csv", "a") as f:
            f.write("\nAverage page faults for LRU " + str(average))

    else:
        chain = load()
        average_fifo = average_lru = 0
        for i in chain:
            average_fifo += fifo(i, frames, pages, verbose=verbose)
            average_lru += lru(i, frames, pages, verbose=verbose)
        average_fifo /= len(chain)
        average_lru /= len(chain)
        print("\nAverage page faults for second chance FIFO", average_fifo)
        with open("output_fifo.csv", "a") as f:
            f.write("\nAverage page faults for FIFO " + str(average_fifo))
        print("\nAverage page faults for LRU", average_lru)
        with open("output_lru.csv", "a") as f:
            f.write("\nAverage page faults for LRU " + str(average_lru))


if __name__ == "__main__":
    S = 20
    # prepare(length=100, pages=S, chains=100)
    run("both", frames=9, pages=S, verbose="yes")
