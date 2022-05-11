import json
import pprint
import sys

import pandas as pd

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

FILE_PATH = "../RES-SUB/DMPV/"

def get_contents(target):
    file_index, run_index, command_index = target.split(":")
    target_index = "{}:{}".format(file_index, run_index)
    with open(FILE_PATH+"{}.json".format(target_index), mode="r") as f:
        data = json.load(f)
    return data

def get_src_command(data):
    return data["src_command"]

def get_sim_commands(data):
    args = list()
    for command in data["similar_datas"]:
        args.append(command["sim_commands"])
    return args

def get_commands(target):
    data = get_contents(target)
    src = data[target]
    src_command = get_src_command(src)
    sim_commands = get_sim_commands(src)

    commands = [src_command]+sim_commands
    return commands

def to_json_file(commands, target):
    src_command = commands.pop(0)
    to_json = {
        "src_command": src_command,
        "dist_command": commands
    }
    TO_JSON_FILE = "../APRIORI/DMPV/DataJson/"
    with open(TO_JSON_FILE+"{}.json".format(target), mode="w") as f:
        json.dump(to_json, f, ensure_ascii=False, indent=4)

def to_dataframe_file(freq_items, target):
    TO_DATAFRAME_FILE = "../APRIORI/DMPV/DataFrame/"
    file_path = TO_DATAFRAME_FILE+"{}.csv".format(target)
    freq_items.to_csv(file_path)

def test(target):
    # TARGET = "190111884:1:0"
    commands = get_commands(target)
    to_json_file(commands, target)

    # データをテーブル形式に加工
    te       = TransactionEncoder()
    te_array = te.fit(commands).transform(commands)
    df       = pd.DataFrame(te_array, columns=te.columns_)
    freq_items = apriori(df,                     # データフレーム
                     min_support  = 0.01,    # 支持度(support)の最小値
                     use_colnames = True,    # 出力値のカラムに購入商品名を表示
                     max_len      = None,    # 生成されるitemsetsの個数
                     verbose = 0,            # low_memory=Trueの場合のイテレーション数
                     low_memory = False,     # メモリ制限あり＆大規模なデータセット利用時に有効
                    )
    freq_items = freq_items.sort_values("support", ascending = False).reset_index(drop=True)
    print(freq_items[:50])
    to_dataframe_file(freq_items, target)


def main(args):
    test(args[1])


def main(args):
    test(args[1])




if __name__ == "__main__":
    main(sys.argv)