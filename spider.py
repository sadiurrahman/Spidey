#!/usr/bin/python3

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import re
import os
import requests
import tkinter
from tkinter import ttk
from tkinter import messagebox



def get_page(url):
    try:
        r = requests.get(url, stream=True,timeout=10)
        print(r.status_code)
        return r
    except:
        return ''

#takes care of only one level of redirection
#downloads url
def download(url):
    global storage
    try:
#        if(url[-1]!='/'):
            r = requests.get(url, stream=True, timeout=10)
            while ((str(r.history)).split('[')[1]).split(']')[0]=='302':
                r = requests.get(url,allow_redirects=False)
                if r.status_code == 302:
                    url1 = r.headers['location']
                    print(url, "  ", url1)
                    if(url1.startswith('http')):
                        url=url1
                        r = requests.get(url, stream=True,timeout=10)
#            if(r.status_code==200):
            print('in downloading', url)
            file_str = url.split('//')[1].split('/')
            l1 = len(file_str)
            file_Name = url.split('/')[-1]
            l = file_Name.split('.')[-1]
            done = 0
            tot = 0
            length = r.headers.get('content-length')
            if(length != None):
                length = int(length)
            if (l.lower()=='pdf' or l.lower()=='ppt' or l.lower()=='jsp'):
                try:
                    storage.pop(storage.index(url))
                except:
                    pass
            if(l.lower() in d_list):
                l2=file_str[0].split('.')[1]
                for i in range(1,l1-1):
                    l2=l2+'/'+file_str[i]
                    if not os.path.exists(l2):
                        os.makedirs(l2)
                file_Name=l2+'/'+file_Name
                if (l.lower()!='html' or l.lower()!='htm'):
                    try:
                        storage.pop(storage.index(url))
                    except:
                        pass
                with open(file_Name, 'wb') as fd:
                    print('downloding ... ', url)
                    print('The Current level is'+str(j), a_levels,levels)
                    print('The Current count is '+str(i),a_count, count)
                    print('The Total count is '+str(count))
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            done += len(chunk)
                            tot = int((100 * done) / length)
#                            show_down_size.set(tot+'%')
                            fd.write(chunk)
                            fd.flush()
                            sys.stdout.write("\r      {0}%     " .format(tot))
                            sys.stdout.flush()            
 #    else:
  #              with open('logs.txt',a) as fd:
   #                 fd.write(str(r.status_code)+'...'+url+'\n')
    except:
        with open('logs.txt','a') as fd:
            fd.write('....'+url+'\n')
        try:
            storage.pop(storage.index(url))
        except:
            pass
        print('#######-----',url, '--cant download moving ahead')

#traverses given url and stores all of them in list
def links(url):
        print('in links', url)
        global storage
        storage=[]
        count = 0
        try:
            r = get_page(url)
            content = r.text
            soup = BeautifulSoup(content)
            for link in soup.find_all('a'):
                a=(link.get("href"))
                if(a!=None): 
#                    if (a.startswith("http")):
#                        d1 = a.split('.')[-1]
#                   if(d1=='html' or d1=='htm'):
                    if(url[0]!='#'):
#                       d1 = a.split('.')[-1]
                        a= urljoin(url,a)
                    if a not in store and a not in storage:
                        count += 1
#                   if(d1=='html' or d1=='htm'):
                        storage.append(a)
                        print(a)
# here we are checking if this link corresponds to a file or folder
#                        w= re.compile(r'.{4,5}://www\..*\..{2,4}.*\..*')
#                        if str(w.match(a))!='None':
                        if(a[-1]!='/'):
                            download(a)
            print(storage)
            return storage, count
        except:
#        with open('logs.txt','a') as fd:
#            fd.write(str(r.status_code)+'...'+url+'\n')
#        print('####--',url, '--cant download moving ahead')
            return [],0


if __name__=="__main__":
        d_list = input('Enter file types seperated by space : ').split()
        store,storage, count, a_count, a_levels,temp =[],[],1, 0, -1, 0
#
        levels = int(input('Enter no of levels(starting from 1) : '))
        url = input('Enter URL (include http/https) : ')
        store.append(url)
        temp = count
        for j in range(a_levels, levels):
            print('present_level ',j)
            count = temp
            for i in range(a_count, count):
                print('present_count ',a_count, i,count)
                l = links(store[i])
                if i==0:
                    download(store[i])
                store = store + l[0]
                temp = temp + l[1]
                print (temp , store)
            a_count = count
            print('\n completed and the success level is ' , j+1,'\n')



#done---increase efficiency..... dont send all links to download
#done----#.. append a / before links containing # also check if / is already present
#done----# add other links also to store not only those containing html or htm
#done----# add links in a set or if list check if they have been added before
#algo is bfs

