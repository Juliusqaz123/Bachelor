import urllib.request
from bs4 import BeautifulSoup
import sys
import config
import os
import shutil
import re
from tqdm import tqdm
import utils

class LinkGen:

    numberOfLinks = config.NUMBER_OF_LINKS * 2
    durationLimit = config.MAX_VIDEO_LEN
    categoryList = config.CATEGORY_LIST

    youtubeUrl = "https://www.youtube.com"
    base = youtubeUrl + "/results?search_query=allintitle%3A"
    page = "&page="
    count = 1
    linkList = []
    listIsFull = False

    def run(self, categories):

        link_flag = self.get_link_flag()
        if link_flag == "0":
            print("Skipping link generation\n")
            return

        print("Generating links\n")

        cwd = os.getcwd()
        download_path = cwd + '/' + config.LINKS_FOLDER

        if os.path.exists(download_path):
            shutil.rmtree(download_path)
        os.makedirs(download_path)

        for category in tqdm(categories):

            self.generate_links(category)
            self.count = 1
            self.write_to_file(utils.get_camel_case_name(category))
            self.linkList.clear()
            self.listIsFull = False

        self.set_link_flag("0")

    def generate_links(self, category):
        query = re.sub("([A-Z])"," \g<0>", category)
        query = query.replace(' ', '+')
        while not self.listIsFull:
            url = self.base + query + self.page + str(self.count)
            print(url)
            req = urllib.request.Request(url, headers={"Accept-Language": "en-US,en;q=0.5"})
            response = urllib.request.urlopen(req)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            videoInfoList = self.parse_info_from_html(soup)

            if videoInfoList[0]['id'].startswith("http://googleadservice.com"):
                videoInfoList.remove(0)
            for videoInfoDict in videoInfoList:
                if videoInfoDict['duration'] > self.durationLimit:
                    continue

                videoUrl = self.youtubeUrl + videoInfoDict['id']

                if self.is_music_video(videoUrl) or self.is_link_used(videoUrl, category):
                    continue

                self.linkList.append(videoUrl)

                if len(self.linkList) == self.numberOfLinks:
                    self.listIsFull = True
                    break

            self.count += 1

    def is_music_video(self, url):
        req = urllib.request.Request(url, headers={"Accept-Language": "en-US,en;q=0.5"})
        response = urllib.request.urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        results = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['yt-uix-sessionlink'])
        is_music = False
        for result in results:
            is_music = "https://play.google.com/music" in result['href']
            if is_music:
                break
        return is_music

    def is_link_used(self, url, category):
        link_file = config.USED_LINKS + '/' + utils.get_camel_case_name(category) + '.txt'

        if os.path.exists(link_file):
            file = open(link_file, 'r')
            links = file.read().splitlines()
            file.close()

            if url in links:
                return True
            else:
                return False
        else:
            return False


    def parse_info_from_html(self, html):
        videoHtmlTags = list(html.findAll('h3', {'class', 'yt-lockup-title'}))

        videoInfoList = []
        for tag in videoHtmlTags:
            tagContents = tag.contents

            if len(tagContents) != 2:
                continue

            id = tagContents[0]['href']
            if not id.startswith("/watch"):
                continue

            durationInSeconds = self.format_duration(tagContents[1])
            dict = {'id': id, 'duration': durationInSeconds}
            videoInfoList.append(dict)

        return videoInfoList



    def write_to_file(self, fileName):
        outputFile = open(config.LINKS_FOLDER + '/' + fileName + ".txt", "w")
        for link in self.linkList:
            outputFile.write(link + '\n')

    def format_duration(self, durationTag):
        durationString = durationTag.text
        prefix = " - Duration: "
        if not str(durationString).startswith(prefix):
            return sys.maxsize

        parsedDuration = durationString[len(prefix):len(durationString)-1]
        timeList = list(map(int, parsedDuration.split(":")))
        multipliers = [3600, 60, 1]
        durationInSecond = 0
        for i in range(0, len(timeList)):
            durationInSecond += timeList[i] * multipliers[len(multipliers) - len(timeList) + i]

        return durationInSecond

    def get_link_flag(self):
        link_flag_file = open(config.LINK_FLAG_FILE, "r")
        value = link_flag_file.read().splitlines()[0]
        link_flag_file.close()

        return value

    def set_link_flag(self, new_value):
        link_flag_file = open(config.LINK_FLAG_FILE, "w")
        link_flag_file.write(new_value)
        link_flag_file.close()

