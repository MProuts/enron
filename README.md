# Enron Takehome

## Usage

**To use pre-build cache:**

Download
[cache.zip](https://drive.google.com/file/d/1yM8t4G_iDnClITtaxHnbAlYDANr07UZ-/view)
and place it in the root of the project. Then:

```sh
unzip cache.zip
./search_cache <term>
```
**To manually build the cache:**
```sh
./create_cache <path_to_enron_data>
./search_cache <term>
```

## Summary

The cache stores the path and position of each occurance of a given word in a
separate file. For example, the cache file for the word 'puppy' looks like this:

**cache/puppy.csv**
```csv
maildir/kaminski-v/all_documents/10296.,2540
maildir/kaminski-v/all_documents/2431.,1327
maildir/kaminski-v/all_documents/5861.,1009
```

While the cache is built, a [trie](https://en.wikipedia.org/wiki/Trie) is also
created and saved in `cache/trie.pickle`. The search engine loads this trie on
initialization (once for each cli session) and uses it to determine which
complete words exist for a given prefix. Results each of those words can then be
read directly from `cache/<word>.csv`.

## Performance

 ```sh
# Time
# ====
# The cache takes ~6 minutes to build on my hardware.
time ./create_cache maildir
126.50s user 68.33s system 51% cpu 6:15.67 total

# With the trie loaded, consecutive searches for the 1000 most common words take
# a little over a 1 second total.
./search_1000
2114157 function calls (348824 primitive calls) in 1.193 seconds

# Space
# =====
# The complete cache is ~5GB on disk.
% du -hs cache
4.7G    cache

# Not great, but not terrible considering the original emails are ~3GB on disk.
% du -hs maildir
2.8G    maildir

# The complete trie, which will be loaded in memory, is 35MB.
% du -hs cache/trie.pickle
35M    cache/trie.pickle
```

## Improvements

I think we could get the footprint way down if we just zipped the cache and
email directories and had queries read from the zip archives. Not sure
now that'll affect reads but worth a try.
