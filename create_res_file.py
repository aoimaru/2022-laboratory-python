import sys
import json
import pprint

from gensim.models.doc2vec import Doc2Vec

model = Doc2Vec.load("./model/2022.05.11.14.06.55:pv-dbow.model")

def get_src_datas(file_name):
    with open("../JSON-SUB/{}.json".format(file_name), mode="r") as f:
        data = json.load(f)
    command_keys = [command_key for command_key in data.keys()]
    src_data = dict()
    for command_key in command_keys:
        file_index, command_index, run_index = command_key.split(":")
        run_key = "{}:{}".format(file_index, command_index)
        if not run_key in src_data:
            src_data[run_key] = list()
        run_data = {
            "command_key": command_key,
            "command_value": data[command_key]
        }
        src_data[run_key].append(run_data)

    return src_data


def get_similars(contents):
    dist_data = dict()
    for content in contents:
        if not content["command_key"] in dist_data:
            dist_data[content["command_key"]] = list()
        similars = model.docvecs.most_similar(content["command_key"], topn=10)
        similar_datas = list()
        for similar in similars:
            command_key = similar[0]
            file_name = command_key.split(":")[0]
            with open("../JSON-SUB/{}.json".format(file_name), mode="r") as f:
                similar_contents = json.load(f)
            similar_data = {
                "sim_commands": similar_contents[command_key],
                "sim_value": similar[1]
            }
            similar_datas.append(similar_data)
        dist_val = {
            "src_command": content["command_value"],
            "similar_datas": similar_datas
        }
        dist_data[content["command_key"]] = dist_val
    return dist_data
    

def to_json_file(file_name):
    TO_FILE_PATH = "../RES-SUB"
    src_datas = get_src_datas(file_name)
    for file_path, file_contents in src_datas.items():
        print(file_path)
        dist_data = get_similars(file_contents)
        with open("{}/{}.json".format(TO_FILE_PATH, file_path), mode="w") as f:
            json.dump(dist_data, f, ensure_ascii=False)


def main(args):
    to_json_file(args[1])
    

    
    


if __name__ == "__main__":
    main(sys.argv)