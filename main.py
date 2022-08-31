import bs4
import os
import requests
import re
import sys

url = 'https://existentialcomics.com/'  # starting url
os.makedirs('existential-comics', exist_ok=True)  # store comics in ./existential-comics

res = requests.get(url)
soup = bs4.BeautifulSoup(res.text, 'html.parser')
number = soup.select('.permalink')
number = int(str(number[0])[87:][:-4])

while number > 0:

    # Download the page.

    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Find the URL of the comic image and download the image.

    # Save the image to ./existential-comics and get the Prev button's url.

    comicElem = soup.select('.comicImg')
    if not comicElem:
        print('Could not find comic image.')
    else:
        for i in range(len(comicElem)):
            comicUrl = 'https:' + comicElem[i].get('src')
            # Download the image.
            print('Downloading image %s...' % comicUrl)
            res = requests.get(comicUrl)
            res.raise_for_status()
            if os.path.exists(os.path.join('existential-comics', str(number) + " - " + os.path.basename(comicUrl))):
                number = number - 1
                url = 'https://existentialcomics.com/comic/' + str(number)
                print('Done.')
                sys.exit()
            imageFile = open(os.path.join('existential-comics', str(number) + " - " + os.path.basename(comicUrl)),
                             'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

    altText = soup.select('.altText')
    if not altText:
        print('Could not find alt text.')
    else:
        alt = altText[0].getText()
        textFile = open(os.path.join('existential-comics', str(number) + " - " + "Alt Text" + ".txt"),
                    'w', encoding='utf-8')
        textFile.write(alt)
        textFile.close()

    explanation = soup.select('#explanation')
    if not explanation:
        print('Could not find explanation.')
    else:
        exp = explanation[0].getText()
        exp = re.compile(r'<.*?>').sub('', exp)
        textFile = open(os.path.join('existential-comics', str(number) + " - " + "Explanation" + ".txt"),
                    'w', encoding='utf-8')
        textFile.write(exp)
        textFile.close()

    number = number - 1
    url = 'https://existentialcomics.com/comic/' + str(number)

print('Done.')