
import os
import yaml


class StatusFile(object):
    """
    Save the latest test case status
    """
    file_path = os.path.join(os.path.dirname(__file__), "..", "prun_status.yaml")

    def __init__(self):
        pass

    @staticmethod
    def save_test(test):
        with open(StatusFile.file_path, "w") as f:
            yaml.dump(test, f)

    @staticmethod
    def read():
        test = None
        if os.path.exists(StatusFile.file_path):
            with open(StatusFile.file_path, "r") as f:
                str_test = f.read()
                test = yaml.load(stream=str_test, Loader=yaml.FullLoader)
        return test



