import os
import codecs
import pprint as pp
import json
from pathlib import Path
import shutil

class Indexer:
    def __init__(self):
        self.tree_depth = 3

    def create_index(self, source_dir_path):
        # Delete existing cache
        shutil.rmtree("cache", ignore_errors=True)
        whitespace_chars = set([" ", "\t", "\n", "\r", "\f", "\v"])
        max_emp_count = 10
        max_doc_count = 10

        # TODO break loops into generators
        for emp_count, employee in enumerate(os.listdir(source_dir_path)):
            print(f"indexing employee {employee}")
            all_docs_path = f"{source_dir_path}/{employee}/all_documents"

            # TODO: iterate through each subdir if all_documents/ is missing
            if not os.path.isdir(all_docs_path):
                continue

            for doc_count, doc in enumerate(os.listdir(all_docs_path)):
                doc_path = f"{all_docs_path}/{doc}"
                with codecs.open(doc_path, 'r',
                                 encoding='utf-8',
                                 errors='replace') as document:
                    word = ""
                    for row, line in enumerate(document):
                        for col, char in enumerate(line):
                            if char in whitespace_chars:
                                word = ""
                                continue

                            word += char.lower()
                            sub_word = word[:self.tree_depth]
                            word_path = '/'.join([*sub_word])
                            index_dir_path = f"{source_dir_path}/../cache/{word_path}/"
                            Path(index_dir_path).mkdir(parents=True, exist_ok=True)

                            index_file_path = f"{index_dir_path}/index.json"

                            # TODO: chunk this so not reading/writing on each
                            # iteration
                            if os.path.isfile(index_file_path):
                                with open(f"{index_file_path}", 'r') as index_file:
                                    index = json.load(index_file)
                            else:
                                index = {}

                            if word not in index:
                                index[word] = []
                            index[word].append((doc_path, row, col))

                            # TODO: chunk this so not reading/writing on each
                            # iteration
                            with open(f"{index_file_path}", 'w') as index_file:
                                index_file.write(json.dumps(index))

                # break after n documents
                if doc_count >= max_doc_count:
                    break

            # break after n employees
            if emp_count >= max_emp_count:
                break

    def search(self, word):
        dir_path = "/".join([*word[:self.tree_depth]])
        file_path = f"cache/{dir_path}/index.json"
        if not os.path.isfile(file_path):
            print(f"Term '{word}' not found")
            return

        with open(file_path, 'rb') as index_file:
            index = json.load(index_file)
            if not word in index:
                print(f"Term '{word}' not found")
                return

            for file_path, row, col in index[word]:
                print(f"{file_path}")
                print(f"line: {row}, column: {col}")
                print()

