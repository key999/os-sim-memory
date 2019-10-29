import csv


# loads data from input.csv, translates to a list
# then returns it
def load(file="input.csv"):
    chain = []

    try:
        with open(file, "r") as f:
            csv_read = csv.reader(f, delimiter='\t')
            # csv_read contains 'lines' amount of lists with data
            for i in csv_read:
                # append every line to chain
                chain.append(i)
    except FileNotFoundError as e:
        print(e)
        exit(3)

    # since csv read the file as list of lists of strings
    # there is a need to convert them to ints
    for i in chain:
        for j in range(len(i)):
            x = int(i[j])
            i[j] = x

    return chain


if __name__ == "__main__":
    print(load("input.csv"))
