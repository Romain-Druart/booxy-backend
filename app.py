from logging import exception
from sys import getsizeof
import time
from itsdangerous import json
import meilisearch

from gutenberg.query import list_supported_metadatas
from gutenberg.acquire import get_metadata_cache

from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata

#Get le cache 
#cache = get_metadata_cache()
#cache.populate()


# text = strip_headers(load_etext(2701)).strip()
# print(text)

from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


client = meilisearch.Client('http://127.0.0.1:7700')

@app.route('/api/add-rank/<book_id>')
def add_rank(book_id):
    doc = client.index('books').get_document(book_id)
    if 'download' in doc:
        client.index('books').update_documents([{
            'id': book_id,
            'download': doc['download']+1
        }])
    else: 
        client.index('books').update_documents([{
            'id': book_id,
            'download': 1
        }])  

#     if is_search:
#         client.index('books').search('', {
#   'filter': ['id' = f'{book_id}] })

    return jsonify(doc)

@app.route('/api/get-facets')
def get_facets():
    result = client.index('books').search('', {'facetsDistribution': ['author', 'language','subject']})
    facets = {'author': [],'language': [], 'subject': []}
    if 'author' in result['facetsDistribution']:
        for i in result['facetsDistribution']['author'].keys():
            facets['author'].append(i)
    for i in result['facetsDistribution']['language'].keys():
        facets['language'].append(i)
    for i in result['facetsDistribution']['subject'].keys():
        facets['subject'].append(i)
    return jsonify(facets)

@app.route('/api/add-book/<int:id>')
def add_book(id):
    #try:
    documents = []
    i = 1
    e = id
    text = ""
    try: 
        text = strip_headers(load_etext(i*e)).strip()
    except:
        pass

    title = list(get_metadata('title', i*e))
    if len(title) > 0:
        title = title[0]
    else:
        title = "Unknown"

    language = list(get_metadata('language', i*e))
    if len(language) > 0:
        language = language[0]
    else:
        language = "Unknown"

    rights = list(get_metadata('rights', i*e))
    if len(rights) > 0:
        rights = rights[0]
    else:
        rights = "Unknown"

    subject = list(get_metadata('subject', i*e))
    if len(subject) > 0:
        subject = subject[0]
    else:
        subject = "Unknown"

    author = list(get_metadata('author', i*e))
    if len(author) > 0:
        author = author[0]
    else:
        author = "Unknown"

    uri = list(get_metadata('formaturi', i*e))
    if len(uri) > 0:
        uri = uri[0]
    else:
        uri = "Unknown"

    book = {'id': i+(e*10), 'title': title, 'language': language, 'rights': rights, 'subject': subject, 'author':author, 'book': text, 'cover': f'https://www.gutenberg.org/cache/epub/{i*e}/pg{i*e}.cover.medium.jpg'}
    documents.append(book)
    index = client.index('books')
    task = index.add_documents_in_batches(documents,100)
    while True:
        tmp = client.get_task(task[0]["uid"])
        if  tmp["status"] == 'succeeded':
            break
        time.sleep(0.1)
    # except Exception as preexception:
    #     print(tmp)
    #     print(preexception)

    return jsonify({'message': 'Success'})

@app.route('/api/settings')
def settings():
    client.index('books').update_settings({
    'displayedAttributes': [
        'id',
        'title',
        'download',
        'language',
        'rights',
        'subject',
        'cover',
        'author'
        
    ]})
    client.index('books').update_ranking_rules([
        'words',
        'typo',
        'proximity',
        'attribute',
        'sort',
        'download:desc',
        'exactness',
    ])
    client.index('books').update_settings({
    'searchableAttributes': [
        'title',
        'book',
        'subject'
    ]})
    client.index('books').update_filterable_attributes([
        'author',
        'language',
        'subject'
    ])
    return jsonify({'message': 'success'})
# print(list_supported_metadatas()) 

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# printProgressBar(0, nb*10, prefix = 'Progress:', suffix = 'Complete', length = 50)

# for e in range(1,nb):

#     # ('author', 'formaturi', 'language', 'rights', 'subject', 'title')
#     for i in range(1+(e*10),10+(e*10)):
#         printProgressBar(i+(e*10), nb*10, prefix = 'Progress:', suffix = 'Complete', length = 50)



