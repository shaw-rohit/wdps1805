from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from nltk.wsd import lesk
from bs4 import Comment
import requests
import nltk
import re


url = "https://www.indiacelebrating.com/essay/importance-of-sports-essay/"


def cleanMe(html):
    soup = BeautifulSoup(html, "html5lib")    
    [x.extract() for x in soup.find_all('script')]
    [x.extract() for x in soup.find_all('style')]
    [x.extract() for x in soup.find_all('meta')]
    [x.extract() for x in soup.find_all('noscript')]
    [x.extract() for x in soup.find_all(text=lambda text:isinstance(text, Comment))]
    return soup

nltk.download('stopwords')
nltk.download('wordnet')
response = requests.get(url)
response = cleanMe(response.content.decode('utf-8')).get_text()
clearText = re.sub('<[^>]*>','',response)
clearText = clearText.replace('\n','')
clearText = clearText.replace('\r','')
clearText = clearText.replace('\t','')
clearText = re.sub(r'[^\x00-\x7F]+',' ',clearText)
clearText = re.sub(r'[(?<=\{)(:*?)(?=\})]',' ',clearText)
i = 0 
Sentenses = clearText.split('.')
for line in Sentenses:
    if len(line) > 6:
        #print (str(i)+". "+line)
        #print("######################################################################")
        tokens           = nltk.word_tokenize(line);
        stopWordsRemoved = [word for word in tokens if word not in stopwords.words('english') and len(word) > 3] 
        tagged           = nltk.pos_tag(stopWordsRemoved)
        entities         = nltk.chunk.ne_chunk(tagged)
        for words in entities:
            if type(words) is tuple:
                #print (type(words))
                Synset = lesk(line, words[0], 'n')
                if Synset is not None:
                    print(str(Synset)+" [##] "+Synset.definition())
                    i = i + 1
        #print(stopWordsRemoved)

#print (Sentenses) 

print(i)