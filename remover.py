import shutil
import os
import config


class Remover:

    def run(self):
        folders = self.get_folders()
        for folder in folders:
            self.remove_from(folder)

    def get_folders(self):
        folder_list =  []
        folder_list.append(config.VIDEOS_FOLDER)
        folder_list.append(config.TFRECORDS_PATH)
        folder_list.append(config.PROCESSED_VIDEOS_PATH)
        return folder_list

    def remove_from(self, folder):
        shutil.rmtree(folder)
        os.makedirs(folder)