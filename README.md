### NWS

This is a webscraper made with Python 3.



#### Installating the application
- Make sure Python3 is installed, download this repository and enter the folder from the commandline.

- optionally you can use a virtual environment to create an isolated Python environment. To do so run:
    - Install [Virtualenv](https://virtualenv.pypa.io/en/stable/): `pip install virtualenv`
    - Create a new virtual environment named ENV. The -p flag ensures the correct version of Python is used: 
    `virtualenv ENV -p python3`
    - Enter the virtual environment and continue this guide: `source ENV/bin/activate`

- Install the Python dependencies: `pip3 install -r requirements.txt`

#### Running the application
Run `python3 run.py`. If installed correctly, a new window will pop-up. Also, two new directories will be created, 
namely `results` and `templates`.   
Here you can specify the settings for the crawler. Pressing the `input`-button allows you to select a file with start 
URL's. The file you'll select should be a TXT-file, containing one web address per line.  
Using the `template`-button, you can specify which template to use for retrieving information from the sites.
This should be a JSON file. Creating new template files can be done using the 
[webscraper Chrome plug-in](http://webscraper.io).
The `output`-button opens the directory in which the extracted data will appear as a CSV file, after the crawler is done
running.  
After selecting an input and output file, the `start`-button can be pressed. The configuration window will close and the
crawling progress can be watched from the commandline window.  When completed, a new file will appear in the output
directory with the retrieved information.


