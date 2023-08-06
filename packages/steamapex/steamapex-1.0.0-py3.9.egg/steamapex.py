import subprocess as sp
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import csv

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        return ""

def getGamesList(steamHTMLText):

    gameList = []
    soup = BeautifulSoup(steamHTMLText)
    gameTr = soup.find_all("tr",{"class":"player_count_row"})
    for tr in gameTr:
        singleGameData=[]
        for span in tr.find_all("span",{"class":"currentServers"}):
            singleGameData.append(span.string)
        for a in tr.find_all("a",{"class":"gameLink"}):
            singleGameData.append(a.string)
        gameList.append(singleGameData)
    return gameList

def printList(gameList):

    print("TOP10","CURRENT PLAYERS","PEAK TODAY","NAME")
    for i in range(10):
        g = gameList[i]
        print(i+1,g[0],g[1],g[2])

if __name__ == '__main__':
    url = "https://store.steampowered.com/stats/"
    steamHTMLText = getHTMLText(url)
    gameList = getGamesList(steamHTMLText)

    printList(gameList)
