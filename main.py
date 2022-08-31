import os
import requests
import bs4
import re
import sys

url = 'https://existentialcomics.com/'  # starting url
os.makedirs('existential-comics', exist_ok=True)  # store comics in ./existential-comics

res = requests.get(url)
soup = bs4.BeautifulSoup(res.text, 'html.parser')
number_tag = soup.select('.permalink')[0]      # get the tag containing the number of the last comic
number = int(number_tag.getText()[-3:])        # extract the number


while number > 0:

    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    comicElem = soup.select('.comicImg')
    if not comicElem:
        print('Could not find comic image.')
    else:
        for i in comicElem:                         # some comics consist of two or more images
            comicUrl = 'https:' + i.get('src')
            print('Downloading image %s...' % comicUrl)
            res = requests.get(comicUrl)
            res.raise_for_status()
            destination = os.path.join('existential-comics', str(number) + " - " + os.path.basename(comicUrl))

            # check if comic has already been downloaded
            if os.path.exists(destination):
                print('Done.')
                sys.exit()

            # download the comic
            imageFile = open(destination, 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

    # get the alt text of the comic
    altText = soup.select('.altText')
    if not altText:
        print('Could not find alt text.')
    else:
        alt = altText[0].getText()
        textFile = open(os.path.join('existential-comics', str(number) + " - " + "Alt Text" + ".txt"),
                        'w', encoding='utf-8')
        textFile.write(alt)
        textFile.close()

    # get the explanation of the comic
    explanation = soup.select('#explanation')
    if not explanation:
        print('Could not find explanation.')
    else:
        exp = explanation[0].getText()
        exp = re.compile(r'<.*?>').sub('', exp)     # remove HTML tags from the explanation
        textFile = open(os.path.join('existential-comics', str(number) + " - " + "Explanation" + ".txt"),
                        'w', encoding='utf-8')
        textFile.write(exp)
        textFile.close()

    number = number - 1
    url = 'https://existentialcomics.com/comic/' + str(number)

print('Done.')
