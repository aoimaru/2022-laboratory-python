import os
import json

from libs.handles import Handle

def patch_file_path(file_path):
    file_path = os.path.basename(file_path)
    file_path = file_path.replace(".json", "")
    return file_path

class TR(object):
    @staticmethod
    def create_tr_data(file_paths):
        tr_datas = dict()
        for file_path in file_paths:
            data = Handle.get_contents(file_path)
            results = data["Results"]
            file_path = patch_file_path(file_path)
            if not results:
                continue
            for hg, result in enumerate(results):
                commands = Handle.get_commands(result["Res"])
                if not commands:
                    continue
                for wd, command in enumerate(commands):
                    tr_data = {
                        "{}:{}:{}".format(file_path, hg, wd): command
                    }
                    tr_datas.update(tr_data)
        
        return tr_datas
    
    @staticmethod
    def create_tr_data_to_json_file(file_paths):
        for file_path in file_paths:
            data = Handle.get_contents(file_path)
            results = data["Results"]
            file_path = patch_file_path(file_path)
            tr_datas = {}
            if not results:
                continue
            for hg, result in enumerate(results):
                commands = Handle.get_commands(result["Res"])
                if not commands:
                    continue
                for wd, command in enumerate(commands):
                    tr_data = {
                        "{}:{}:{}".format(file_path, hg, wd): command
                    }
                    tr_datas.update(tr_data)
            print(tr_datas)
            # ファイルパスはパッチ
            TO_FILE_PATH = "JSON"
            with open("{}/{}.json".format(TO_FILE_PATH, file_path), mode="w") as f:
                json.dump(tr_datas, f, ensure_ascii=False)
    
    @staticmethod
