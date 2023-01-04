import os
import codecs
import pprint as pp
import pickle
from pathlib import Path

class Indexer:
    @classmethod
    def create_index(self, source_dir_path):
        whitespace_chars = set([" ", "\t", "\n", "\r", "\f", "\v"])
        index = {}

        for employee in os.listdir(source_dir_path):
            all_docs_path = f"{source_dir_path}/{employee}/all_documents"

            # TODO: iterate through each subdir if all_documents/ is missing
            if not os.path.isdir(all_docs_path):
                continue

            for doc in os.listdir(all_docs_path):
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

                            word += char
                            if len(word) <= 1:
                                index_dir_path = f"{source_dir_path}/../cache/{'/'.join([*word])}"
                            else:
                                sub_word = word[:-1]
                                index_dir_path = f"{source_dir_path}/../cache/{'/'.join([*sub_word])}"

                            Path(index_dir_path).mkdir(parents=True, exist_ok=True)
                            index_file_path = f"{index_dir_path}/index.pickle"

                            if os.path.isfile(index_file_path):
                                with open(f"{index_file_path}", 'rb') as index_file:
                                    index = pickle.load(index_file)
                            else:
                                index = {}

                            if word not in index:
                                index[word] = set()
                            index[word].add((doc_path, row, col))

                            with open(f"{index_file_path}", 'wb') as index_file:
                                pickle.dump(index, index_file, protocol=pickle.HIGHEST_PROTOCOL)

                # break after one document
                break

            # break after one employee
            break

    @classmethod
    def search(self, word):
        # TODO move magic number to instance property
        dir_path = "/".join([*word[:3]])
        file_path = f"cache/{dir_path}/index.pickle"

        with open(file_path, 'rb') as index_file:
            index = pickle.load(index_file)
            pp.pprint(index[word])
