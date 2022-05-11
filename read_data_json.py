import sys
import json


def test(file_path):
    with open(file_path, mode="r") as f:
        data = json.load(f)
    src_command = data["src_command"]
    print(src_command)
    dist_commands = data["dist_command"]
    for dist_command in dist_commands:
        print(dist_command)
    

def main(args):
    file_path = args[1]
    test(file_path)




if __name__ == "__main__":
    main(sys.argv)