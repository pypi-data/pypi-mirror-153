# Super Scraper
Scraping couldn't get much easier.  

**Super Scraper** is built with ease in mind - for those hard to scrape places. It drives with Selenium and parses with BeautifulSoup4. I've provided some convenience methods to make common actions even easier for you.

# Example

```
from superscraper import SuperScraper, By

scraper = SuperScraper(show_process=True)
scraper.search('https://www.google.com')
scraper.fill_in(By.NAME, 'q', 'hello world')
scraper.click(By.NAME, 'btnK')

search_results = scraper.driver.find_elements(By.CLASS_NAME, 'g')
for result in search_results:

    title = scraper.attempt(result.find_element, By.TAG_NAME, 'h3')
    if title:
        print(title.text)
        a = result.find_element(By.TAG_NAME, 'a')
        scraper.open_new_tab(By.LINK_TEXT, a.text)
        scraper.close_current_tab(switch_to_tab=-1)
```