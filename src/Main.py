import wechatsogou
import datetime
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr
import rc


def mail(article):
    ret = True
    try:
        msg = MIMEText(article['abstract'] + '<br>文章链接:<a href=\'' + article['content_url'] + '\'>点此进入</a>'
                       + '<br>报名地址:<a href=\'' + article['source_url'] + '\'>点此进入</a>', 'html', 'utf-8')
        msg['From'] = formataddr(['NCHU_LectureMonitors', from_addr])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr([to_addr, to_addr])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "NCHU_新的讲座_" + article['title']  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(from_addr, password)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(from_addr, [to_addr, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


from_addr = input('输入你的邮箱账号：')
password = input('输入你的邮箱密码：')
to_addr = input('发送到谁的邮箱：')
time_delay = int(input('时间间隔(分钟)：'))
time_start = int(input('开始时间(小时):'))
time_end = int(input('结束时间(小时):'))

ws_api = wechatsogou.WechatSogouAPI()
i = 1
while 1:
    # 检查是否在该运行的时间内
    cur_time = datetime.datetime.now()
    if cur_time.hour < time_start or cur_time.hour > time_end:
        print('当前时间:', cur_time, '未到爬取时间，跳过')
        time.sleep(time_delay * 60)
        continue

    print('正在进行第' + str(i) + '次扫描')
    i = i + 1
    data = ws_api.get_gzh_article_by_history('NCHU-XSH',
                                             identify_image_callback_sogou=rc.identify_image_callback_ruokuai_sogou,
                                             identify_image_callback_weixin=rc.identify_image_callback_ruokuai_weixin)
    articles = data['article']
    for article in articles:
        title = article['title']
        if '学而有术' in title:
            titleTimeStamp = article['datetime']
            # print('datetime', titleTimeStamp)
            titleTime = datetime.datetime.utcfromtimestamp(titleTimeStamp)

            diffMinutes = (cur_time - titleTime).total_seconds()
            if diffMinutes / 60 < (time_delay + 1) * 60:  # 发送时间在15分钟内
                # 发送邮件
                ret = mail(article)
                if ret:
                    print("邮件发送成功")
                else:
                    print("邮件发送失败")

    time.sleep(time_delay * 60)