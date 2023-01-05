import pickle
import os
import csv

import cache_constants as c
import cache_helpers as h
from trie import Trie

class CacheSearchEngine:

    def __init__(self):
        # Number of results to show in each "page"
        self.page_size = 10

        if not os.path.exists(c.CACHE_DIR_PATH):
            msg = f"Expected dir {c.CACHE_DIR_PATH}/ to exist."
            cmd = "To regenerate the cache, use: `./create_cache <path_to_enron_data>`"
            raise FileNotFoundError("\n".join([msg, cmd]))

        if not os.path.exists(c.TRIE_FILE_PATH):
            msg = f"Expected {c.TRIE_FILE_PATH} to exist. To regenerate it, use:"
            cmd = "`rm -r cache/ && ./create_cache <path_to_enron_data>`"

            raise FileNotFoundError("\n".join([msg, cmd]))
        # Load the trie into memory just once
        # ===================================
        print("Loading trie, this may take a few seconds...")
        with open(c.TRIE_FILE_PATH, 'rb') as trie_file:
            self.trie = pickle.load(trie_file)

    def search(self, prefix, cli=True):
        prefix = h._encode(prefix)

        quit = False
        while not quit:
            # Retrieve matching words from the trie
            # =====================================
            matches = self.trie.match_prefix(prefix)
            if not matches:
                print(f"'{prefix}' was not found.")
                prefix, quit = self._search_again() if cli else (None, True)
                continue
            results_count = 0
            fieldnames = ["doc_path", "position"]
            for term in matches:
                # Iterate through file corresponding to each match
                # ================================================
                file_path = h._cache_file_path(term)
                with open(file_path) as file:
                    reader = csv.reader(file)
                    for line in reader:

                        if results_count % self.page_size == 0:
                            self._page_number(results_count)

                        self._print_cache_item(line, term, prefix)
                        results_count += 1

                        if results_count % self.page_size == 0:
                            if cli == True:
                                quit = not self._next_page(results_count)
                            else:
                                quit = True

                        if quit:
                            break
                    if quit:
                        break

            if not quit:
                print(f"End of results.")

            if cli == True:
                prefix, quit = self._search_again()
            else:
                prefix, quit = (None, True)

        print("Goodbye!")

    def _page_number(self, results_count):
        n = results_count // self.page_size + 1
        msg = f"Page {n}"
        line = len(msg) * "="
        print("\n".join([msg, line]))

    def _print_cache_item(self, line, term, prefix):
        doc_path, position = line
        style = c.BLUE + c.BOLD + c.UNDERLINE
        end_style = c.END
        n = len(prefix)
        print(f"---")
        print(f"match: '{style}{term[:n]}{end_style}{term[n:]}'")
        print(f"path: {doc_path}")
        print(f"position: {position}")

    def _next_page(self, results_count):
        start = results_count - self.page_size
        msg = f"Showing results {start}-{results_count}"
        line = "=" * len(msg)
        print(line)
        print(msg)
        yn = ""
        msg = f"View next {self.page_size} results? [y/n]\n=> "
        while not yn in ['y', 'n']:
            yn = input(msg).lower().strip()
        if yn == 'y':
            print("gets here")
            return True
        else:
            return False

    def _search_again(self):
        msg = "Enter your next query: (or type /quit)\n=> "
        prefix = input(msg).lower().strip()
        if prefix == "/quit":
            return (None, True)
        else:
            return (prefix, False)
