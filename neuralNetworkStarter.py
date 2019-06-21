import subprocess
import config
import os
from logger import Logger

class NeuralNetworkStarter:

    def __init__(self, step_size, output_dims, load):
        self.step_size = step_size
        self.output_dims = output_dims
        self.load = load

    def count_tf_records(self):

        return len(os.listdir(config.TFRECORDS_PATH))


    def run(self):
        logger = Logger()
        start_time = logger.get_current_timestamp()
        current_path = os.getcwd()
        os.chdir(config.NEURAL_NETWORK_PATH)
        network_start_command =  'python2.7 train.py --model i3d --inputDims 10 --outputDims %s' \
                                 ' --dataset youtube --load %s --expName %s --fName trainlist --seqLength 1' \
                                 ' --size 224 --train 1 --split 1 --wd 0.0 --lr %s --nEpochs 11' \
                                 ' --baseDataPath youtube --numVids %s' \
                                 ' --saveFreq 1 --dropoutRate 0.5 --gradClipValue 100.0 --batchSize 10'\
                                 % (self.output_dims, self.load, config.EXPERIMENT_NAME, self.step_size,
                                    self.count_tf_records())
        print(network_start_command)
        subprocess.run(network_start_command, shell=True)
        os.chdir(current_path)

        end_time = logger.get_current_timestamp()
        logger.log_network_training_time(start_time, end_time)