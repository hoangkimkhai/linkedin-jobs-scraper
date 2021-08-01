import  time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
from bs4 import BeautifulSoup
from Job import Job


class Browser:
    def __init__(self, website):
        self.browser = webdriver.Chrome('D:\chromedriver\chromedriver.exe')  # Path to chrome driver
        self.search_urls = []
        self.website = website

    def log_in(self, username, password):
        print(self.website.login_url)
        self.browser.get(self.website.login_url)
        elementId = self.browser.find_element_by_id('username')
        elementId.send_keys(username)
        elementId = self.browser.find_element_by_id('password')
        elementId.send_keys(password)
        elementId.submit()

    def generate_search_url(self, topics):
        for topic in topics:
            prefix_search_url = self.website.search_url
            search_url = prefix_search_url + topic + "&location={}".format('Netherlands')
            if search_url not in self.search_urls:
                self.search_urls.append(search_url)

    def make_page_complete(self, jobs_search_url):
        actions = ActionChains(self.browser)
        self.browser.get(jobs_search_url)
        time.sleep(1)
        current_in_view = 4
        base_css_selector = 'div.jobs-search-two-pane__job-card-container--viewport-tracking-'
        css_selector = base_css_selector + str(current_in_view)
        try:
            element = self.browser.find_element_by_css_selector(css_selector)
            self.browser.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(0.5)
        except:
            print("Cant find the element, something is wrong with the site")
        while (current_in_view < 20):
            current_in_view += 3
            css_selector = base_css_selector + str(current_in_view)
            try:
                element = self.browser.find_element_by_css_selector(css_selector)
                self.browser.execute_script("arguments[0].scrollIntoView();", element)
                time.sleep(0.5)
            except:
                print("Cant find the element, something is wrong with the site")
                continue
        element = self.browser.find_element_by_css_selector('section.jobs-search-two-pane__pagination')
        actions.move_to_element(element)
        actions.perform()

    def get_jobs_details(self, jobs_search_url):
        self.make_page_complete(jobs_search_url)
        src = self.browser.page_source
        soup = BeautifulSoup(src, 'html.parser')
        links = soup.select("a.job-card-container__link ")
        count_link = 0
        visited = []
        company_patterns = '/company/*'
        regex = re.compile(company_patterns)
        for li in links:
            url = li.attrs['href']
            if not regex.match(url) and url not in visited:
                count_link += 1
                visited.append(url)
                abs_link = "https://www.linkedin.com/" + url
                self.browser.get(abs_link)
                src = self.browser.page_source
                bs = BeautifulSoup(src, 'html.parser')
                try:
                    info = bs.find('div', {'class': 'mt2'})
                    title = bs.find('h1').get_text().strip()
                    rr = bs.find('div', {'class': 'mt2'})
                    company = rr.find('a').get_text().strip()
                    location = rr.find('span', {'class': 'jobs-unified-top-card__bullet'}).get_text().strip()
                    posted_date = rr.find('span', {'class': 'jobs-unified-top-card__posted-date'}).get_text().strip()
                except:
                    continue
                num_apps = 0
                job = Job(title, company, location, posted_date, num_apps)
                print("Job {}".format(count_link), end=': ')
                job.myprint()
                time.sleep(2)