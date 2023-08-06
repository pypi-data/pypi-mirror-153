""" Parse html to extract structured NLP data """
import html2text


def html2md(html_text: str, **kwargs):
    """ Use html2text (and bs4) to convert HTML str to markdown text (str)"""
    parser = html2text.HTML2Text(**kwargs)
    parser.feed(html_text)
    return parser.finish()
