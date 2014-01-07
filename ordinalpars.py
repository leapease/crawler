#! /usr/bin/python2.7
# -*- encoding: utf8 -*_



from sgmllib import SGMLParser
import urllib2



class CrUrlList(SGMLParser):
    "device from SGMLParser to parse html"

    def reset(self):
        self.url=''
        self.undict={}
        self.is_a=False
        SGMLParser.reset(self)

    def start_a(self,attrs):
        self.is_a=True
        self.url='' # for temp use
        templist=[v for k,v in attrs if k=='href']
        if templist:
            tlist=[]
            tlist.extend(templist)
            self.url=tlist[0]


    def end_a(self):
        self.is_a=False


    def handle_data(self,text):
        if self.is_a==True:
            if text.find('』')>0 :
                self.undict[text]=self.url



if __name__=='__main__':
    num=0
    content=urllib2.urlopen('http://bbs.pediy.com/index.php').read()
    cli=CrUrlList()
    cli.feed(content)
    print 'url and name dictionary'
    for (k,v) in cli.undict.iteritems():
        print '%s %60s' % (k.ljust(20),v)

