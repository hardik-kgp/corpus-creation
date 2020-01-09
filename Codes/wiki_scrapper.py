from html.parser import HTMLParser
import wikipediaapi
import sys
import numpy as np

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inHead = False
        self.skipData = False
        self.currDataLevel = 0
        self.levels = [1]
        with open('skip_header_list.txt', 'r') as f:
    	    self.skipHeaderList = set([line.strip() for line in f])

        with open('accept_header_list.txt', 'r') as f:
            self.acceptHeaderList = set([line.strip() for line in f])

    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            self.inHead = True
            if self.skipDataLevel >= 2:
                self.skipDataLevel = 100
            while self.levels[-1] >= 2:
                self.levels.pop()
            self.levels.append(2)
        elif tag == 'h3':
            self.inHead = True
            if self.skipDataLevel >= 3:
                self.skipDataLevel = 100
            while self.levels[-1] >= 3:
                self.levels.pop()
            self.levels.append(3)
        elif tag == 'h4':   
            self.inHead = True
            if self.skipDataLevel >= 4:
                self.skipDataLevel = 100
            while self.levels[-1] >= 4:
                self.levels.pop()
            self.levels.append(4)
        else:
            return

    def handle_endtag(self, tag):
        if tag == 'h2' or tag == 'h3' or tag == 'h4':
            self.inHead = False
            # self.levels.pop()
        return
        print("End tag  :", tag)

    def handle_data(self, data):
        if self.inHead:
            # for item in self.skipHeaderList:
            #     print(item)
            if data.lower() in self.skipHeaderList:
                self.skipDataLevel = self.levels[-1]
                return
            elif data.lower() in self.acceptHeaderList:
                if self.skipDataLevel > self.levels[-1]:
                    print("**"+data+"**")
                return
            else:
                if self.skipDataLevel > self.levels[-1]:
                    print("Accept Header? [Y/n]: " + data.lower(), file=sys.stderr)
                    x = input()
                    if x.lower() == 'n':
                        self.skipDataLevel = self.levels[-1]
                        self.skipHeaderList.update({data.lower()})
                        return
                    else:
                        if self.skipDataLevel > self.levels[-1]:
                            print("**"+data+"**")
                        self.acceptHeaderList.update({data.lower()})
                        return
                return


        if len(self.levels) == 0 or self.skipDataLevel <= self.levels[-1]:
            return
        print(data,end=' ')

        return

    def save_dicts(self):
    	with open('skip_header_list.txt', 'w') as f:
    		for item in self.skipHeaderList:
        		f.write("%s\n" % item)
    	with open('accept_header_list.txt', 'w') as f:
    		for item in self.acceptHeaderList:
        		f.write("%s\n" % item)

wiki_html = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.HTML)
pages = ['Operating_system','Software_quality']

for page_title in pages:

    sys.stdout = open('raw_corpus/'+page_title + '.txt', 'w')

    page = wiki_html.page(page_title) # insert title here
    print('***'+page_title.replace('_', ' ')+'***')
    parser = Parser()
    parser.feed(page.text)
    parser.save_dicts()
