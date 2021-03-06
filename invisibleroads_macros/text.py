import re
import sys


WHITESPACE_PATTERN = re.compile(r'\s+', re.MULTILINE)
PUNCTUATION_PATTERN = re.compile(r'[^a-zA-Z\s]+')


def compact_whitespace(string):
    return WHITESPACE_PATTERN.sub(' ', string).strip()


def cut_and_strip(x, separator):
    head, separator, tail = x.partition(separator)
    return head.strip(), tail.strip()


def has_whitespace(string):
    return WHITESPACE_PATTERN.search(string) is not None


def parse_words(x):
    return x.replace(',', ' ').split()


def remove_punctuation(string):
    return compact_whitespace(PUNCTUATION_PATTERN.sub(' ', string))


def strip_whitespace(string):
    return WHITESPACE_PATTERN.sub('', string)


def unicode_safely(x):
    # http://stackoverflow.com/a/23085282/192092
    try:
        return x.decode(sys.getfilesystemencoding())
    except (AttributeError, UnicodeEncodeError):
        return x
