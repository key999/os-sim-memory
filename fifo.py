from page import Page


# main fifo algorithm function
# takes variables:
# chain - list of int values determining pages needed by the algorithm
# mem_size - int value determining amount of frames allocated for the process
# pages - int value determining amount of different pages the process may need
# verbose - controls if the function should be run in quiet or verbose mode
def fifo(chain, mem_size, pages, verbose="n"):
    # a quick function to print out swap
    def see_swap():
        print()
        for i in swap:
            print(i.id, ":", i.validity, end=' | ', sep='')
        print()

    # setting needed variables
    to_write = ""  # what will be written to output file
    dram = [Page() for _ in range(mem_size)]  # imitates process frames / operating memory
    swap = [Page(id=i) for i in range(pages)]  # imitates swap memory containing every page
    swap = tuple(swap)  # 'tuplify' the swap so that it stays unchanged
    page_fault_counter = oldest = 0  # initialise page fault counter, oldest frame pointer and presence
    present = -1

    # first, show the chain of pages the process needs
    print("Chain of references:", chain) if verbose == "yes" else None
    to_write += ("chain:" + str(chain) + "\n")

    # "process" working loop
    for i in chain:
        present = -1  # needed for later, do not modify

        # show current memory frames
        p = '['
        print("\n[ ", end='') if verbose == "yes" else None
        for j in dram:
            print(j, end=' ') if verbose == "yes" else None
            p += str(j.id) + " "
        print("]", end='') if verbose == "yes" else None
        p += "]"
        to_write += "\n" + p + "\n"

        # ensure var oldest does not go over memory size
        oldest %= mem_size

        # search for page i in operating memory
        # if it is present, set present to 1, otherwise set to 0
        print() if verbose == "yes" else None
        for j in dram:
            if j.id == i:
                present = 1
                # set the page referenced bit to 1
                # needed for second chance fifo
                j.referenced = 1
                break
            else:
                present = 0

        # frame is in operating memory
        if present == 1:
            # notify that it is present
            print("\t{0} is in".format(i), end='') if verbose == "yes" else None
            to_write += ("\t{0} is in".format(i) + "\n")
            see_swap() if verbose == "yes" else None

            # since the page is in the memory the process is able to use it and does not throw page fault
            # continue with next needed page
            continue

        # frame is not in operating memory
        else:
            # increment page fault counter by 1
            page_fault_counter += 1

            # notify that the frame is absent
            print("\t{0} is not in,".format(i), end='') if verbose == "yes" else None
            to_write += ("\t{0} is not in,".format(i) + "\n")
            see_swap() if verbose == "yes" else None

            # check if operating memory still has a free frame
            try:
                # find where is a free frame
                pointer = 0  # points at the frame with no page in it
                found = False
                for j in dram:
                    if j.id == -1:
                        # found it
                        found = True
                        break
                    pointer += 1

                # there are no free frames
                # go to:
                # except ValueError
                if not found:
                    raise ValueError

                # there is a free frame, use it to allocate needed page
                # set required page in it and change its validity bit
                dram[pointer] = swap[i]
                swap[i].validity = 1

                # notify about moving to first free frame
                print("\tmoving page to first free frame", end='') if verbose == "yes" else None
                to_write += ("\tmoving page to first free frame" + "\n")

            # there are no free frames
            except ValueError:
                # check if page set for swapping was referenced lately
                # iterate over memory:
                # this is the actual second chance FIFO algorithm

                oldest_copy = oldest  # local copy of variable oldest pointing to the oldest frame
                x = 0
                while x >= 0:
                    oldest_copy %= mem_size
                    # was not referenced lately
                    if dram[oldest_copy].referenced == 0:
                        # zero validity bit of page that is about to be unloaded from memory
                        x = dram[oldest_copy].id
                        swap[x].validity = 0

                        dram[oldest_copy] = swap[i]  # swap oldest page in memory with a needed page from swap
                        swap[i].validity = 1  # set validity bit of the needed page to 1 to indicate it is in memory
                        oldest_copy += 1  # set pointer to next oldest page in memory
                        oldest += 1  # increment global oldest pointer by 1
                        oldest %= mem_size
                        break

                    # was referenced lately
                    elif dram[oldest_copy].referenced == 1:
                        print("X", end='') if verbose == "yes" else None
                        # zero the referenced bit
                        # and increment oldest page pointer
                        dram[oldest_copy].referenced = 0
                        oldest_copy += 1
                        oldest += 1

                # notify about swapping pages
                print("\tchanging {0} to {1}".format(dram[oldest], i), end='') if verbose == "yes" else None
                to_write += ("\tchanging {0} to {1}".format(dram[oldest], i) + "\n")

        print() if verbose == "yes" else None

    # at the end show operating memory
    # just for reference and to see what the algorithm actually did
    p = '['
    print("\n[ ", end='') if verbose == "yes" else None
    for j in dram:
        print(j, end=' ') if verbose == "yes" else None
        p += str(j.id) + " "
    print("]", end='') if verbose == "yes" else None
    p += "]"
    to_write += p

    with open("output_fifo.csv", "a") as f:
        f.write(to_write + "\npage faults: " + str(page_fault_counter) + "\n\n")

    return page_fault_counter


if __name__ == "__main__":
    fifo([1, 5, 4, 2, 7, 11, 11, 13, 1, 1, 2, 1, 3, 1], 3, 14)
