import os
import utils

class Corpus:
    def __init__(self, path_to_directory):
        self.path_to_directory = path_to_directory


    # Generate all emails in corpus in format file name, body
    def emails(self):
        self.filenames = os.listdir(self.path_to_directory)
        for filename in self.filenames:
            if filename.startswith("!"):
                continue
            else:
                with open(f"{self.path_to_directory}/{filename}", 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    yield filename, file_content

    # Generate all spams in corpus in format file name, body
    def spams(self):
        classification = utils.read_classification_from_file (f"{self.path_to_directory}/!truth.txt")
        filenames = os.listdir(self.path_to_directory)
        for filename in filenames:
            if filename.startswith("!"):
                continue

            if classification[filename] == 'OK':
                continue
            else:
                with open(f"{self.path_to_directory}/{filename}", 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    yield filename, file_content

    # Generate all hams in corpus in format file name, body
    def hams(self):
        classification = utils.read_classification_from_file(f"{self.path_to_directory}/!truth.txt")
        filenames = os.listdir(self.path_to_directory)
        for filename in filenames:
            if filename.startswith("!"):
                continue

            if classification[filename] == 'SPAM':
                continue
            else:
                with open(f"{self.path_to_directory}/{filename}", 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    yield filename, file_content
