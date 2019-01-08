from bs4 import BeautifulSoup
import urllib
from threading import Thread
import time

users = []

def parseEntry(entryNumber = 0):
    try:  
        fp = urllib.request.urlopen("https://eksisozluk.com/entry/" + str(entryNumber))
        mybytes = fp.read()
        
        html_doc = mybytes.decode("utf8")
        fp.close()
        
        soup = BeautifulSoup(html_doc, 'html.parser')
        
        content = soup.find(attrs = {"class": "content"}).get_text()
        title = soup.find(attrs = {"id" : "title"})["data-title"]
        author = soup.find(attrs = {"class": "entry-author"}).get_text()
        date = soup.find(attrs = {"class": "entry-date"}).get_text()
        
        return [title, author, content.strip(), date]
    except urllib.error.HTTPError as err:
        if err.code == 503:
            return parseEntry(entryNumber)
        return None

def parser(index):
    f_entry = open("entryler.csv", 'a')
    f_user = open("kullanicilar.csv", 'a')
    #f_entry.writelines(["id|yazar|içerik|zaman\n"])
    #f_user.writelines(["yazar"])
    global users
    finish = 86200000
    hundred_count = 0
    count = index + 1
    while count < finish:
        #time.sleep(0.25)
        entry = parseEntry(count)
        if entry == None:
            count += 20
            continue
        f_entry.write(str(count) + "|" + str(entry[0]) + "|" + str(entry[1]) + "|" + str(entry[2]) + "|" + str(entry[3]) + "\n")
        if entry[1] not in users:
            users.append(entry[1])
            f_user.write(str(entry[1]) + "\n")
        count += 20
        hundred_count += 1
        if hundred_count == 100:
            f_entry.close()
            f_user.close()
            f_entry = open("entryler.csv", 'a')
            f_user = open("kullanicilar.csv", 'a')
            print(count)
            hundred_count = 0
        
    f_entry.close()
    f_user.close()
    

f_entry = open("entryler.csv", 'w')
f_user = open("kullanicilar.csv", 'w')
f_entry.writelines(["id|başlık|yazar|içerik|zaman\n"])
f_user.writelines(["yazar\n"])
f_entry.close()
f_user.close()

for i in range(20):
    t = Thread(target = parser, args = (i,))
    t.daemon = True
    t.start()