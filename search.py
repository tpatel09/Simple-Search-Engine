# Author: Tejas Patel
# Email: trpatel@umass.edu
# Spire ID: 33247968
import urllib.request
import re
import string
import sys


def read_article_file(url):
  req = urllib.request.urlopen(url)
  text = req.read()
  text = text.decode('UTF-8')
  return text

def text_to_article_list(text):
  articles = re.split('<NEW ARTICLE>', text)
  articles = [article for article in articles if article.strip()]
  return articles

def split_words(text):
  words = []
  lines = text.splitlines()
  for line in lines:
    line_words = line.split()
    words.extend(line_words)
  return words

def scrub_word(word):
  scrubbed_word = word.strip(string.punctuation)
  return scrubbed_word

def scrub_words(words):
  scrubbed_words = []
  for word in words:
    scrubbed_word = word.strip(string.punctuation).lower()
    if scrubbed_word:
      scrubbed_words.append(scrubbed_word)
  return scrubbed_words

def build_article_index(article_list):
  article_index = {}
  for (index, article) in enumerate(article_list):
      words = split_words(article)
      for word in words:
          scrubbed_word = scrub_words(word)
          article_index[scrubbed_word].add(index)
  return article_index

def find_words(keywords, index):
  intersect_docs = set()
  for keyword in keywords:
      scrubbed_word = scrub_words(keyword)
      if scrubbed_word in index:
          docs = index[scrubbed_word]
          if len(intersect_docs) == 0:
              intersect_docs = docs
          else:
              intersect_docs = intersect_docs.intersection(docs)
  return intersect_docs




if __name__ == '__main__':
  print(len(sys.argv))
  if len(sys.argv) != 4:
      print("Usage: python search.py URL command keyword")
      sys.exit(1)
  url = sys.argv[1]
  command = sys.argv[2]
  keyword = sys.argv[3]

  text = read_article_file(url)
  articles = text_to_article_list(text)
  index = build_article_index(articles)

  if command == "find":
      article_ids = find_words(keyword.split(), index)
      print(" ".join(str(id) for id in article_ids))
  elif command == "print":
      article_id = int(keyword)
      if article_id >= len(articles):
          print("Article not found")
      else:
          print(articles[article_id])
  else:
      print("Unknown command:", command)
      sys.exit(1)
