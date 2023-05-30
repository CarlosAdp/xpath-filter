from pathlib import Path
from typing import Union

import lxml.html
import yaml


def xpath_filter(
    html: Union[lxml.html.HtmlElement, str, Path],
    xpaths: Union[dict, str, Path]
) -> dict:
    '''Filters HTML using xpaths.

    :param html: HTML document. It can be either the path to an HTML file, the
    literal document as string or a :class:`lxml.html.HtmlElement` instance.
    :type html: str or :class:`lxml.html.HtmlElement`
    :param xpaths: Mappings from named html elements to their xpath locations.
    Argument can be either a dictionary or the path to a yml file.

    .. note::

        Each mapping is a key-value pair where the key is the name of the html
        element and the value is the element's definition, including the
        following attributes:

        - "xpath": the element's xpath location
        - "matches": either "first" to return only first match or "all" to
        return all of them. Defaults to "first"
        - "elements": optional recursive attribute to map inner elements.

    Example::

        article:
            xpath: //div[@class = "article"]
            matches: first
            elements:
                title: ./@data-title
                author: ./@data-author
                body:
                    xpath: ./p/text()
                    matches: all

    .. note::
        Optionally, one node can be represented as a simple key-value pair,
        where the value is the xpath location. In this case, "matches" defaults
        to "first" and element has no inner nodes (leaf).

    Example::

        article: //div[@class = "article"]/p/text()

    :type xpaths: dict or str or Path
    :returns: A dictionary of filtered HTML elements.
    :rtype: dict
    :raises ValueError: If xpaths is not a valid YAML file
    '''

    if isinstance(html, (str, Path)):
        path = Path(html)
        if path.is_file():
            html = lxml.html.fromstring(path.read_text(encoding='utf-8'))
        else:
            html = lxml.html.fromstring(html) if html else None

    if isinstance(xpaths, (str, Path)):
        path = Path(xpaths)
        if path.is_file():
            try:
                xpaths = yaml.safe_load(path.read_text())
            except yaml.parser.ParserError:
                raise ValueError(f'Invalid yaml file: {path}')
        else:
            raise ValueError(f'File does not exist: {path}')

    return _xpath_filter(html, xpaths)


def _xpath_filter(
    html: lxml.html.HtmlElement,
    xpaths: dict
):
    '''Filters HTML using xpaths.'''
    if xpaths is None:
        return html

    if html is None:
        return None

    res = {}

    for elem, definition in xpaths.items():
        if isinstance(definition, str):
            definition = {'xpath': definition}

        xpath = definition.get('xpath')
        n_matches = definition.get('matches', 'first')
        elements = definition.get('elements')

        matches = html.xpath(xpath)

        if n_matches == 'first':
            match = matches[0] if matches else None
            res[elem] = _xpath_filter(match, elements)
        else:
            res[elem] = [_xpath_filter(match, elements) for match in matches]

    return res
