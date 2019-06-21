import time
import datetime
import config
import os


class Logger:

    def log_video_download_time(self, start, end):
        duration = end - start
        size = self.get_size(config.BAKALAURAS_PATH + '/' + config.VIDEOS_FOLDER)
        fd = open(config.LOG_FILE_PATH + '/download_time.csv', 'a')
        fd.write("%s,%s,%s,%s\n" %(self.convert_timestamp(start), self.convert_timestamp(end), duration, size)) #format for csv
        fd.close()

    def log_video_segmentation_time(self, start, end):
        duration = end - start
        size = self.get_size(config.BAKALAURAS_PATH + '/' + config.PROCESSED_VIDEOS_PATH)
        fd = open(config.LOG_FILE_PATH + '/segment_time.csv', 'a')
        fd.write("%s,%s,%s,%s\n" %(self.convert_timestamp(start), self.convert_timestamp(end), duration, size)) #format for csv
        fd.close()

    def log_tfrecords_generation_time(self, start, end):
        duration = end - start
        size = self.get_size(config.TFRECORDS_PATH)
        fd = open(config.LOG_FILE_PATH + '/tfrecords_time.csv', 'a')
        fd.write("%s,%s,%s,%s\n" %(self.convert_timestamp(start), self.convert_timestamp(end), duration, size)) #format for csv
        fd.close()

    def log_network_training_time(self, start, end):
        duration = end - start
        fd = open(config.LOG_FILE_PATH + '/training_time.csv', 'a')
        fd.write("%s,%s,%s\n" %(self.convert_timestamp(start), self.convert_timestamp(end), duration)) #format for csv
        fd.close()

    def get_size(self, start_path='.'): #bytes
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def convert_timestamp(self, timestamp):
        st = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        return st

    def get_current_timestamp(self):
        ts = time.time()
        return ts
