#/usr/bin/python3
#-*- coding: utf-8 -*-
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import telegram
import certifi
import ssl

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def get_config():   
    config = {}
    with open("config.py") as f:
        for line in nonblank_lines(f):
            if line and "#" not in line:
                val = line.replace(" ", "").split("=")
                config[val[0]] = val[1]
            else:
                pass
    return config

def get_sites():   
    sites = {}
    with open("sites.py") as f:
        for line in nonblank_lines(f):
            if line and "#" not in line:
                val =line.split(",")
                sites[val[0].replace(" ", "")] = val[1]
            else:
                pass
    return sites

def main():
    
    config = get_config()
    
    bot = telegram.Bot(config["TOKEN"])
    group_id = config["GROUP_ID"]
    #bot.sendMessage(chat_id = group_id ,text = "Bot connected successfully")
    print("Bot connected successfully")
    def sendMsg(idChat,message):
        #bot.sendMessage(chat_id = idChat ,text = message)
        print(message)
        
    sites = get_sites()

    for site in sites:
        alias = sites[site]
        req = Request(site)
        try:
            #gcontext = ssl._create_unverified_context()
            gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            response = urlopen(req,context=gcontext)
            sendMsg(group_id,'El sitio '+ alias +' está trabajando correctamente')
        except HTTPError as e:
            sendMsg(group_id,'El servidor no pudo completar la petición hacia ' + alias + '.')
            sendMsg(group_id,'Error code: '+ str(e.code))
        except URLError as e:
            sendMsg(group_id,'Error en ' + alias)
            sendMsg(group_id,'Reason: ' + str(e.reason))

if __name__ == "__main__":
    main()
