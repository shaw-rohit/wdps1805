from bs4 import BeautifulSoup
from bs4 import Comment
from pattern.web import plaintext
import nltk
import warc
import re 
from nltk.corpus import treebank



def cleanMe(html):
    soup = BeautifulSoup(html, "html5lib")    
    [x.extract() for x in soup.find_all('script')]
    [x.extract() for x in soup.find_all('style')]
    [x.extract() for x in soup.find_all('meta')]
    [x.extract() for x in soup.find_all('noscript')]
    [x.extract() for x in soup.find_all(text=lambda text:isinstance(text, Comment))]
    return soup


f = warc.open("sample.warc.gz")
for record in f:
	if record.header['Warc-type'] == 'response':
		print record.header['Warc-Trec-ID']
		data =  record.payload.read()
		header , text = data.split('\r\n\r\n',1)
		soup =cleanMe(text)
		content = soup.get_text().encode('ascii', 'ignore').decode('ascii')
		content = ''.join([i for i in content if not i.isdigit()])
		content = re.sub(r"[':;,.&{}()@$%^*-]", '', content)
		tokens = nltk.word_tokenize(content)
		tagged =nltk.pos_tag(tokens)
		entities=nltk.chunk.ne_chunk(tagged)
		a1=str(entities)
		file_object = open('out.text','w')
		file_object.write(a1)
		file_object.close()
		print entities
		quit()



