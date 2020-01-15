import requests
from lxml import etree
import pandas as pd
from datetime import datetime
import re
import time

idlist = pd.read_table('Influencer.txt',header=0,encoding='gb18030',delim_whitespace=True)
idlist.columns=['idlist']

def downloadurl(id):
    url = 'https://socialblade.com/instagram/user/%s/monthly'%(id)
    return(url)

headers = {
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0'
}

def getcorelist(id):
    r = requests.get(downloadurl(id), headers=headers)
    page = etree.HTML(r.content)
    coredata = page.xpath('//div[@id="socialblade-user-content"]/script/text()')
    corelists = re.findall('data: ..(.+\d).',coredata[0].strip())
    return(corelists)

def genedata(corelists,id):
    #followers_w = corelists[3].split('],[')
    #following_w = corelists[4].split('],[')
    updates_w = corelists[5].split('],[')
    newlist = [[datetime.fromtimestamp(int(i.split(',')[0]) / 1000).strftime('%Y-%m-%d'), i.split(',')[1]] for i in
                   updates_w]
    df = pd.DataFrame(newlist, columns=['Date', '%s_updates_w' %(id)])
    return(df)

j=0
base = pd.DataFrame(columns=('Date',''))
for i in range(len(idlist.loc[:,'idlist'])):
    id = idlist.loc[i, 'idlist']
    print(id)
    try:
        corelist = getcorelist(id)
        new = genedata(corelist,id)
    except:
        new = pd.DataFrame(columns=('Date','%s_updates_w'%id))
    data = pd.merge(base, new, on = 'Date', how = 'outer', sort =True)
    time.sleep(1)
    base = data
    j = j+1
    print('This is the %s Influencer'%j)
    if id == 'katestedlife':
        data.to_csv("updates_w.csv", sep=',', mode='a', encoding='gb18030',index=False)
        break
