import os
import sys
import csv
import codecs
from pathlib import Path
import email
import pickle

import cache_constants as c
import cache_helpers as h
from trie import Trie

class CacheGenerator():
    def __init__(self):
        self.trie = Trie()
        self.data = {}

        # Number of documents to process - there are around 128103 documents total
        # self.max_docs = 10_000
        self.max_docs = float("inf")
        # Number of documents to process in memory before writing results to disk
        self.batch_size = 10_000
        # Number of documents to process before printing progress message
        self.read_msg_interval = 1_000
        # Number of word cache files to write to disk before
        self.write_msg_interval = 10_000

    def generate(self, source_dir_path):
        # Check if cache already exists
        # =============================
        if os.path.isdir(c.CACHE_DIR_PATH):
            print("The cache already exists.")
            print("To search the cache use: ./search_cache <term>")
            return
        Path(c.CACHE_DIR_PATH).mkdir()

        # Loop through employees
        # ======================
        total_docs = 0
        employees = os.listdir(source_dir_path)
        for employee in employees:
            all_docs_path = f"{source_dir_path}/{employee}/all_documents"
            if not os.path.isdir(all_docs_path):
                continue

            # Loop through employees
            # ======================
            documents = os.listdir(all_docs_path)
            for doc in documents:
                total_docs += 1
                doc_path = f"{all_docs_path}/{doc}"
                with codecs.open(doc_path, 'r',
                                 encoding='utf-8',
                                 errors='replace') as document:

                    # Exclude email headers and attachments
                    # =====================================
                    # Hat tip: https://stackoverflow.com/a/32840516/2770474
                    body = ""
                    message = email.message_from_file(document)
                    if message.is_multipart():
                        for part in message.walk():
                            ctype = part.get_content_type()
                            cdispo = str(part.get('Content-Disposition'))
                            if ctype == 'text/plain' and 'attachment' not in cdispo:
                                body = part.get_payload()
                    else:
                        body = message.get_payload()

                    # Build an intermediate data dictionary
                    # =====================================
                    word = ""
                    for i in range(len(body)):
                        char = body[i]
                        if char in c.WHITESPACE_CHARS:
                            if word not in self.data:
                                self.data[word] = []
                            self.data[word].append((doc_path, i))
                            word = ""
                            continue
                        word += char.lower()

                # After processing reading each document...
                # =========================================
                # Print a progress message at intervals
                if total_docs % self.read_msg_interval == 0:
                    print(f"{total_docs} documents read")
                # Save the batch data to disk and the trie in memory
                if total_docs % self.batch_size == 0:
                    self._write_data()
                # Exit both loops if doc limit exceeded
                if total_docs >= self.max_docs:
                    break
            # Exit both loops if doc limit exceeded
            if total_docs >= self.max_docs:
                break

        # After reading all documents...
        # ==============================
        # Write the last chunk of data
        self._write_data()
        # Write the completed trie to disk
        with open(c.TRIE_FILE_PATH, 'wb') as trie_file:
            pickle.dump(self.trie, trie_file, protocol=pickle.HIGHEST_PROTOCOL)


    # Writes data to the file cache and trie in memory
    # ================================================
    def _write_data(self):
        i = 0
        for word in self.data:
            # Print a progress message at intervals
            if i % self.write_msg_interval == 0:
                print(f"{i} words written")
            # Write to trie
            self.trie.add_word(word)
            file_path = h._cache_file_path(word)
            # Write to file
            with open(file_path, 'a+') as cache_file:
                writer = csv.writer(cache_file)
                writer.writerows(self.data[word])
            i += 1
        self.data.clear()
