import wechatsogou
import datetime

ws_api = wechatsogou.WechatSogouAPI()

data = ws_api.get_gzh_article_by_history('NCHU-XSH')

articles = data['article']
for article in articles:
    title = article['title']
    if '学而有术' in title:
        titleTimeStamp = article['datetime']
        print('datetime', titleTimeStamp)
        titleTime = datetime.datetime.utcfromtimestamp(titleTimeStamp)

        curTime = datetime.datetime.now()
        diffMinutes = (curTime - titleTime).total_seconds()
        if diffMinutes/60 < 15: #发送时间在15分钟内
            #do someThing
            print('diffMinutes', diffMinutes / 60)

#print(ws_api.get_gzh_article_by_history('NCHU-XSH'))