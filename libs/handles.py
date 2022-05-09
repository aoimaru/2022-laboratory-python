import glob
import json

class Handle(object):
    @staticmethod
    def get_file_path(root: str):
        return glob.glob(root, recursive=True)

    @staticmethod
    def get_contents(file_path: str):
        with open(file_path, mode="r") as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def get_commands(tokens):
        if not tokens:
            return []
        commands = []
        command = []
        _ = tokens.pop(0)
        while tokens:
            token = tokens.pop(0)
            if not token:
                continue
            if token == "AND":
                if command:
                    commands.append(command)
                command = []
            else:
                command.append(token)

        return commands
