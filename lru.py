from page import Page, PageFault


# main lru algorithm function
# takes variables:
# chain - list of int values determining pages needed by the algorithm
# mem_size - int value determining amount of frames allocated for the process
# pages - int value determining amount of different pages the process may need
# verbose - controls if the function should be run in quiet or verbose mode
def lru(chain, mem_size, pages, verbose="yes"):
    global i  # just to satisfy pycharm's whingeing
    memory = [Page() for _ in range(mem_size)]  # imitates process' operating memory
    swap = [Page(i) for i in range(pages)]  # imitates swap memory
    swap = tuple(swap)  # 'tuplify' swap so that it stays unchanged
    stack = []  # for keeping track of oldest pages
    page_fault_counter = 0  # page fault counter
    to_write = str(chain)

    # quick function for printing memory or swap
    def print_list(w):
        print("[ ", end='', sep='')
        p = "[ "
        for i in w:
            print(i, end=' ', sep='')
            p += str(i) + " "
        print("]")
        p += "]"
        return p

    # "process" working loop
    for needed_page in chain:
        # print memory frames and current stack
        to_write += "\nmemory: " + print_list(memory) if verbose == "yes" else None
        print("stack: ", end='') if verbose == "yes" else None
        to_write += "\nstack: " + print_list(stack) if verbose == "yes" else None

        # check if needed page is in memory
        try:
            present = 0
            for i in memory:
                if needed_page == i.id:
                    present += 1
                elif needed_page != i.id:
                    pass

            if present == 1:
                # present
                print("Page {0} is present".format(needed_page)) if verbose == "yes" else None
                to_write += "\n" + "Page {0} is present".format(needed_page)
            elif present == 0:
                # not present, go to:
                # except PageFault
                raise PageFault
            else:
                # unexpected outcome in lru
                exit(1)
        except PageFault:
            page_fault_counter += 1

            # try to find a free frame
            free = False
            for i in range(len(memory)):
                if memory[i].id == -1:
                    # found a free frame
                    free = True
                    break

            # found a free frame
            if free:
                print("Page {0} not present, but a free frame exists. Moving to free frame".format(
                    needed_page)) if verbose == "yes" else None
                to_write += "\n" + "Page {0} not present, but a free frame exists. Moving to free frame".format(
                    needed_page)
                # var i is still set after previous for loop
                memory[i] = swap[needed_page]

            # did not find a free frame
            # swap out the oldest frame
            elif not free:
                # first, find which frame holds the least recently used page in operating memory
                w = [i.id for i in memory]  # simplify memory
                for i in stack:  # try to find the oldest page from stack in memory
                    if i in w:
                        # when found, break
                        break

                oldest = w.index(i)

                print("Page {0} not present. Page {1} was used least recently, swapping it out".format(
                    needed_page, memory[oldest])) if verbose == "yes" else None
                to_write += "\n" + "Page {0} not present. Page {1} was used least recently, swapping it out".format(
                    needed_page, memory[oldest])

                # actually swap out the oldest page from memory and insert needed page
                memory[oldest] = swap[needed_page]

            to_write += "\nmemory: " + print_list(memory) if verbose == "yes" else None
            print("stack: ", end='') if verbose == "yes" else None
            to_write += "\nstack: " + print_list(stack) if verbose == "yes" else None

        finally:
            # regardless if needed page was in memory or not
            # move needed page to top of stack
            try:
                stack.remove(needed_page)
                stack.append(needed_page)
            except ValueError:
                stack.append(needed_page)

            print() if verbose == "yes" else None
            to_write += "\n"

    with open("output_lru.csv", "a") as f:
        f.write(to_write)

    return page_fault_counter


if __name__ == "__main__":
    c = [5, 7, 5, 6, 7, 3, 3, 4, 5, 4, 8, 1, 2, 2, 5]
    print("Page faults:", lru(c, 3, 10, "yes"))
