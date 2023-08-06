import pyexlatex as pl


class CoAuthor(pl.Template):

    def __init__(self, author_name: str):
        self.author_name = author_name
        self.contents = [pl.NoLineBreak(name) for name in author_name.split(' ')]
        super().__init__()
