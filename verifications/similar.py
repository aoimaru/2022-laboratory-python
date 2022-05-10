import sys
import json

from gensim.models.doc2vec import Doc2Vec



def main(args):
    model = Doc2Vec.load("./model/2022.05.10.01.03.50:apt-get-install.model")
    file_path, commands, _ = args[1].split(":")
    with open("../JSON/{}.json".format(file_path), mode="r") as f:
        data = json.load(f)
    
    print(data[args[1]])
    tag = "{}:{}".format(file_path, commands)
    tag_keys = list()
    for cnt, key in enumerate(data.keys()):
        print()
        key_cnt = key.split(":")[-1]
        if key.startswith(tag):
            print(data[key])
            items = model.docvecs.most_similar(key, topn=10)
            for item in items:
                item_cnt = item[0].split(":")[-1]
                if key_cnt == item_cnt:
                    print(item)
    


if __name__ == "__main__":
    main(sys.argv)