import re

from urllib.request import urlopen
from html.parser import HTMLParser


CODEFORCES_HOME = 'https://codeforces.com'
CONTEST_URL_TEMPLATE = 'https://codeforces.com/contest/{}'


class ContestParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self._problems = set()
        self._started = False

    @property
    def problems(self):
        return list(self._problems)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'table' and attrs.get('class') == 'problems':
            self._started = True
        elif (tag == 'a' and self._started and
              re.match(r'^/contest/\d+/problem/.*$', attrs.get('href'))):
            self._problems.add(attrs.get('href'))

    def handle_endtag(self, tag):
        if tag == 'table' and self._started:
            self._started = False


class ProblemParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self._tests = []
        self._started_input = False
        self._started_output = False
        self._parse_data = False
        self._was_pre_tag = False
        self._current_test = {}

    @property
    def tests(self):
        return self._tests

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div':
            css_class = attrs.get('class')
            if css_class == 'input':
                self._started_input = True
                self._parse_data = True
            elif css_class == 'output':
                self._started_output = True
                self._parse_data = True
        elif tag == 'pre' and self._parse_data:
            self._was_pre_tag = True

    def handle_data(self, data):
        if self._was_pre_tag:
            if self._started_input:
                self._current_test['input'] = data.strip('\n')
            elif self._started_output:
                self._current_test['output'] = data.strip('\n')

    def handle_endtag(self, tag):
        if tag == 'div' and not self._parse_data:
            if self._started_input:
                self._started_input = False
            elif self._started_output:
                self._started_output = False
                self._tests.append(self._current_test.copy())
                self._current_test = {}
        elif tag == 'pre' and self._parse_data:
            self._parse_data = False
            self._was_pre_tag = False


def _name_from_url(url):
    return url.split('/')[-1]


def parse(contest):
    result = {}
    with urlopen(CONTEST_URL_TEMPLATE.format(contest)) as response:
        contest_html_content = response.read()
    contest_parser = ContestParser()
    contest_parser.feed(contest_html_content.decode('utf-8'))
    for problem_url in contest_parser.problems:
        with urlopen(f'{CODEFORCES_HOME}/{problem_url}') as response:
            problem_html_content = response.read()
        problem_parser = ProblemParser()
        problem_parser.feed(problem_html_content.decode('utf-8'))
        result[_name_from_url(problem_url)] = problem_parser.tests
    return result
