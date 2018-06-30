'''get list of words from dictionary.com
'''
import os
import sys
import string

f = open("word_list.txt", "wb")

url_to_data = {}

def wget(url):
    import urllib2
    global url_to_data
    if url in url_to_data:
        return url_to_data[url]
    else:
        print "wget\t" + url
        data = urllib2.urlopen(url).read().strip()
        url_to_data[url] = data
        return data
    
chrs = list(string.ascii_lowercase)
chrs.insert(0,'0')

def extract_words(data):
    word_urls = []
    d = data.split('class="word">')[1:]
    ci = -1
    for dd in d:
        ci += 1
        stuff = dd.split('</span>')[0]
        url = stuff.split('"')[1]
        word_urls.append(url)
        f.write(url + "\n")
        
    return word_urls

print "new line\n\n\n\n"

all_word_urls = []

for c in chrs:
    p_i = 1  # start at 1 and go until we get the same result (again)
    
    data, data_last = None, None
    while(True):
        a = "http://www.dictionary.com/list/" + c + "/" + str(p_i)
        p_i += 1
        data = wget(a)
        
        if data == data_last:
            break
        
        word_urls_this_page = extract_words(data)
        all_word_urls.extend(word_urls_this_page)
        
        data_last = data

f.close()
