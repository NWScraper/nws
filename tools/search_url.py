"""
Script to check if sites are responding.
:var str input_file: Path to input TXT file (one search query per line)
:var str output_file: Path to CSV output file to create
"""
import csv
from urllib.parse import urlparse
from googlesearch import search  # https://github.com/MarioVilas/googlesearch

# files used:
input_file = "search_terms.txt"
output_file = "search_url2.csv"

with open(input_file, 'rb') as f:  # open input_file
    queries = f.readlines()  # split on lines


result = []
queries = [q.decode('utf-8') for q in queries]
print(queries)

for query in queries:
    query = str(query).strip()
    print(query, end=' ')
    sites = []
    if query:
        srch = search(query, stop=3)
        netlocs = []
        for url in srch:
            netloc = urlparse(url).netloc
            if netloc not in netlocs:
                sites.append(url)
                netlocs.append(netloc)
            if len(sites) > 3:
                break
        while len(sites) < 3:
            sites.append('')
        print(sites[0])
        result.append([query] + sites)


# write to CSV
with open(output_file, 'w+') as f:  # open output_file
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["query", "top result", "result 2", "result 3"])  # write header
    n = 0
    for row in result:
        row = [i.encode('utf-8') for i in row]
        print(n, row)
        n += 1
        writer.writerow(row)

print("done!")
