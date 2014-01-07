#! /usr/bin/python2.7
"""
this python file control download process

"""

import ordinalpars,websr
import topicindexgrabber
import os

#define function to get directory

def getWorkingDir():
    curdir=os.getcwd()
    if not curdir.endswith(os.path.sep):
        curdir+=os.path.sep
    curdir+='download'+os.path.sep
    if not os.path.exists(curdir):
        os.mkdir(curdir)
    return curdir

def writeToFile(content,dpath):
    file_w=open(dpath,'w')
    try:
        file_w.write(content)
    except Exception,e:
        print 'write file error,',e
        return
    file_w.close()

class DownloadWebsites(object):
    def __init__(self,mainsite,workdir):
        self.mainsite=mainsite
        self.workdir=workdir
        self.success_num=0
        self.fail_num=0
        self.total_num=0
        self.topic_dict={}

    def gointomainsite(self):
        src=websr.SrcWebIndex(self.mainsite)
        dict_main_topic=src.getMainUrl()
        for (k,v) in dict_main_topic.iteritems():
            dpath=self.workdir+k+os.path.sep
            if not os.path.exists(dpath):
                os.mkdir(dpath)
            topic_url=self.mainsite+v
            self.topic_dict[dpath]=topic_url
        return self.topic_dict

    def gointomaintopicsite(self):
        self.gointomainsite()
        for (k,v) in self.topic_dict.iteritems():
            print 'go into top topics website: ',v
            tpig=topicindexgrabber.pagesgrabber(v)
            page_ll=tpig.collectPages()
            for pl in page_ll:
                wsrc=websr.GetContentFromUrl(pl)
                wsrc.Content()
                ii=topicindexgrabber.CollectUserTopicsList(wsrc.content)
                for (ikurl,ikname) in ii:
                    nexturl=mainsite+ikurl
                    downpath=k+ikname
                    print 'read url:,',nexturl
                    wdscf=websr.GetContentFromUrl(nexturl)
                    wdscf.Content()
                    writeToFile(wdscf.content,downpath)
                    print 'write file %s succced!' % ikname

    def download_job(self):
        self.gointomaintopicsite()


if __name__=='__main__':
    workingdir=getWorkingDir()
    mainsite=websr.indexurl
    dls=DownloadWebsites(mainsite,workingdir)
    dls.download_job()
