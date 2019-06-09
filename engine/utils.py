import csv 

def readBaike(config_path, config_encoding):
    with open(config_path, encoding=config_encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        # for row in csv_reader:
            # if line_count == 0:
                # print(len(row))
            # print(row[0], row[1])
            # line_count += 1
        # print(line_count)
        return [row for row in csv_reader]


if __name__ == '__main__':
    readBaike("../data/baike.csv", "utf-8")