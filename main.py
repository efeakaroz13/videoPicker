##
# Author: Efe Akaroz
# Written@2nd of november 2023
# Note : you have the right to change, redistrubute and use freely. GNU is better than UNIX 
##

import random
import json
import requests
from bs4 import BeautifulSoup



class VideoPicker:
    def __init__(self):
        self.data = {
            "channels":["UCHdPuKshPHyRHE3rz75rXdw"],#Only channel ids
            "history":[],
            "downloads":"downloads",#The folder for downloads
            "interests":["science","software","physics","documentary","energy generation","photography","history","political ideas","debate","self improvement","time management","economics","stock market"],
            "mode":"interests", #subscriptions or interests
            "openAIAPIkey":"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"    
        }
        try:
            data= open("data.json","r").read()
            self.data= json.loads(data)
        except:
            open("data.json","w").write(json.dumps(self.data,indent=4))

    def selectChannel(self):

        channel = random.choice(self.data["channels"])
        page  = requests.get("https://yewtu.be/channel/"+channel,headers={"User-Agent":"Mozilla firefox"})
        
        soup = BeautifulSoup(page.content,"html.parser")

        channelMetadata = {

            "image":"https://yewtu.be"+soup.find_all("div",{"class":"channel-profile"})[0].find("img").get("src"),
            "name":soup.find_all("div",{"class":"channel-profile"})[0].find("span").get_text()
        }
        videos = []

        for h in soup.find_all("div",{"class":"h-box"}):
            try:
                videoCardRow = h.find_all("div",{"class":"video-card-row"})[0].find("a")
                title = videoCardRow.get_text()
                href = videoCardRow.get("href")
                duration = int(h.find("p",{"class":"length"}).get_text().split(":")[0])
                if duration >=10:
                    videos.append({"title":title,"href":href,"duration":duration})


                #get the channel video metadata and organize them under the channel metadata attribute.
                #Makes us able to filter shorter videos. Ideal for increased attention span
                #You are welcome.



            except Exception as e:
                pass

        channelMetadata["videos"] = videos

        self.channel = channelMetadata
        return self.channel
    def selectVideo(self):
        #Selecting a random video from the randomly selected youtube channel.
        try:
            videos = self.channel["videos"]
        except:
            raise TypeError("You need to use select channel first in order to select video")
        selected = random.choice(videos)

        return selected

    def downloadVideo(self):
        #Analyse the json in html content,
        #get HMAC key and put it to the /latest_version?id=1EHUoAEJmYg&itag=22&hmac_key=74c8f489f422fce7ef8cd9a8e2936fdb5119d98f
        #URL with id.
        #It gives the MP4 Video file. Also compressed.

if __name__ == "__main__":
    picker =  VideoPicker()
    channel = picker.selectChannel()
    video = picker.selectVideo()
    print(json.dumps(video,indent=4))



