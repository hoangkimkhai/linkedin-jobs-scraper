from Browser import Browser
from Website import Website


def main():
    web_site = Website("Linkedin", 'https://linkedin.com',
                       'https://www.linkedin.com/jobs/search/?geoId=102890719&keywords=',
                       'https://www.linkedin.com/uas/login')
    browser = Browser(web_site)
    browser.log_in('your_linked_in_user_name', 'your_linked_in_password')
    topics = ['java', 'python']
    browser.generate_search_url(topics)
    browser.get_jobs_details(browser.search_urls[0])


if __name__ == "__main__":
    main()