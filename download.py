import argparse
import os.path
import urllib.request
import requests
from bs4 import BeautifulSoup

from writable_dir import WritableDir


my_parser = argparse.ArgumentParser(description='CourseHunter downloader')

my_parser.add_argument('--e_mail',
                       metavar='e_mail',
                       type=str,
                       help='User email',
                       required=True)

my_parser.add_argument('--password',
                       metavar='password',
                       type=str,
                       help='User password',
                       required=True)

my_parser.add_argument('--url',
                       metavar='url',
                       type=str,
                       help='Course url, which you want to download',
                       required=True)

my_parser.add_argument('--out',
                       metavar='out',
                       type=str,
                       action=WritableDir,
                       help='Output directory',
                       required=True)

args = my_parser.parse_args()

data = {
    'e_mail': args.e_mail,
    'password': args.password
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

proxyDict = {
    "https": 'http://127.0.0.1:8080'
}

# Create the session and set the proxies.
session = requests.Session()
# session.proxies = proxyDict # for debugging
# session.verify = False

r = session.post(url='https://coursehunter.net/sign-in', headers=headers, data=data)

r = session.get(url=args.url)

print("*** Starting parsing url {}...".format(args.url))

soup = BeautifulSoup(r.content, 'html.parser')
rawUrls = soup.find_all("link", attrs={"itemprop": "contentUrl"})
rawDescriptions = soup.find_all("meta", attrs={"itemprop": "description"})
urls = [tag.get('href') for tag in rawUrls][:3]
descriptions = [tag.get('content') for tag in rawDescriptions]

print("Retrieved {} files.".format(len(urls)))

for i in range(len(urls)):
    file = urls[i]
    file_index = '{:0>{}}. '.format(i + 1, len(str(len(urls))) + 1)
    local_file_name = os.path.join(args.out, file_index + descriptions[i] + ".mp4")

    print("Status: {}/{} {:.2f}%".format(i, len(urls), i / len(urls)), end='. ')
    print("Start downloading file %s to %s " % (file, local_file_name))
    urllib.request.urlretrieve(file, local_file_name)

print("Finished!!! Total downloads: %s" % len(urls))
