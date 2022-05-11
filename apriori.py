import json
import pprint

import pandas as pd

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

FILE_PATH = "../RES-SUB/190111884:0.json"

def get_contents():
    with open(FILE_PATH, mode="r") as f:
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
    data = get_contents()
    src = data[target]
    src_command = get_src_command(src)
    sim_commands = get_sim_commands(src)
    commands = [src_command]+sim_commands
    return commands

def test():
    TARGET = "190111884:0:0"
    commands = get_commands(TARGET)
    # pprint.pprint(commands)

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


def main():
    test()




if __name__ == "__main__":
    main()