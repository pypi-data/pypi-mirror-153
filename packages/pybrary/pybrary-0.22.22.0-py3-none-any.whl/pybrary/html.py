from html.parser import HTMLParser
from urllib.request import urlopen

from . import debug

class Node:
    def __init__(self, parent, tag, attrs):
        self.parent = parent
        self.tag = tag
        self.attrs = dict(attrs)
        self.text = None
        self.children = []

    @property
    def level(self):
        return self.parent.level+1 if self.parent else 0

    def add(self, node):
        self.children.append(node)

    def __iter__(self):
        for child in self.children:
            yield child
            yield from child

    @property
    def classes(self):
        return self.attrs.get('class',  '').split(' ')

    def __getattr__(self, key):
        return self.attrs.get(key, '')

    def __str__(self):
        return f'{"  "*self.level}{self.tag} {self.classes}'


class Parser(HTMLParser):
    auto_end = 'img', 'link', 'meta'

    def handle_starttag(self, tag, attrs):
        if self.current.tag in self.auto_end:
            self.handle_endtag(self.current.tag)
        # print('  -->', tag)
        node = Node(self.current, tag, attrs)
        self.current.add(node)
        self.current = node

    def handle_data(self, data):
        self.current.text = data.strip()

    def handle_endtag(self, tag):
        current = self.current.tag
        if current!=tag and current in self.auto_end:
            self.handle_endtag(current)
        # print('<--  ' ,tag)
        self.current = self.current.parent

    def load(self, html):
        debug('parser load %s', len(html))
        self.root = Node(None, 'root', {})
        self.current = self.root
        self.feed(html)
        self.close()
        debug('parser html loaded')
        return self.root

    def get(self, url):
        html = urlopen(url).read().decode('utf-8')
        return self.load(html)
