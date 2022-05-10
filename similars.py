import json
import sys
import pprint

ROOT_FILE_PATH = "RES"

def test(file_path):
    with open("{}/{}.json".format(ROOT_FILE_PATH, file_path), mode= "r") as f:
        data = json.load(f)
    
    for value in data.values():
        print()
        src_command = value["src_command"]
        print("src_command: ", src_command)
        for sim_data in value["similar_datas"]:
            print(sim_data)
        print()
    
    for value in data.values():
        print(value["src_command"])



def main(args):
    test(args[1])


if __name__ == "__main__":
    main(sys.argv)