import json
from collections import Counter

with open("articles/articles.json", "r") as json_file:
    data = json.load(json_file)

keyword_counter = Counter()
author_counter = Counter()

for entry in data:
    keyword_counter.update(entry["keywords"])    
    author_counter.update(entry["authors"])

with open('articles/keywords.txt', 'a') as f:
    f.write("Keyword Frequencies:\n")
    for keyword, frequency in keyword_counter.items():
        f.write(f"{keyword}: {frequency}\n")

with open('articles/authors.txt', 'a') as f:
    f.write("\nAuthor Frequencies:\n")
    for author, frequency in author_counter.items():
        f.write(f"{author}: {frequency}")