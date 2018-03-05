"""
Script to check if sites are responding.
:var str input_file: Path to input TXT file (one URL per line)
:var str outpu_file: Path to CSV output file to create
"""
import urllib.request
import csv
import ssl

# files used:
input_file = "urls.txt"
output_file = "check_url.csv"

with open(input_file, 'r') as f:  # open input_file
    sites = f.readlines()  # split on lines

result = []
n = 1
print('lines:', len(sites))
for url in sites:
    url = url.strip()
    if url:
        if '://' not in url:  # add URL-scheme if missing
            new_url = ''.join(['http://', url])
        print(n, new_url, end=' ')
        try:
            req = urllib.request.Request(new_url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            })
            res = urllib.request.urlopen(req)
        except Exception as e:
            res.code = e
        print(res.code)
        if url == new_url:
            new_url = ''
        result.append([url, new_url, res.code])
        n += 1

# write to CSV
with open(output_file, 'w+') as f:  # open output_file
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["URL", "URL used", "result"])  # write header
    for row in result:
        writer.writerow(row)

print("done!")
