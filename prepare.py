from random import randint


# prepares 'chains' amount of 'length' long random reference chains
# writes them to input.csv
def prepare(length=100, pages=20, chains=100):
    with open("input.csv", "w") as f:
        # for every chain
        for _ in range(chains):
            to_write = ""
            # write a line containing references
            for i in range(length):
                # if it is the last reference in current chain
                if i == length - 1:
                    # do not put a tab at the end
                    to_write += "{0}".format(randint(0, pages - 1))
                    continue
                else:
                    to_write += "{0}\t".format(randint(0, pages - 1))

            to_write += "\n"
            f.write(to_write)


if __name__ == "__main__":
    prepare(length=20, pages=20, chains=30)
