import sys
import re
import html
import unidecode
import string
from string import digits

from typing import Optional, List

from bs4 import BeautifulSoup


class TextCleaner:
    REMOVE_HTML_TAGS = "remove_html_tags"
    DECODE_HTML_ENTITIES = "decode_html_entities"
    REPLACE_ACCENTED = "replace_accented"
    REPLACE_UNICODE_NBSP = "replace_unicode_nbsp"
    REPLACE_NEWLINES_TABS = "replace_newlines_tabs"
    REMOVE_EXTRA_QUOTATION = "remove_extra_quotation"
    REMOVE_EXTRA_WHITESPACES = "remove_extra_whitespaces"
    REMOVE_URLS = "remove_urls"
    REMOVE_PUNCTUATION = "remove_punctuation"
    LOWERCASE = "lowercase"
    REMOVE_DIGITS = "remove_digits"

    def __init__(self):
        self._steps = [
            self.REMOVE_HTML_TAGS,
            self.DECODE_HTML_ENTITIES,
            self.REPLACE_ACCENTED,
            self.REPLACE_UNICODE_NBSP,
            self.REPLACE_NEWLINES_TABS,
            self.REMOVE_EXTRA_QUOTATION,
            self.REMOVE_URLS,
            self.REMOVE_PUNCTUATION,
            self.LOWERCASE,
            self.REMOVE_DIGITS,
            self.REMOVE_EXTRA_WHITESPACES,
        ]

    def clean(
        self,
        text: str,
        steps: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None
    ) -> str:

        text = text.strip()
        
        if not steps:
            steps = self._steps

        if exclude:
            steps = [step for step in steps if step not in exclude]

        for step in steps:
            try:
                step_function = getattr(sys.modules[__name__], f"_{step}")
            except AttributeError:
                continue

            text = step_function(text)

        return text


def _remove_html_tags(text: str) -> str:
    """ Removes html tags """
    soup = BeautifulSoup(text, "html.parser")

    return soup.get_text(separator=" ")
    

def _decode_html_entities(text: str) -> str:
    """ Converts html entities in the corresponding unicode string"""
    return html.unescape(text)


def _remove_extra_whitespaces(text: str) -> str:
    """ Removes extra whitespaces """
    pattern = re.compile(r'\s+')

    return re.sub(pattern, " ", text)


def _replace_accented(text: str) -> str:
    """ Removes all accented characters"""
    return unidecode.unidecode(text)


def _replace_unicode_nbsp(text: str) -> str:
    """ Removes unicode whitespaces"""
    return text.replace(u'\xa0', u' ')


def _remove_extra_quotation(text: str) -> str:
    """ Removes extra quotation marks """
    text = re.sub(r'\"{2,}', '"', text)

    return re.sub(r'\'{2,}', "'", text)


def _replace_newlines_tabs(text: str) -> str:
    """ Removes all the occurrences of newlines, tabs, and combinations like: \\n, \\. """
    text = text.translate(str.maketrans("\n\r", "  "))

    return text.replace("\\n", " ").replace("\t", " ").replace("\\", " ")


def _remove_urls(text: str) -> str:
    """ Removes all urls from text"""
    pattern = r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?'

    return re.sub(pattern, '', text, flags=re.MULTILINE)


def _remove_punctuation(text: str) -> str:
    """ Removes punctuation from text """
    punctuation = string.punctuation + '¿¡'
    table = str.maketrans('', '', punctuation)
    words = text.split()

    stripped = [word.translate(table) for word in words]

    return ' '.join(stripped)


def _lowercase(text: str) -> str:
    """ Transform text to lowercase"""
    return text.lower()


def _remove_digits(text: str) -> str:
    """ Remove digits from text"""
    table = str.maketrans('', '', digits)

    return text.translate(table)
