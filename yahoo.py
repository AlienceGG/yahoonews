# -*- coding: utf-8 -*-
##Version：2.0
##Python：python2.7
##By：alience
##LastUpdate：2014.12.05
   
import urllib2  
import urllib  
import re  
import thread  
import time  
import os
import sys
import datetime
import MySQLdb

from bs4 import BeautifulSoup


def page_loop(page,news_id):
    page=page+10
    myUrl = 'https://news.search.yahoo.com/search;_ylt=AwrBJR.uqXJUCSwAt_LQtDMD?p=visit&fr=yfp-t-703&fr2=piv-web&provider=4551793&focuslim=provider&xargs=0&pstart=1&b='+str(page)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
    headers = { 'User-Agent' : user_agent } 
    req = urllib2.Request(myUrl, headers = headers) 
    myResponse = urllib2.urlopen(req).read()
    soup = BeautifulSoup(myResponse)


    div_web_soup=soup.find(attrs={"id":"web"})
    # only one ser_results=soup.find_all("ul")

    a_tag=div_web_soup.find_all('a')
    
    for atag in a_tag:
        print news_id
        #print atag 
        a_href=atag.get('href')
        right_url='http://news.yahoo.com/'
        if(a_href.find(right_url)==0):
            a_req=urllib2.Request(a_href)
            a_response=urllib2.urlopen(a_req).read()
            a_soup=BeautifulSoup(a_response)

            news_tittle=a_soup.find('h1').get_text()
            
            cite_tag=a_soup.find('cite')
            
            span_tag_author=cite_tag.find_all('span')
            if(len(span_tag_author)!=0):
                    news_author=span_tag_author[1].get_text()
            else:
                news_author=''

            abbr_tag=cite_tag.find('abbr')
            news_time=abbr_tag.get_text()
            p_tag=a_soup.find_all('p')
            news_content=''
            for p in p_tag:	
                news_content=news_content+p.get_text()
            newsprint(news_tittle,news_author,news_time,news_content)   
            write(news_id,a_href,news_tittle,news_author,news_time,news_content)
            news_id=news_id+1
    page_loop(page,news_id)

def newsprint(news_tittle,news_author,news_time,news_content):
    print 'news_tittle:'+news_tittle
    print 'news_author:'+news_author
    print 'news_time:'+news_time
    print 'news_content:'+news_content  

def write(news_id,a_href,news_tittle,news_author,news_time,news_content):
    try:
        #如果是第一个数据，多一个建数据库
        if(news_id==1):
            conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306,charset='utf8')
            cur=conn.cursor()
            
            #这个是数据库编码 
            conn.set_character_set('utf8')
            cur.execute('SET NAMES utf8;')
            cur.execute('SET CHARACTER SET utf8;')
            cur.execute('SET character_set_connection=utf8;')
            
            cur.execute('create database if not exists python12')
            conn.select_db('python12')

            #数据库习惯性报错，拉丁文blabala
            news_tittle=news_tittle.encode('latin-1', 'ignore')
            news_author=news_author.encode('latin-1', 'ignore')
            news_time=news_time.encode('latin-1', 'ignore')
            news_content=news_content.encode('latin-1', 'ignore')

            cur.execute('create table test(id int,url varchar(200),source varchar(20),tittle varchar(100),author varchar(50),time varchar(50),content text)')
 
            value=[news_id,a_href,'yahoo',news_tittle,news_author,news_time,news_content]
            cur.execute('insert into test values(%s,%s,%s,%s,%s,%s,%s)',value)
            print str(news_id)+'ok'
            conn.commit()
            cur.close()
            conn.close()
        else :
            conn=MySQLdb.connect(host='localhost',user='root',passwd='root',port=3306,charset='utf8')
            cur=conn.cursor()

            conn.set_character_set('utf8')
            cur.execute('SET NAMES utf8;')
            cur.execute('SET CHARACTER SET utf8;')
            cur.execute('SET character_set_connection=utf8;')
            
            conn.select_db('python12')
            value=[news_id,a_href,'yahoo',news_tittle,news_author,news_time,news_content]
            news_tittle=news_tittle.encode('latin-1', 'ignore')
            news_author=news_author.encode('latin-1', 'ignore')
            news_time=news_time.encode('latin-1', 'ignore')
            news_content=news_content.encode('latin-1', 'ignore')
            cur.execute('insert into test values(%s,%s,%s,%s,%s,%s,%s)',value)
            print str(news_id)+'ok'
            conn.commit()
            cur.close()
            conn.close()
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])    
    

#----------- 程序的入口处 -----------
if __name__=='__main__':
    page_loop(1,1)
