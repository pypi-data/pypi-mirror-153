
import os


class FirmwareBinPath(object):

    def __init__(self):
        self.linux_path = "/home/share/sqa/FW_Release/redtail"
        self.windows_path = r"\\172.29.190.4\share\sqa\FW_Release\redtail"
        self.auto_build_folder = "nightly"

    def search_auto_build_firmware_folder(self, commit):
        auto_build_path = os.path.join(self.windows_path, self.auto_build_folder)
        bin_folder = None
        for item in os.listdir(auto_build_path):
            item_path = os.path.join(auto_build_path, item)
            if os.path.isdir(item_path):
                if commit in item_path:
                    bin_folder = item
                    break
        return bin_folder

    def search_firmware_file(self, bin_path, commit, volume, nand):
        bin_file = None
        for item in os.listdir(bin_path):
            item_path = os.path.join(bin_path, item)
            if os.path.isfile(item_path):
                if "preBootloader" not in item:
                    if "_{}_".format(volume.lower()) in item.lower():
                        if item.endswith(".bin"):
                            if volume.lower() == "all" or "_{}_".format(nand.lower()) in item.lower():
                                bin_file = item
                                break
        return bin_file

    def get_image_path(self, base_path, volume, commit_id, nand):
        nand = "ALL" if volume.lower() == "all" else nand
        _files = os.listdir(base_path)
        if os.path.exists(base_path):
            for item in _files:
                item_path = os.path.join(base_path, item)
                if os.path.isdir(item_path):
                    ret = self.get_image_path(item_path, volume, commit_id, nand)
                    if ret is not None:
                        return ret
                elif ("_{}_".format(volume) in item) and (commit_id in item) and ("preBootloader" not in item) and \
                        item.endswith(".bin") and ("_{}_".format(nand) in item):
                    return os.path.join(base_path, item)

    def get_auto_build_fw_path(self, commit, volume, nand):
        volume = "ALL" if volume == "" else volume
        linux_path,  windows_path = None, None
        bin_folder = self.search_auto_build_firmware_folder(commit)
        if bin_folder is not None:
            bin_path = os.path.join(self.windows_path, self.auto_build_folder, bin_folder)
            bin_file = self.search_firmware_file(bin_path, commit, volume, nand)
            if bin_file is not None:
                linux_path = "{}/{}/{}/{}".format(self.linux_path, self.auto_build_folder, bin_folder, bin_file)
                windows_path = os.path.join(self.windows_path, self.auto_build_folder, bin_folder, bin_file)
        return windows_path, linux_path
    #
    # def get_related_fw_path(self, base_path, commit, volume, nand="BICS4"):
    #     fw_path = None
    #     fw_file = self.search_firmware_file(base_path, commit, volume, nand)
    #     if fw_file is not None:
    #         fw_path = os.path.join(base_path, fw_file)
    #     return fw_path

