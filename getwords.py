#!/usr/bin/env python2.7
import os
import sys

url_to_data = {}


def wget(url):
    import urllib2
    global url_to_data
    if url in url_to_data:
        return url_to_data[url]
    else:
        print "wget\t" + url
        response = urllib2.urlopen(url)  # print response.info()
        data = response.read().strip()
        url_to_data[url] = data
        return data

print os.popen("mkdir -p dat").read().strip()

for line in open("word_list.txt").readlines():
    words = line.strip().split("/")
    word = words[len(words) - 1]
    fn = "dat/" + word
    open(fn, "wb").write(wget(line.strip()))

