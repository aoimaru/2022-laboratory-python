import sys
import json

from gensim.models.doc2vec import Doc2Vec

def main(args):
    model = Doc2Vec.load("./model/2022.05.11.14.06.55:pv-dbow.model")
    items = model.docvecs.most_similar(args[1], topn=20)
    index_name = args[1]
    index_names = index_name.split(":")
    file_name = index_names[0]
    with open("../JSON-SUB/{}.json".format(file_name), mode="r") as f:
        data = json.load(f)
    
    print("src:", data[args[1]])
    print(model.docvecs[args[1]])
    print(type(model.docvecs[args[1]]))

    for cnt, item in enumerate(items):
        print(item)
        file_name = item[0].split(":")[0]
        with open("../JSON-SUB/{}.json".format(file_name), mode="r") as f:
            data = json.load(f)
        print(cnt, ": ", item[1])
        print(item[0], ": " ,data[item[0]])


if __name__ == "__main__":
    main(sys.argv)