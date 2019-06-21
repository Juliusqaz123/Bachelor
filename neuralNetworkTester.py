import os
import subprocess
import config
import shutil
import utils
import time
import numpy as np
from logger import Logger

class NeuralNetworkTester:

    def __init__(self, categories):
        self.categories = categories


    def run(self):
        self.generate_tfrecords()

        current_path = os.getcwd()
        os.chdir(config.NEURAL_NETWORK_PATH)
        log_folder_name = ("exp_test_%s_%s" % (time.strftime("%d_%m_%H_%M"), config.EXPERIMENT_NAME))
        metrics_dir = os.path.join(config.TEST_LOG_PATH, log_folder_name)

        network_test_command = 'python2.7 test.py --model i3d --numGpus 1 --dataset youtube --loadedDataset youtube' \
                               ' --train 0 --load 1 --inputDims 10 --outputDims %s --seqLength 1 --size 224' \
                               ' --expName %s --numVids 200 --split 1 --baseDataPath youtube --metricsDir %s' \
                               ' --fName testlist --verbose 1' % (len(self.categories), config.EXPERIMENT_NAME, metrics_dir)
        subprocess.run(network_test_command,shell=True)

        if os.path.exists(metrics_dir):
            self.calculate_predictions(metrics_dir)

        os.chdir(current_path)

    def generate_tfrecords(self):
        n_records = 60

        print("Copying videos for testing")

        if not os.path.exists(config.TEST_VIDEO_PATH):
            os.mkdir(config.TEST_VIDEO_PATH)

        if len(os.listdir(config.TEST_VIDEO_PATH)) == 0:
            for category in self.categories:

                category_path = os.path.join(config.UCF_PATH, utils.get_camel_case_name(category))
                if not os.path.exists(category_path):
                    print("Category \"{}\" not found in {}".format(utils.get_camel_case_name(category), category_path))
                    continue

                os.mkdir(os.path.join(config.TEST_VIDEO_PATH, category.replace(' ', '')))

                test_videos = os.listdir(category_path)
                n_records = len(test_videos) if len(test_videos) < n_records else n_records

                for i in range(n_records):
                    shutil.copy(os.path.join(category_path, test_videos[i]), os.path.join(config.TEST_VIDEO_PATH, category.replace(' ', '')))

            tfrecords_command = 'python2.7 %s/utils/generate_tfrecords_dataset.py' \
                                ' --videos_dir %s --save_dir %s' % (
                                config.NEURAL_NETWORK_PATH, config.TEST_VIDEO_PATH,
                                config.TEST_LIST_PATH)

            if not os.path.exists(config.TEST_LIST_PATH):
                os.mkdir(config.TEST_LIST_PATH)

            if not len(os.listdir(config.TEST_LIST_PATH)) == 0:
                print("Removing old tfrecords from testlist")
                shutil.rmtree(config.TEST_LIST_PATH)
                os.makedirs(config.TEST_LIST_PATH)

            print("Generating tfrecords for testing")
            print(tfrecords_command + '\n')
            subprocess.run(tfrecords_command, shell=True)

        else:
            print(config.TEST_VIDEO_PATH + " is not empty, finishing...")

    def calculate_predictions(self, path):
        predictions_file = "test_predictions_youtube_avg_pooling.npy"
        data = np.load(path + '/' + predictions_file)
        good_pred = 0
        count = 1
        pred_dict = {}

        for i in range(1, len(data)):
            if data[i - 1][0] == data[i - 1][1]:
                good_pred += 1

            if data[i - 1][1] != data[i][1]:
                category = data[i - 1][2].split('_')[0]
                pred_dict[category] = float(good_pred) / count
                good_pred = 0
                count = 0

            count += 1

        if data[-1][0] == data[-1][1]:
            good_pred += 1

        category = data[-1][2].split('_')[0]
        pred_dict[category] = float(good_pred) / (count - 1)

        if not os.path.exists(config.PREDICTIONS_LOG_FOLDER):
            os.makedirs(config.PREDICTIONS_LOG_FOLDER)

        logger = Logger()
        for key in pred_dict:
            start = logger.get_current_timestamp()
            fd = open(config.PREDICTIONS_LOG_FOLDER + '/' + key + '.csv', 'a')
            fd.write("%s,%s\n" % (logger.convert_timestamp(start), pred_dict[key]))  # format for csv
            fd.close()

        start = logger.get_current_timestamp()
        fd = open(config.PREDICTIONS_LOG_FOLDER + '/total' + '.csv', 'a')
        fd.write("%s,%s\n" % (logger.convert_timestamp(start), (sum(pred_dict.values()) / len(pred_dict))))  # format for csv
        fd.close()

