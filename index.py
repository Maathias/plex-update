import sys
import os
import json
import urllib
from datetime import datetime

response = urllib.urlopen("https://plex.tv/pms/downloads/5.json")
data = json.loads(response.read())
usefull = data['computer']['Linux']

os.system(
    '(dpkg -s plexmediaserver 2>/dev/null || echo "Version: none") | grep Version')

print "Newest version:", usefull['version']
print "Release date:", datetime.utcfromtimestamp(
    int(usefull['release_date'])).strftime('%Y-%m-%d %H:%M:%S')

switch = {
    "debian": 0,
    "debian32": 0,
    "debian64": 1,
    "debianarmv8": 2,
    "debianarmv7": 3,
    "redhat": 4,
    "redhat32": 4,
    "redhat64": 5,
}

version = switch[(sys.argv[1] if len(sys.argv)>1 else 'debian')+(sys.argv[2] if len(sys.argv)>2 else '32')]

print "Platform:", usefull['releases'][version]['label']

ok = raw_input("Correct? [Y/n]: ")
if ok == 'n' or ok == 'N':
	exit()

os.system('wget '+usefull['releases'][version]['url'] +
          ' -O plexmediaserver-'+usefull['version'])

os.system('sudo dpkg -i '+'plexmediaserver-'+usefull['version'])
