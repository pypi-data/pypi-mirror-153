import requests
import html2text
import logging
import xml.etree.ElementTree as ElementTree
import concurrent.futures


log = logging.getLogger(locals().get('__name__'))

FEED_URL = "https://news.google.com/rss/topics/CAAqHAgKIhZDQklTQ2pvSWJHOWpZV3hmZGpJb0FBUAE"  # local news
# world news:"https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB"
TIMEOUT = 4
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.114 Safari/537.36",
}


def get_news_stories_text():
    stories = get_rss_feed_stories()

    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        for story in stories:
            for article_url in story["urls"]:
                executor.submit(get_article, article_url, story)

    return stories


def get_rss_feed_stories():
    response = requests.get(FEED_URL)
    tree = ElementTree.fromstring(response.text)
    channel = tree[0]

    stories = []

    for item in channel[8:]:  # skips metadata at start of feed
        title = item[0].text.rpartition("-")[0][:-1]  # removes news outlet name from headline + trailing space
        article_urls = []

        # nbsp definition needed to parse, always needs root node so added for single link stories
        xml_string = "<!DOCTYPE xml [<!ENTITY nbsp ' '>]><root>" + item[4].text + "</root>"

        # ridiculous that google doesn't escape special characters
        xml_string = xml_string.replace("&nbsp;", '')
        xml_string = xml_string.replace("&", "&amp;")

        description = ElementTree.fromstring(xml_string)[0]   # [0] index undoes root tag adding from above

        if description.tag == "ol":
            for list_item in description[:-1]:    # ordered list tag, last item is GNews story link so need to skip
                article_urls.append(list_item[0].attrib["href"])
        elif description.tag == "a":    # only one source covering the story
            article_urls.append(description.attrib["href"])
        stories.append({"title": title, "urls": article_urls, "articles": []})

    return stories


def get_article(url, story):
    text = get_article_content(url)

    if text is not None:
        story["articles"].append(text)


def get_article_content(url):
    log.info("Requesting " + url)

    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    except requests.exceptions.RequestException as e:
        log.debug("Timed out requesting " + url)
        log.warning(e)
        return

    if response.status_code != 200:
        log.debug("Received " + str(response.status_code) + " from " + url)
        return

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_emphasis = True
    text_maker.ignore_images = True
    text_maker.ignore_tables = True

    text = response.text
    summary = text[:256]
    return text_maker.handle(summary)
