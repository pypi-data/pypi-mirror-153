# filum 

`filum` saves discussion threads to your local machine. 

It's like a bookmark manager but it saves actual content rather than just the link pointing to it.

It's like Pocket or Instapaper but for Reddit, Hacker News and Stack Exchange. 


## Installation

1. Create a virtual environment for `filum` (optional but recommended).

Linux: `$ python3 -m venv /path/to/new/venv`

Windows: `$ c:\Python35\python -m venv c:\path\to\new\venv`

For more details [click here](https://docs.python.org/3/library/venv.html).

2. Install from PyPI.

`python3 -m pip install filum`


## Usage

### Save a new thread

`$ filum add <url>`

Example: `$ filum add https://www.reddit.com/r/Python/comments/v1rde4/whats_a_python_feature_that_is_very_powerful_but/ianzrfp/`

You may supply a permalink to a child node of the thread to save only a specific section of the thread.

The following platforms are supported: Reddit, Hacker News, Stack Exchange.

### View information about currently saved threads

`$ filum all`

The left-most column of the table contains values to be used as selectors (in place of `<label>`) for the subsequent commands.

### View a specific thread

`$ filum show <label>`

Example: `$ filum show 2` for the thread in the table with '2' in the `#` column.

*Note that the values in the `label` column are dynamic. Run `$ filum all` after modifying the database to see all changes.* 

The thread is piped through a terminal pager by default. To disable this, run `$ filum config` and edit `pager = true` to `pager = false`.

If you use a pager, you can navigate between nodes in the thread by searching for the `¬` symbol (yes very hacky).

### Delete a thread

`$ filum delete <label>`

Example: `$ filum delete 2` for the thread in the table with '2' in the `#` column.

### Update a thread

`$ filum update <label>`

Example: `$ filum update 2` for the thread in the table with '2' in the `#` column.

`filum` will offer to update a thread if you try to add a thread that's already saved in the database.

### Add tags to a saved thread

`$ filum tags <label> <tag 1> <tag 2> ...`

Example: `$ filum tags 2 python webdev` to add the tags "python" and "webdev" to the thread in the table with '2' in the `#` column.

### Delete tags from a saved thread

`$ filum tags <label> <tag 1> <tag 2> ... --delete`

Example: `$ filum tags 2 webdev --delete` to remove the tag "webdev" from the thread in the table with '2' in the `#` column.

### Search for a thread

Full-text search of saved threads is currently unavailable. However, you can filter the threads by tags or by source.

`$ filum search --tags <tag>`

`$ filum search --source <source>`

To select a thread based on the table returned by the search command, pass in the flag that was used as the filter.

`$ filum show <label> --tags <tag>`

`$ filum show <label> --source <source>`


## Known limitations

These limitations are on my to-do list to improve.

- Reddit comment sub-threads that are hlabelden under a comment fold (with a "load more comments" link) are ignored
- Hyperlinks in HN threads are not rendered in full
- The search command only takes in one search string at a time
- Filters for searching cannot be combined, e.g. you can search either by a tag or by source

## Contributing

I'm not currently accepting any pull requests, but questions and suggestions are more than welcome. 


## Disclaimer

`filum` is alpha software and far from stable. Please do not rely solely on `filum` for archival&mdash;at the very least bookmark the page or use the save feature on the respective platforms.