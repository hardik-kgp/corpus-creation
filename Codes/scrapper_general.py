from bs4 import BeautifulSoup as bs 
import requests
from html.parser import HTMLParser
import sys

class Parser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.inHead = False
		self.skipData = False

	def handle_starttag(self, tag, attrs):
		if tag=='code':
			self.skipData = True
		if tag == 'h2' or tag == 'h3' or tag == 'h4' or tag == 'strong':
			self.inHead = True

	def handle_endtag(self, tag):
		if tag=='code':
			self.skipData=False
		if tag == 'h2' or tag == 'h3' or tag == 'h4' or tag == 'strong':
			self.inHead = False
		return

	def handle_data(self, data):
		if self.skipData:
			return
		if self.inHead:
			if data.lower() in self.skipHeaderList:
				return
			else:
				print("**"+data+"**")
				return
		print(data,end=' ')
		return

res = requests.get("https://stackoverflow.com/search?page=2&tab=Relevance&q=data%20structures")
soup = bs(res.text,'lxml')
links = soup.findAll('a' , {'class':'question-hyperlink'})
st = open('stopwords.txt','a+')
parser=Parser() 
for link in links:
	sys.stdout  = sys.__stdout__
	link = str(link["href"])
	page_title = (link.split('/')[3])
	page_title = page_title.split('?')[0]
	if(not link.startswith('/qu')):
		continue
	print("include ?? ",link.split('/')[3])
	ans = str(input())
	if(ans!="y"):
		if(ans=='s'):
			continue
		st.write("%s\n" %ans)
		continue
	sys.stdout = open('stackoverflow_pages/'+page_title + '.txt', 'w')
	print('***',link.split('/')[3].split('?')[0],'***')	
	link="https://stackoverflow.com"+link.split('?')[0]
	res1 = requests.get(link)
	soup1 = bs(res1.text,'lxml')
	answers = soup1.findAll('div' , {'class':'post-text'})
	for answer in answers:
		parser=Parser()
		#print(answer)
		parser.feed(str(answer))	
		 

	
	
	
		
	
	
