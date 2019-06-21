import os
from datetime import datetime

MAX_VIDEO_LEN = 1200
CATEGORY_LIST = "categories.txt"
BATCH_SIZE = 1
NUMBER_OF_LINKS = 100
VIDEOS_FOLDER = "videos"
LINKS_FOLDER = "categories"
LOG_FOLDER = 'logs'
DESKTOP_PATH = '/home/julius/Desktop'
KURSINIS_PATH = DESKTOP_PATH + '/Kursinis'
BAKALAURAS_PATH = os.getcwd()
NEURAL_NETWORK_PATH = KURSINIS_PATH + "/M-PACT"
LOG_FILE_PATH = BAKALAURAS_PATH + '/' + LOG_FOLDER
PREDICTIONS_LOG_FOLDER = LOG_FILE_PATH + '/predictions'
PROCESSED_VIDEOS_PATH = 'processed_videos'
TFRECORDS_PATH = NEURAL_NETWORK_PATH + '/youtube/tfrecords_youtube/Split1/trainlist'
TEST_LIST_PATH = NEURAL_NETWORK_PATH + '/youtube/tfrecords_youtube/Split1/testlist'
LEARNING_RATE = 0.01
EXPERIMENT_NAME = "I3D_Youtube_Default4"
UCF_PATH = NEURAL_NETWORK_PATH + "/UCF-101-unprocessed"
TEST_VIDEO_PATH = BAKALAURAS_PATH + "/test_videos"
TEST_LOG_PATH = NEURAL_NETWORK_PATH + "/test_log"
LINK_FLAG_FILE = 'link_flag.txt'
LOAD_CHECKPOINTS_FILE = "load_checkpoints.txt"
PROCESSED_VIDEO_COUNT_FILE = "video_count.txt"
USED_LINKS = BAKALAURAS_PATH + "/used_links"
PROGRAM_EXIT_TIME = datetime(2019, 5, 21, 8, 58)
