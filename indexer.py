import os
import codecs
import pprint as pp

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
                                if len(word) > 0:
                                    if not word in index:
                                        index[word] = set()
                                    index[word].add((doc_path, row, col))
                                    word = ""
                            else:
                                word += char

            pp.pprint(index)
            break
