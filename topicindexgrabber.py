#! /usr/bin/env python
#--*-- encoding: utf-8 --*--
# filename: topicindexgrabber.py

import time,os,os.path,urllib2,errno,re
import websr
from sgmllib import SGMLParser
from websr import indexurl


# define state
DEAD=0
DONE=1
CONNECTING=2
CONNECTED=3
#define timeout
TIME_OUT=10


class pagesRedirectHtml(SGMLParser):
    def reset(self):
        self.lastpage=''
        self.templist=[]
        self.is_a=False
        SGMLParser.reset(self)

    def start_a(self,attrs):
        self.is_a=True
        self.templist=[v for k,v in attrs if k=='href']

    def end_a(self):
        self.is_a=False

    def handle_data(self,text):
        if self.is_a==True:
            mh=re.match(r'^最后一页',text)
            if mh:
                self.lastpage=self.templist[0]
                return self.lastpage


class pagesgrabber(object):
    """ get all the sort pages for the  main url"""
    def __init__(self,homeurl):
        self.url=homeurl
        self.content=''
        self.urllist=[]
    def collectPages(self):
        request=urllib2.Request(self.url,headers=websr.header)
        try:
            response=urllib2.urlopen(request,timeout=TIME_OUT)
            self.content=response.read()
        except Exception,e:
            print 'read web error occur',e
            return
        return self.handle_data()
    def handle_data(self):
        if self.content:
            prt=pagesRedirectHtml()
            prt.feed(self.content)
            lastpage=prt.lastpage
            self.urllist.append(self.url) #home url
            if lastpage:
                pos=lastpage.find('page=')
                startdirect=lastpage[:pos+5]
                num=lastpage[pos+5:]
                print 'num is ' ,num
                print 'direct is ',startdirect
                numvalue=int(num)
                if numvalue>1:
                    for ii in xrange(2,numvalue+1):
                        directurl="%s%s%d" %(indexurl,startdirect,ii)
                        self.urllist.append(directurl)
        return self.urllist
"""
the following two class  to get topic url.html
  welcom to test"""

#define two-function to collect users topics
def CollectUserTopicsList(content):
    #pattern=re.compile(r"<a href=.*?id=.*?>[\u4e00-\u9fa5_a-zA-Z0-9]+</a>")
    pattern=re.compile(r'(?:<a href=").*?" id=".*?">.*?</a>')
    alllist=pattern.findall(content)
    needlist=[]
    myflag=r'id="thread_title_'
    for li in alllist:
        if li.find(myflag)>0:
            tup=ExtractDirectAndName(li)
            needlist.append(tup)
    return needlist
#must content 'href=' and 'id=' key words
def ExtractDirectAndName(href_ele):
    href_key='href='
    id_key='id'
    pos1=href_ele.find(href_key)+len(href_key)
    pos2=href_ele.find(id_key)
    url=href_ele[pos1:pos2]
    url=url.rstrip()
    url=url.replace(r'"','')
    pos1=url.find(r's=')
    pos2=url.find(r';')
    inurl=url[0:pos1]
    inurl+=url[pos2+1:]
    name=''
    pattern=re.compile(r">.*?<")
    ks=re.search(r'>.*?<',href_ele)
    if ks:
        name=ks.group(0)
        name=name.replace('<','')
        name=name.replace('>','')
        name=name.replace(os.path.sep,'')
        name=name.replace(r"&quot;",r'"')
        name+='.html'
    else:
        name='special.html'
    tup=(inurl,name)
    return tup




if __name__=='__main__':
    pageg=pagesgrabber('http://bbs.pediy.com/forumdisplay.php?f=30')
    pageurl_ll=pageg.collectPages()
    count=0
    for ll in pageurl_ll:
        count+=1
        if count>2:
            break
        getc=websr.GetContentFromUrl(ll)
        getc.Content()
        li=CollectUserTopicsList(getc.content)
        for ii in li:
            mvs,kvs=ii
            print mvs,kvs
