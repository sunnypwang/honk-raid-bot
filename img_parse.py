import urllib.request
web = urllib.request.urlopen(
    'https://www.serebii.net/swordshield/galarpokedex.shtml')

for line in web:
    line = line.decode()
    if 'Grookey' in line:
        print(line)
