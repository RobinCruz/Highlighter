import nltk
from newspaper import Article

def scrape(url):
  art=Article(url)
  art.download()
  art.parse()
  art.nlp()
  text= art.text
  #text= summarize.call(text)
  return text