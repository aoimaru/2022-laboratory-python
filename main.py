

from libs.doc2vecs import D2V
from libs.handles import Handle
from libs.trs import TR

ROOT_FILE_PATH = "../0512-results/**/*.json"

def do():
    file_paths = Handle.get_file_path(ROOT_FILE_PATH)
    for file_path in file_paths:
        print(file_path)
    tr_datas = TR.create_tr_data(file_paths)
    D2V.create_model(tr_datas, name="apt-get-install")
    # from datetime import datetime
    # current_time = datetime.now()
    # current_time_str = current_time.strftime('%Y.%m.%d.%H.%M.%S')
    # print(current_time_str)
    # print(type(current_time_str))
    



def main():
    do()


if __name__ == "__main__":
    main()