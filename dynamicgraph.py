import requests
from lxml import etree
import numpy as np
import pandas as pd
import time
import re

headers = {
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0'
}

idlist = pd.read_table('Influencer.txt',header=0,encoding='gb18030',delim_whitespace=True)
idlist.columns=['idlist']

def downloadurl(id):
    url = 'https://socialblade.com/instagram/user/%s/legacy'%(id)
    return(url)

def parsefollow(id):
    r = requests.get(downloadurl(id), headers=headers)
    page = etree.HTML(r.content)
    daterange = page.xpath('//div[@style="width: 865px; background: #333; padding: 20px; margin-top: 20px; text-transform: uppercase; color:#fff;"]/h2/text()')
    dates = re.findall('\d+-\d+-\d+',daterange[0].strip())
    index = pd.date_range(dates[0],dates[1])
    coredata = page.xpath('//div[@style="width: 890px; padding: 15px 10px 15px 5px; background: #fff; float: left; margin: 0px 0px 10px 0px;"]/script/text()')
    core = re.findall('data: .(\d.+\d)]',coredata[0].strip())
    corelists = [i.split(',') for i in core]
    adjust = len(index)-len(corelists[0])
    indexadjust = index[adjust:]
    df = pd.DataFrame(np.transpose(corelists), index=indexadjust, columns=['followers', 'following', 'updates'])
    df.to_csv("%s.csv"%id, sep=',', mode='a', encoding='gb18030')

for i in range(len(idlist.loc[:,'idlist'])):
    id = idlist.loc[i, 'idlist']
    try:
        parsefollow(id)
        time.sleep(1)
    except:
        print("There is something wrong in %s"%(id))
