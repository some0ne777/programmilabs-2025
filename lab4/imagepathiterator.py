import csv
import os

class ImagePathIterator:
    def __init__(self, csv_file: str):
        self.paths = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    path = row.get('Absolute path', '')
                    if path and os.path.exists(path):
                        self.paths.append(path)
        except:
            pass
    
    def __iter__(self):
        self.index = 0
        return self
    
    def __next__(self):
        if self.index < len(self.paths):
            path = self.paths[self.index]
            self.index += 1
            return path
        raise StopIteration