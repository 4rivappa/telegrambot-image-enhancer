import re

def clean_line(input):
    input = re.sub("\s\s+", " ", input)
    input = input.strip()
    return input

quotes_file = open('./data-collection/quotes.txt', 'r', encoding='utf-8')

for line in quotes_file.readlines():
    if line == "":
        continue
    parts = line.split('―')
    quote = clean_line(parts[0])
    author = clean_line(parts[1])
    print(quote)
    print(author)

quotes_file.close()
