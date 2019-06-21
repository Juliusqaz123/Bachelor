import os, subprocess, shutil
import config
from logger import Logger

class Segmenter:


    def run(self):
        logger = Logger()
        start_time = logger.get_current_timestamp()
        processed_videos = 'processed_videos'
        if os.path.exists(processed_videos):
            shutil.rmtree(processed_videos)
        os.mkdir(processed_videos)
        videos_folder = os.listdir(config.VIDEOS_FOLDER)

        for folder in videos_folder:
            cur = os.getcwd()
            os.chdir(config.PROCESSED_VIDEOS_PATH)
            os.mkdir(folder.lower())
            os.chdir(cur)

            folder_relative_path= os.path.join(config.VIDEOS_FOLDER, folder)
            videos = os.listdir(folder_relative_path)
            for video in videos:
                video_absolute_path = os.path.join(config.BAKALAURAS_PATH,folder_relative_path,video)
                video_name = video[0:video.find('.')] + '%03d' + video[video.find('.'):]
                print(video_name)
                destination_absolute_path = os.path.join(config.BAKALAURAS_PATH,
                                                         config.PROCESSED_VIDEOS_PATH, folder.lower(), video_name)
                cmd_command = 'ffmpeg -i  %s -c copy -map 0 -segment_time 00:00:05 -f segment -reset_timestamps 1 %s'\
                              %(video_absolute_path, destination_absolute_path)
                print(cmd_command)
                subprocess.run(cmd_command, shell=True)


        end_time = logger.get_current_timestamp()
        logger.log_video_segmentation_time(start_time, end_time)