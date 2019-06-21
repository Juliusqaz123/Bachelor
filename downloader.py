from __future__ import unicode_literals
import os
import shutil
import youtube_dl
import config
from tqdm import tqdm
from logger import Logger
import utils

class Downloader:

    def __init__(self, categories, batch_size):
        self.categories = categories
        self.batch_size = batch_size
        self.empty_link_list = False

    def run(self):
        logger = Logger()
        start_time = logger.get_current_timestamp()
        for category in self.categories:
            print("Downloading videos for: {}".format(category))
            self.download(category)
        end_time = logger.get_current_timestamp()
        logger.log_video_download_time(start_time, end_time)

    def download(self, category):

        cwd = os.getcwd()
        download_path = cwd + '/' + config.VIDEOS_FOLDER + '/' + utils.get_camel_case_name(category)

        if os.path.exists(download_path):
            shutil.rmtree(download_path)
        os.makedirs(download_path)
        while(len(os.listdir(download_path)) != self.batch_size):
            filtered_urls = self.get_urls(category, self.batch_size- len(os.listdir(download_path)))
            if len(filtered_urls) == 0:
                break
            self.download_batch(filtered_urls,download_path,category)



    def download_batch(self, filtered_urls, download_path, category):
        for idx, url in enumerate(tqdm(filtered_urls)):

            self.add_url_to_used_list(url, category)
            print("Download link for {}: {}".format(category, url))

            ydl_opts = {
                'outtmpl': '{0}/{1}{2}.%(ext)s'.format(download_path, utils.get_camel_case_name(category), idx),
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True,
                'include_ads': False,
                'format': '219/278/worstvideo/worst',
                'progress_hooks': [self.removeUrl]
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

    def get_urls(self, category, size):
        links = open(config.LINKS_FOLDER + '/' + utils.get_camel_case_name(category) + ".txt", "r+")
        urls = links.readlines()

        if self.batch_size > len(urls):
            filtered_urls = urls
        else:
            filtered_urls = urls[0:size]
        links.close()
        return filtered_urls

    def add_url_to_used_list(self, url, category):
        if not os.path.exists(config.USED_LINKS):
            os.makedirs(config.USED_LINKS)

        file_name = utils.get_camel_case_name(category) + ".txt"
        file = open(config.USED_LINKS + '/' + file_name, "a")
        file.write(url)
        file.close()

    def removeUrl(self, dict):
        if dict['status'] == 'finished':
            fileDir = dict['filename']
            files = fileDir.split('/')
            category = files[-2]
            cwd = os.getcwd()
            file = cwd + '/' + config.LINKS_FOLDER + '/' + category + '.txt'

            links = open(file, "r")
            lines = links.readlines()

            lines.pop(0)
            if len(lines) == 0:
                self.empty_link_list = True
            links.close()
            print(lines)
            outputFile = open(file, "w")
            for line in lines:
                outputFile.write(line)
            outputFile.close()
