from IPython.display import Markdown, display
from tabulate import tabulate
from urllib.request import urlopen
from bs4 import BeautifulSoup
from langchain.schema.document import Document
import os, json

def load_text(book_id: int) -> str:
    """
    Load a book from the Gutenberg project.

    :param book_id: The id of the book to load.
    :return: The text of the book.
    """
    START_MARKERS = ['*** START OF']
    END_MARKERS = ['*** END OF']

    def _download(url: str) -> str:
        try:
            print(f'loading text from {url}')
            with urlopen(url) as response:
                text = []
                # ignore lines up to start markers
                for line in response:
                    line = line.decode("utf-8-sig").strip()
                    if any(line.startswith(token) for token in START_MARKERS):
                        break
                # add all lines up to end markers
                for line in response:
                    line = line.decode("utf-8-sig").strip()
                    if any(line.startswith(token) for token in END_MARKERS):
                        break
                    text.append(line)
            return '\n'.join(text).strip()
        except:
            return None
    return  _download(f'http://aleph.gutenberg.org/{"/".join(str(book_id)[:-1])}/{book_id}/{book_id}.txt') or \
            _download(f'http://aleph.gutenberg.org/{"/".join(str(book_id)[:-1])}/{book_id}/{book_id}-0.txt') or \
            _download(f'https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt') or \
            _download(f'https://www.gutenberg.org/files/{book_id}/{book_id}.txt') or \
            _download(f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt')

def from_cache(book_id: int) -> str:
    """
    Load a book from local cache. If not in cache,
    return None.

    :param book_id: The id of the book to load.
    :return: The text of the book.
    """
    if not os.path.exists(f'books/{book_id}.json'):
        return None
    with open(f'books/{book_id}.json', 'r') as f:
        metadata = json.load(f)
    with open(f'books/{book_id}.txt', 'rb') as f:
        content = f.read().decode('utf-8').replace('\r', '')
    return Document(metadata=metadata, page_content=content)

def to_cache(book_id: int, book: dict) -> None:
    """
    Write book to local cache.

    :param book_id: The id of the book to load.
    :return: The text of the book.
    """
    # ensure books folder exists
    os.makedirs('books', exist_ok=True)
    # dump json of book without property text
    text = book['text']
    book = book.copy()
    del book['text']
    # write book to cache
    with open(f'books/{book_id}.json', 'w') as f:
        json.dump(book, f)
    print(f'wrote book to cache: books/{book_id}.json')
    with open(f'books/{book_id}.txt', 'wb') as f:
        f.write(text.encode('utf-8'))
    print(f'wrote book to cache: books/{book_id}.txt')

def get_cache_ids() -> list:
    """
    Return list of book ids in cache

    :return: List of ids in cache
    """
    # ensure books folder exists
    os.makedirs('books', exist_ok=True)
    
    # scan file names from *.txt files from the books folder
    return [int(file.split('.')[0]) for file in os.listdir('books') if file.endswith('.json')]

def get_cache_list() -> list:
    """
    Read metadata from cache and return.

    :return: List of books in cache
    """
    def _read_metadata(book_id: int) -> dict:
        with open(f'books/{book_id}.json', 'r') as f:
            book = json.load(f)
        return book
    # scan file names from *.txt files from the books folder
    return [_read_metadata(book_id) for book_id in get_cache_ids()]

def load_book(book_id: int) -> dict:
    """
    Load a book from the Gutenberg project.

    :param book_id: The id of the book to load.
    :return: The text of the book.
    """
    # read meatdata from page
    print(f'loading metadata from https://www.gutenberg.org/ebooks/{book_id}')
    with urlopen(f'https://www.gutenberg.org/ebooks/{book_id}') as response:
        page = BeautifulSoup(response, 'html.parser')
    book = { 'id': book_id }
    rows = page.find('table', {'class': 'bibrec'}).find_all('tr')
    rows.reverse() 
    fields = dict([[row.find('th').get_text().lower().strip(), row.find('td').get_text().strip()] for row in rows if row.find('th')])
    a = fields['author'].split(',')
    book['yearspan'] = a.pop().strip()
    book['author'] = ','.join(a)
    book['title'] = fields['title']
    book['language'] = fields['language']
    book['release_date'] = fields['release date']

    # load text from Gutenberg project
    book['text'] = load_text(book_id)

    # create dictionary with book id as key and book text as value
    return book

def get_book(book_id: int, reload: bool = False) -> dict:
    """
    Load a book from the Gutenberg project.

    :param book_id: The id of the book to load.
    :return: The text of the book.
    """
    # check if book is in cache
    if not(reload) and (book := from_cache(book_id)):
        return book
    # fetch book from Gutenberg project
    book = load_book(book_id)
    to_cache(book_id, book)
    return from_cache(book_id)


def print_books(list: list[dict] = None, extra_headers: list[str] = None, format: str = 'pipe'):
    """
    Print books in list.

    :param list: The list of books to print.
    :param format: The format of the output.
    """
    list = sorted(list or get_cache_list(), key=lambda x: x['language'] + x['author'] + x['title'])
    headers = ['id', 'language', 'author', 'title'] + (extra_headers or [])
    rows = [[x[h] for h in headers] for x in list]
    if format == 'text':
        print(tabulate(rows, headers, tablefmt="github"))
        print()
    else:
        display(Markdown(tabulate(rows, headers, tablefmt="pipe")))
