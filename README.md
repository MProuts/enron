# Enron Takehome

## To create the index:
```sh
./create_index <path_to_enron_data>
```

This would be the preprocessing that was happening on the server. This is
exceptionally slow because we're sort of brute forcing I/O -- each character causes a
read/write to disk. There's definitely a better way to batch read/writes, but
this is just me trying to get something out the door.

# To search:
```sh
./search <term>
```

This would be on the mobile client. The app would come bundled with the index
files on disk.
