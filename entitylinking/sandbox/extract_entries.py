import re
#import warc

from html.parser import HTMLParser

def get_text_from_warc(file):
	f = warc.open(file)
	output = []
	with open('entries_single_page.txt', 'w', encoding="utf-8") as outfile:
		for record in f:
			if record.header.get("WARC-Trec-ID"):
				outfile.write('WARC-Trec-ID: ' + record.header.get("WARC-Trec-ID") + '\n')
			if record.url:
				payload = record.payload.read()
				header, html = payload.split(b'\r\n\r\n', maxsplit=1)
				html = html.strip()
				if len(html) > 0:
					text = get_text_from_html(html)
					if text:
						text = cleanup(text)
						for entry in text.replace('\n', ' ').split():
							outfile.write(entry + '\n')
				break
	return output

def cleanup(s):
	s = re.sub(' +', ' ', s)
	s = re.sub(r'[^a-zA-Z0-9]+', ' ', s)
	return s

def get_text_from_html(html):
	tree = HTMLParser(html)
	if tree.body is None:
		return None
	for tag in tree.css('script'):
		tag.decompose()
	for tag in tree.css('style'):
		tag.decompose()
	text = tree.body.text(separator='\n')
	return text

get_text_from_warc('sample.warc.gz')