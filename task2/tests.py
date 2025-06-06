from unittest.mock import patch, Mock
from solution import parse_animals

HTML_PAGE_1 = '''
<div class="mw-category-group">
    <a href="/animal1">Аист</a>
    <a href="/animal2">Заяц</a>
    <a href="/animal3">Знаменитые животные по алфавиту</a>
</div>
<a href="/page2">Следующая страница</a>
'''

HTML_PAGE_2 = '''
<div class="mw-category-group">
    <a href="/animal4">Ёж</a>
    <a href="/animal5">Жираф</a>
</div>
'''

HTML_PAGE_3 = '''
<div class="mw-category-group">
    <a href="/animal6">Aardvark</a>  <!-- Англоязычное название, должно остановить цикл -->
</div>
'''
HTML_EMPTY = '''
<div class="mw-category-group">
</div>
'''

HTML_NO_NEXT = '''
<div class="mw-category-group">
    <a href="/animal1">Ягуар</a>
    <a href="/animal2">Зебра</a>
</div>
'''

HTML_WITH_STOP_WORDS = '''
<div class="mw-category-group">
    <a href="/animal1">Знаменитые животные по алфавиту</a>
    <a href="/animal2">Породы по алфавиту</a>
    <a href="/animal3">Ящерица</a>
</div>
'''


def mock_requests_get(url):
    mock_resp = Mock()
    if url.endswith("page2"):
        mock_resp.text = HTML_PAGE_2
    elif url.endswith("page3"):
        mock_resp.text = HTML_PAGE_3
    else:
        mock_resp.text = HTML_PAGE_1
    return mock_resp


def mock_requests_get_multiple(url):
    mock_resp = Mock()
    if url.endswith("empty"):
        mock_resp.text = HTML_EMPTY
    elif url.endswith("nonext"):
        mock_resp.text = HTML_NO_NEXT
    elif url.endswith("stopwords"):
        mock_resp.text = HTML_WITH_STOP_WORDS
    else:
        mock_resp.text = HTML_PAGE_1
    return mock_resp


@patch('requests.get', side_effect=mock_requests_get_multiple)
def test_parse_animals_empty_category(mock_get):
    site = "https://example.com"
    url = site + "/empty"

    result = parse_animals(site, url)
    assert result == {}


@patch('requests.get', side_effect=mock_requests_get_multiple)
def test_parse_animals_no_next_page(mock_get):
    site = "https://example.com"
    url = site + "/nonext"

    result = parse_animals(site, url)
    expected = {'Я': 1, 'З': 1}
    assert result == expected


@patch('requests.get', side_effect=mock_requests_get_multiple)
def test_parse_animals_ignore_stop_words(mock_get):
    site = "https://example.com"
    url = site + "/stopwords"

    result = parse_animals(site, url)
    expected = {'Я': 1}
    assert result == expected


@patch('requests.get', side_effect=mock_requests_get_multiple)
def test_parse_animals_multiple_groups(mock_get):
    site = "https://example.com"
    url = site + "/multiple"

    html_multiple = '''
    <div class="mw-category-group">
        <a href="/animal1">Утка</a>
        <a href="/animal2">Фламинго</a>
    </div>
    <div class="mw-category-group">
        <a href="/animal3">Хомяк</a>
        <a href="/animal4">Цапля</a>
    </div>
    '''
    mock_resp = Mock()
    mock_resp.text = html_multiple

    with patch('requests.get', return_value=mock_resp):
        result = parse_animals(site, url)

    expected = {'У': 1, 'Ф': 1, 'Х': 1, 'Ц': 1}
    assert result == expected
