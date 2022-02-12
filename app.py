from sys import getsizeof
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
# print('print'+list(get_metadata('title', 2701)))
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

#printProgressBar(0, nb*10, prefix = 'Progress:', suffix = 'Complete', length = 50)
#     # ('author', 'formaturi', 'language', 'rights', 'subject', 'title')
#     for i in range(1+(e*10),10+(e*10)):
#         printProgressBar(i+(e*10), nb*10, prefix = 'Progress:', suffix = 'Complete', length = 50)
#i = 1
#e = 49345


nbBooks = 10
client = meilisearch.Client('http://127.0.0.1:7700', 'poulet')

#Index
index = client.index('books')
client.index('books').update_settings({
  'displayedAttributes': [
      'title',
      'language',
      'rights',
      'subject',
      'cover'
]})
client.index('books').update_settings({
  'searchableAttributes': [
      'title',
      'book',
      'subject'
]})


# Créer la liste de livres et indexer
documents = []
for e in range(1,nbBooks):
    text = ""
    try: 
        text = strip_headers(load_etext(e)).strip()
    except:
        pass
    title = list(get_metadata('title', e))
    if len(title) > 0:
        title = title[0]
    else:
        title = "Unknown"
    language = list(get_metadata('language', e))
    if len(language) > 0:
        language = language[0]
    else:
        language = "Unknown"
    rights = list(get_metadata('rights', e))
    if len(rights) > 0:
        rights = rights[0]
    else:
        rights = "Unknown"
    subject = list(get_metadata('subject', e))

    uri = list(get_metadata('formaturi', e))
    if len(uri) > 0:
        uri = uri[0]
    else:
        uri = "Unknown"
    book = {'id': e*10, 'title': title, 'language': language, 'rights': rights, 'subject': subject, 'book': text, 'cover': f'https://www.gutenberg.org/cache/epub/{e}/pg{e}.cover.medium.jpg'}
    documents.append(book)
index.add_documents_in_batches(documents,100)


