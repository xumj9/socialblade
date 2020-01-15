import requests
from lxml import etree
import pandas as pd
from datetime import datetime
import re

idlist = pd.read_table('Influencer.txt',header=0,encoding='gb18030',delim_whitespace=True)
idlist.columns=['idlist']
f = open('Influencer.txt','w')

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
    for i in range(len(corelists)):
        corelists[i] = corelists[i].split('],[')
        newlist = [[datetime.fromtimestamp(int(i.split(',')[0]) / 1000).strftime('%Y-%m-%d'), i.split(',')[1]] for i in
                   corelists[i]]
        df = pd.DataFrame(newlist, columns=['date', '%s_recent_list%s' %(id,str(i))])
        df.to_csv('%s_recent_list%s.csv' %(id,str(i)), sep=',', mode='a', encoding='gb18030')


for i in range(len(idlist.loc[:,'idlist'])):
    id = idlist.loc[i, 'idlist']
    try:
        corelist = getcorelist(id)
        genedata(corelist,id)
    except:
        f.write(id+'\n')

f.close()
