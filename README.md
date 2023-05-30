# xpath-filter

[![version](https://img.shields.io/badge/version-0.1.0-blue)](https://pypi.org/project/xpath-filter)

Filter HTML files using xpath mappings.

## Installation

Install `xpath-filter` using pip:

```shell
pip install xpath-filter
```

## Usage

Import the `xpath_filter` function from the `xpath_filter` module. Find below
some use cases.

### Filtering HTML file

```python
>>> xpaths = {
...     'article': {
...         'xpath': '//div[@class="article"]',
...         'matches': 'all',
...         'elements': {
...             'author': './@data-author',
...             'content': './p/text()'
...         }
...     }
... }
>>> xpath_filter('index.html', xpaths)
```

Result

```python
{'article': [{'author': 'Ana', 'Content': 'Awesome'}, {'author': 'Bob', 'Content': 'Bad'}]}
```

### Filtering HTML file from a YAML xpaths definition.

File at "xpaths.yml":

```yml
article:
    xpath: //div[@class="article"]
    matches: first
    elements:
        author: './@data-author'
        content: ./p/text()
```

Code:

```python
>>> xpath_filter('index.html', 'xpaths.yml')
```

Result

```python
{'article': [{'author': 'Ana', 'Content': 'Awesome'}, {'author': 'Bob', 'Content': 'Bad'}]}
```

### Simplified filtering

By definining only the xpath of an HTML element, only its first match is returned and no inner element is searched.

```python
>>> xpath_filter('index.html', {'article': '//div[@class="article"]'})
>>> xpath_filter('index.html', {'article': '//div[@class="article"]/p/text()'})
```

Result

```python
{'article': <Element div at 0x1f08369ea80>}
{'article': 'Awesome'}
```
