"""
Script to check if sites are responding.
:var str input_file: Path to input TXT file (one URL per line)
:var str outpu_file: Path to CSV output file to create
"""
import urllib.request
import urllib.error
import csv

# files used:
input_file = "input.txt"
output_file = "output.csv"

with open(input_file, 'r') as f:  # open input_file
    sites = f.readlines()  # split on lines

result = []
for url in sites:
    url = url.strip()
    if url:
        if '://' not in url:  # add URL-scheme if missing
            new_url = ''.join(['http://', url])
        print(new_url, end=' ')
        try:
            req = urllib.request.urlopen(new_url)
        except urllib.error.URLError as e:
            req.code = e
        print(req.code)
        if url == new_url:
            new_url = ''
        result.append([url, new_url, req.code])

# write to CSV
with open(output_file, 'w+') as f:  # open output_file
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["URL", "URL used", "result"])  # write header
    for row in result:
        writer.writerow(row)

print("done!")
