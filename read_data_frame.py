import pandas as pd
import sys

def read_csv(file_path):
    freq_items = pd.read_csv(file_path)
    print(freq_items[:30])


def test(file_path):
    read_csv(file_path)



def main(args):
    test(args[1])


if __name__ == "__main__":
    main(sys.argv)