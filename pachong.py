import os
import pandas as pd
from IPython.core.interactiveshell import InteractiveShell
#InteractiveShell.ast_node_interactivity = "all"
#pd.set_option('display.max_colwidth', 100)

link = 'http://www.mitbbs.com/bbsdoc1/Immigration_1_0.html'

agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
        
from urllib.request import urlopen, Request
headers = agent
reg_url = link
req = Request(url=reg_url, headers=headers) 
html = urlopen(req).read() 
#print(html)
text_file = open("G:\My Drive\Paper review\Scrape_mitbbs\Output.txt", "wb")
text_file.write(html)
text_file.close()

def load_xml(file_path):
    f = open(file_path, 'r', encoding="GB2312", errors='ignore')
    # gb2312 works in jupyter but not .py
    out = f.readlines()
    doc = []
    for line in out:
        doc.append(line)
    df = pd.Series(doc)
    return df
    
output_path = "G:\My Drive\Paper review\Scrape_mitbbs\Output.txt"
d = load_xml(output_path)

#d.iloc[630:632]
# print(d.iloc[629])
# print(d.iloc[630])
article_id = d.str.extractall(r'article_t/Immigration/([0-9]{1,})')[0].tolist()
article_index = d.str.extractall(r'article_t/Immigration/([0-9]{1,})').index.tolist()
article_index = [i[0] for i in article_index]
title_index = [i+1 for i in article_index]
list_title = d.iloc[title_index].tolist()
date_range = [i-5 for i in article_index]
list_date = d.iloc[date_range].str.extractall(r'(\d{4,4}[-]\d{2,2}[-]\d{2})')[0].tolist()


t = pd.DataFrame(list(zip(article_id, list_title, list_date)), 
               columns =['article_id', 'title', 'date']) 
t['link'] = t['article_id'].apply(lambda x: 'http://www.mitbbs.com/article_t/Immigration/'+ x +'.html')
t1 = t[t.title.str.contains('审稿')]

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib
    
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = '' # ENTER YOUR OWN SENDER EMAIL OR input('From: ')
password = '' # ENTER YOUR SEND EMAIL PASSWORD OR input('Password: ')
to_addr = '' # ENTER YOUR RECIPIENT EMAIL OR input('To: ')
smtp_server = 'smtp.gmail.com' #input('SMTP server: ')

msg = MIMEText(t1.to_string(), 'plain', 'utf-8')
msg['From'] = _format_addr('yanshuli.ds')
#msg['To'] = _format_addr('管理员 <%s>' % to_addr)
msg['Subject'] = Header('mitbbs_crawl', 'utf-8').encode()
    
smtp_server = 'smtp.gmail.com'
smtp_port = 587
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
