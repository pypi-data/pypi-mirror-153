![build](https://img.shields.io/bitbucket/pipelines/omniviant/scrapekit/master)
![package version](https://img.shields.io/pypi/v/scrapekit)
![wheel](https://img.shields.io/pypi/wheel/scrapekit)
![python versions](https://badgen.net/pypi/python/scrapekit)

# scrapekit
Modular scraping convenience framework.

**Convenience Methods**:

- `scrapekit.common.get_user_agent(os, browser)`: Returns a random User-Agent string.
  - Can filter by OS and browser

**Proxy Provider Module List**:

- [IP Burger](https://secure.ipburger.com/aff.php?aff=1479&page=residential-order)

## Installation
```shell
pip install scrapekit
```

## Usage Examples

**Simple proxified session**

```python
import scrapekit

session = scrapekit.ipburger.make_session('MyIPBurgerUsername")

res = session.get('https://icanhazip.com')
print(res.status_code, res.text)
# 200 89.46.62.37
```

**Proxified session with random Windows Firefox User-Agent**:

```python
import scrapekit

user_agent = scrapekit.common.get_user_agent(os='Windows', browser='Firefox')
session = scrapekit.ipburger.make_session(
    'MyIPBurgerUsername',
    headers={'User-Agent': user_agent}
)
```