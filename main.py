

from libs.doc2vecs import D2V
from libs.handles import Handle
from libs.trs import TR

"""
    環境ごとに書き換える $HOME配下
"""
ROOT_FILE_PATH = "../0512-results/**/*.json"

def create_model():
    file_paths = Handle.get_file_path(ROOT_FILE_PATH)
    tr_datas = TR.create_tr_data(file_paths)
    D2V.create_model(tr_datas, name="apt-get-install")
    
def create_index():
    file_paths = Handle.get_file_path(ROOT_FILE_PATH)
    tr_datas = TR.create_tr_data_to_json_file(file_paths)


def main():
    create_index()


if __name__ == "__main__":
    main()