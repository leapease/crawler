#! /usr/bin/python2.7
#-*- encoding: utf-8 -*-

from urllib2 import Request,urlopen,HTTPError,URLError
import os
import ordinalpars

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0'
header={ 'User-Agent' : user_agent }
indexurl=r'http://bbs.pediy.com/'
TIME_OUT=10


class SrcWebIndex(object):

    ''' class for getting html '''
    def __init__(self,mainurl):
        self.url=mainurl

    def getMainUrl(self):
        "search for pediy not using cookielib"
        getCon=GetContentFromUrl(self.url)
        getCon.Content()
        content=getCon.content
        cli=ordinalpars.CrUrlList()
        cli.feed(content)
        return cli.undict

#define class to get content from url

class GetContentFromUrl(object):
    def __init__(self,url):
        self.url=url
        self.content=''
    def Content(self):
        req=Request(self.url,headers=header)
        try:
            response=urlopen(req,timeout=TIME_OUT)
            self.content=response.read()
        except Exception,e:
            print 'error occur ,reason is ',e
            return
        return self.content



if __name__=='__main__':
    src=SrcWebIndex(indexurl)
    dict1=src.getMainUrl()
    for (k,v) in dict1.iteritems():
        print k,v
