import requests
import urllib3
urllib3.disable_warnings()


class Brikeda:
    def __init__(self,url,key,robot=""):
        self.url=url
        self.key=key
        self.robot =robot
        print(f'Robot {self.robot} is initialized')

    def WeatherForecast(self):
        furl=self.url + "/api/AI/Weather"
       # print(furl)
        response = requests.get(furl, verify=False)
        print(response.content)
    def SyncMessages(self,message):
        newurl=self.url + '/api/AI/message'
        print(newurl)     
        response = requests.post(newurl, json ={"key": self.key,  "message": message}, verify=False)
        print(response.content)
    def TestIt(self,message):
        print(f"you said: {message}" )
    def Sentiment(self,text):
        furl=self.url + "/api/AI/Sentiment"
        response = requests.post(furl, json ={"key": self.key,  "text": text}, verify=False)
        json = response.json() 
        sentiment_data=json['data']
        return sentiment_data
