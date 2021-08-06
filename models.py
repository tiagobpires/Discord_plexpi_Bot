class Torrent:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.size = ''
        self.status = ''
        self.progress = ''

    def __str__(self):
        return f'{self.id}\t{self.name}\t{self.size}\t{self.status}\t{self.progress}'

    def __repr__(self):
        return f'Torrent(id={self.id}, name={self.name}, size={self.size}, '\
               f'status={self.status}, progress={self.progress})'

    def completed(self):
        return self.progress == '100%'
