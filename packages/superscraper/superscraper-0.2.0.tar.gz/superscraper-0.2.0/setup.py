# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['superscraper']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'selenium>=4.2.0,<5.0.0',
 'webdriver-manager>=3.7.0,<4.0.0']

setup_kwargs = {
    'name': 'superscraper',
    'version': '0.2.0',
    'description': 'the friendliest scraper around',
    'long_description': "# Super Scraper\nScraping couldn't get much easier.  \n\n**Super Scraper** is built with ease in mind - for those hard to scrape places. It drives with Selenium and parses with BeautifulSoup4. I've provided some convenience methods to make common actions even easier for you.\n\n# Example\n\n```\nfrom superscraper import SuperScraper, By\n\nscraper = SuperScraper(show_process=True)\nscraper.search('https://www.google.com')\nscraper.fill_in(By.NAME, 'q', 'hello world')\nscraper.click(By.NAME, 'btnK')\n\nsearch_results = scraper.driver.find_elements(By.CLASS_NAME, 'g')\nfor result in search_results:\n\n    title = scraper.attempt(result.find_element, By.TAG_NAME, 'h3')\n    if title:\n        print(title.text)\n        a = result.find_element(By.TAG_NAME, 'a')\n        scraper.open_new_tab(By.LINK_TEXT, a.text)\n        scraper.close_current_tab(switch_to_tab=-1)\n```",
    'author': 'MBeebe',
    'author_email': 'grow.food.everywhere@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
