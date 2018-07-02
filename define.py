#!/usr/bin/env python2.7
import io
import re
import sys
import xml
import libxml2
import html5lib
from lxml import etree
from contextlib import contextmanager

args = sys.argv

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


@contextmanager  # elementTree.dump() went to terminal
def stdout_redirector(stream):  # grab data instead
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout


root = html5lib.parse(wget("http://www.dictionary.com/browse/" + args[1]))
print "word:" + args[1]

'''result is xml.etree object
    https://docs.python.org/2/library/xml.etree.elementtree.html'''

for c in root[1]:
    summary = str(c).strip()
    if len(summary.split("script")) < 2:
        if len(summary.split("div")) > 1:
            defs = {}
            q = io.BytesIO()
            with stdout_redirector(q):
                xml.etree.ElementTree.dump(c)
            r = q.getvalue()
            ol_s = re.findall("<html:ol(.*?)</html:ol>", r)
            for l in ol_s:
                li_s = re.findall("<html:li(.*?)</html:li>", r)
                for ll in li_s:
                    if len(ll.split("luna-example")) > 1:
                        defs[ll.strip()] = None
            ci = 0
            for key in defs:
                ci += 1
                k = "<html:span " + key
                k = re.sub("<html:style(.*?)</html:style>", " ", k)
                k = str(ci) + ". " + re.sub('(<!--.*?-->|<[^>]*>)', ' ', k)
                while(k != re.sub("  ", " ", k)):
                    k = re.sub("  ", " ", k)
                print k + "\n"
