from linkGen import LinkGen
from downloader import Downloader
from segmenter import Segmenter
from neuralNetworkStarter import NeuralNetworkStarter
from neuralNetworkTester import NeuralNetworkTester
from remover import Remover
import subprocess
import config
import utils
from  datetime import datetime
from logger import Logger

input_file = open(config.CATEGORY_LIST, "r")
categories = input_file.read().splitlines()
input_file.close()

generator = LinkGen()
generator.run(categories)
downloader = Downloader(categories, config.BATCH_SIZE)
segmenter = Segmenter()
remover = Remover()
logger = Logger()
processed_video_count = utils.get_processed_video_count()

while processed_video_count < config.NUMBER_OF_LINKS:
    processed_video_count = utils.get_processed_video_count()
    load = utils.get_checkpoints_flag()

    downloader.run()

    segmenter.run()

    source = config.NEURAL_NETWORK_PATH

    tfrecords_command = 'python2.7 %s/utils/generate_tfrecords_dataset.py' \
                        ' --videos_dir %s --save_dir %s' % (config.NEURAL_NETWORK_PATH, config.PROCESSED_VIDEOS_PATH,
                                                            config.TFRECORDS_PATH)
    print(tfrecords_command + '\n')

    start_time = logger.get_current_timestamp()
    subprocess.run(tfrecords_command, shell=True)
    end_time = logger.get_current_timestamp()
    logger.log_tfrecords_generation_time(start_time, end_time)

    starter = NeuralNetworkStarter(config.LEARNING_RATE, len(categories), load)

    tester = NeuralNetworkTester(categories)
    starter.run()
    load = utils.set_checkpoints_flag("1")
    tester.run()
    remover.run()
    processed_video_count += config.BATCH_SIZE
    utils.set_processed_video_count(processed_video_count)

    if datetime.now() > config.PROGRAM_EXIT_TIME:
        break





