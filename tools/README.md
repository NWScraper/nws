### Tools

## check_url.py

This script can be used to check the status codes of a list of websites.

1. Create a file named `urls.txt`, which contains the web addresses of the websites to test, one per line.
Make sure this file is placed in the same directory as `check_url.py`.

1. Open `check_url.py` with IDLE, or create a new file and paste its contents in there.

1. In IDLE, click `Run > Run module`. Save the file if prompted.

1. After the script is done running, a new file should appear in the same directory, named `check_url.csv`.
HTTP-status code 200 means the site is functioning properly, anything else might indicate a problem.


## search_url.py

This script can be used to find the first Google results of batch of queries.

1. search_terms.txt

1. Create a file named `search_terms.txt`, which contains the search terms you would like use, one query per line.
You could for instance use a list of the names of general practices you would like to find the web address for.
Make sure this file is placed in the same directory as `search_url.py`.

1. This script requires an external module to function.
Install the package or manually download it from https://github.com/MarioVilas/googlesearch and place the folder `googlesearch` in the same directory as `search_url.py`.

1. Open `search_url` with IDLE, or create a new file and paste its contents in there.

1. In IDLE, click `Run > Run module`. Save the file if prompted.

1. After the script is done running, a new file should appear in the same directory, named `search_url.csv`.

