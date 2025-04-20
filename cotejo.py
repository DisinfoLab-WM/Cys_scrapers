from bs4 import BeautifulSoup
import requests
import sys
import datetime
import time
import json


def main(args):
    result=requests.get("https://cotejo.info/feed/")
    soup=BeautifulSoup(result.content.decode('utf-8'), "xml")
    items=soup.find_all("item")
    results=[]
    file = args[1]
    if len(args) == 2: # if no start date specified
        for item in items:
            date = ymd_from_date(item.find("pubDate"))
            add_to_results(results,item,date)
    else: # if start date specified
        file = args[3]
        for item in items:
            #print(item.find("pubDate"))
            date = ymd_from_date(item.find("pubDate"))
            
            if is_after(args[1]+" "+args[2], date): # stop when we get to before the start date
                break
            #print("here")
            add_to_results(results,item,date)
    
    
    to_dump = {"articles":{}}
    
    counter = 0
    
    for result in results:
        date_time = result[3].split(" ")
        date = date_time[0].split("-")
        time_ = date_time[1].split(":")
        unix_date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time_[0]), int(time_[1]), int(time_[2]))
        
        to_dump["articles"][str(counter)] = {"title":str(result[0]), "text":str(result[1]),"author":result[2],"date_published":str(result[3]),"unix_date_published":str(time.mktime(unix_date.timetuple())),"organization_country":"Venezuela", "site_name": "Cotejo", "url":str(result[4]), "language":"es"}
    
        #print(to_dump["articles"][str(counter)])
        counter += 1
    with open(file, "w") as json_file:
        json.dump(to_dump, json_file, indent=4)

def add_to_results(results, item, date):
    title = item.find("title").string
    link = item.find("link").string
    body = item.find("description")
    author = item.find("dc:creator").string
    
    results.append([title,body,author,date,link])

def ymd_from_date(date):
    #print(date)
    ymd=date.string.split(" ")
    day=ymd[1]
    month=ymd[2].lower()
    year=ymd[3]
    
    months = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    cur=0
    while months[cur]!=month:
        #print(month)
        cur+=1
    return "-".join([year,str(cur),day]) + " " + ymd[4]
    
def is_before(d1,d2):
    #print(d1)
    #print(d2)
    d1 = d1.split(" ")
    d2 = d2.split(" ")
    
    date1 = d1[0].split("-")
    date2 = d2[0].split("-")
    
    time1 = d1[1].split(":")
    time2 = d2[1].split(":")
    
    if date1[0]>date2[0]:
        return False
    elif date1[0]==date2[0]:
        if date1[1]>date2[1]:
            return False
        elif date1[1]==date2[1]:
            if date1[2]>date2[2]:
                return False
            elif time1[0]==time2[0]:
                if time1[1]>time2[1]:
                    return False
                elif time1[1]==time2[1]:
                    if time1[2]>time2[2]:
                        return False
    return True
    
def is_after(d1,d2):
    return is_before(d2,d1)

main(sys.argv)
