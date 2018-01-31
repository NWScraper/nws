import time
import crawler
import reader
import writer
import window
import datetime
import random

def test1():
    """Running v1 threaded with async"""
    tag = "threaded async"
    order = [i for i in range(1, 11)]
    random.shuffle(order)
    result = []
    for n in order + [order[0]]:
        start_time = time.time()
        wcc = crawler.Controller(file="NZR500.txt", last_line=100)
        # wcc.run()
        wcc.threaded_run(threads=n)
        stop_time = time.time()
        date_string = datetime.datetime.now().strftime('%c')
        s = f"{n}, {int(stop_time - start_time)}, {date_string}, {tag}\n"
        result.append(s)
        #with open('test_results.csv', 'a') as f:
        #    f.write(s)
        print(s)
    result.sort()
    with open('test_results.csv', 'a') as f:
        for line in result:
            f.write(line)

def test2():
    """Running v1 using only the WebCrawler class"""
    webcrawler = crawler.WebCrawler(url="debeukenhuisartsen.praktijkinfo.nl")
    webcrawler.crawl()
    entry = webcrawler.html[0]
    print('html\'s:', len(webcrawler.html))

    r = reader.Reader(entry['html'], entry['url'])
    r.test()

def test3():
    """Running v1 using the Controller"""
    start_time = time.time()
    wcc = crawler.Controller(file="NZR500.txt", last_line=100)
    wcc.threaded_run()
    stop_time = time.time()
    date_string = datetime.datetime.now().strftime('%c')
    s = f"Collected sites. {int(stop_time - start_time)} seconds, {date_string}\n"
    print(s)

    start_time = time.time()
    w = writer.SiteWriter(entrylist=wcc.html)
    w.save()
    stop_time = time.time()
    date_string = datetime.datetime.now().strftime('%c')
    s = f"Written files. {int(stop_time - start_time)} seconds, {date_string}\n"
    print('\n', s)

def test4():
    """Running v1 using the GUI"""
    app = window.App(crawler, title="Nivel")
    app.start()



if __name__ == '__main__':
    start_time = time.time()
    test4()
    print(f"seconds: {int(time.time() - start_time)}")


