#Import required modules
import argparse
from bs4 import BeautifulSoup
from bs4.element import Comment
import string
import requests

#Remove HTML data save for visible text
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

#Scrape HTML Data from URL
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

#Clean text
def clean_up_text(html) :
    translator = str.maketrans('', '', string.punctuation)
    translated = text_from_html(html).translate(translator)
    word_list = translated.split()
    words = [word.lower() for word in word_list]
    unique_words = set(words)
    return sorted(unique_words)

#Create additional arguments
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--alpha-only', action='store_true', help="Include only alphabetic characters")
parser.add_argument('-n', '--numbers-only', action='store_true', help="Include only numeric characters")
parser.add_argument('-p', '--potential-issues', action='store_true', help="Add a warning for words that might pose an issue")
parser.add_argument('url', nargs='+', help='Target URL')
args = parser.parse_args()

#Process arguments
for url in args.url :
    r  = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    cleaned_up_list = clean_up_text(r.text)
    #Filter numbers and write to file
    if args.numbers_only:
        numbers = filter(str.isdigit, cleaned_up_list)
        for word in sorted(numbers) :
            print(word)
    #Filter letters and write to file
    elif args.alpha_only:
        letters = filter(str.isalpha, cleaned_up_list)
        for word in sorted(letters) :
            print(word)
    #Potential Issues Warning
    elif args.potential_issues:
        test = filter(str.isalnum, cleaned_up_list)
        print("\n" + "Potential Issues:")
        for t in cleaned_up_list:
            test = filter(str.isalnum, cleaned_up_list)
            if(t not in test):
                print(t)
    #Default option; write to file
    else:
        for word in cleaned_up_list :
            print(word)
