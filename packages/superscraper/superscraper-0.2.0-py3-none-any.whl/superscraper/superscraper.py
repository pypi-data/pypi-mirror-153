import bs4
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import atexit
import typing

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class SuperScraper:

    def __init__(self, show_process=False, incognito=True, downloads_path=None):
        self.base_url: str = ""
        self.session = None
        self.cookies: list = list()
        self.driver = None
        self.parser = None
        self.__setup_selenium(
            show_process=show_process,
            incognito=incognito,
            downloads_path=downloads_path)
        atexit.register(self.close)

    def __setup_selenium(self, show_process=False, incognito=True, downloads_path=None):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        if incognito:
            options.add_argument('--incognito')
        if not show_process:
            options.add_argument('--headless')
        if downloads_path:
            prefs = {"download.default_directory" : downloads_path}
            options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=options)

    def set_base_url(self, url):
        self.base_url = url

    def search(self, query: str = ''):
        if query.startswith('http'):
            urlstring = query
        elif not self.base_url and not query.startswith('http'):
            return 'URL ERROR'
        else:
            urlstring = self.base_url + query
        self.driver.get(urlstring)
        self.make_soup()

    def make_soup(self):
        page_source = self.driver.page_source
        self.parser = bs4.BeautifulSoup(
            page_source,
            features="html.parser")
        return self.parser

    def raw_html(self):
        return self.parser.prettify()

    def images(self, src_only=False):
        imgs = self.parser.find_all('img')
        if src_only:
            return [x.get('src') for x in imgs]
        else:
            return imgs

    def links(self):
        return self.parser.find_all('a')

    def xpath(self, tag, attr, value):
        return f"//{tag}[@{attr}='{value}']"

    def parse_xpath(self, element):
        # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:  # type: bs4.element.Tag
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name if 1 == len(siblings) else '%s[%d]' % (
                    child.name,
                    next(i for i, s in enumerate(siblings, 1) if s is child)
                    )
                )
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)

    def click(self, by: By, value, timeout: int=5, new_tab: bool=False):
        el = self.wait(
            expect.visibility_of_element_located,
            (by, value),
            timeout=timeout)
        if new_tab:
            el.send_keys(Keys.CONTROL + Keys.RETURN)
        else:
            el.click()

    def open_new_tab(self, by: By, value, timeout: int=5, switch_to: bool=True):
        self.click(by, value, timeout, new_tab=True)
        if switch_to:
            self.switch_tabs(-1)

    def fill_in(self, by: By, value, content, clear: bool=False, timeout: int=5):
        el = self.wait(
            expect.visibility_of_element_located,
            (by, value),
            timeout=timeout)
        if clear:
            el.clear()
        el.send_keys(content)

    def switch_tabs(self, index: int=-1, make_soup: bool=True):
        self.driver.switch_to.window(
            self.driver.window_handles[index])
        if make_soup:
            self.make_soup()
    
    def close_current_tab(self, switch_to_tab=-1):
        self.driver.close()
        self.switch_tabs(switch_to_tab)

    def wait(self, condition, element_tuple, timeout: int=5, poll_frequency: float=0.2, graceful: bool=False):
        # condition = expected_conditions.[condition]
        # element_tuple = (By.ID, 'idElement')
        if graceful:
            return self.graceful_wait(condition, element_tuple, timeout, poll_frequency)
        waiter = WebDriverWait(
            self.driver,
            timeout=timeout,
            poll_frequency=poll_frequency)
        return waiter.until(condition(element_tuple))

    def graceful_wait(self, condition, element_tuple, timeout: int=5, poll_frequency: float=0.2, default=None):
        try:
            return self.wait(condition, element_tuple, timeout, poll_frequency, graceful=False)
        except:
            return default

    def get(self, by: By, value, many: bool=False, timeout: int=5, default=None):
        condition = getattr(
            expect,
            f'presence_of_{"all_elements" if many else "element"}_located')
        return self.graceful_wait(
            condition=condition,
            element_tuple=(by, value),
            timeout=timeout,
            default=default)
    
    def attempt(self, action, *args, **kwargs):
        try:
            res = action(*args, **kwargs)
        except:
            res = None
        return res

    def close(self):
        self.driver.quit()
 