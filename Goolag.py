#! /usr/bin/env/ python3

#################################################
# Goolag is a utility that launches a selenium
# web driver with the AdNauseum addon enabled and
# uses a simple implementation of Markov chains
# to randomize webdriver behavior. The end result
# is a process which can be run in the background
# that generates high volumes of fake clicks for
# online ads (undermining online advertising integrity).
#
# You might ask "what's the next step in your master plan?"
#
# Crashing this profit model . . . WITH NO SHAREHOLDERS
##################################################

# HTML parsing tools and selenium will be required
import requests
import bs4
from selenium import webdriver
import random
from time import sleep
import re
import argparse

class Setup:
    '''
    Class container for setting driver profile preferences,
    fetching proxy lists and methods necessary to use the
    proxy functinality of the script
    '''
    
    def __init__(self, **kwargs):
        self.proxy_list_url = 'http://us-proxy.org'
        self.proxies = []
        self.tor_ip = '127.0.0.1'
        self.tor_port = 9050
        with open('User Agents') as infile:
            self.agents = infile.read().split('\n')
        # TODO: Gracefully remove these since the argparser already does this
        self.flags = {
            'proxy':False,
            'tor':False}
        self.flags.update(kwargs)
        self.profile = webdriver.FirefoxProfile('n89ei0po.AdNauseum')

    def fetch_proxies(self):
        # request us-proxy web page and return a list of
        # IP and port numbers [(IP,port),]
        proxies = []
        r = requests.get(self.proxy_list_url)
        # Exit on failure if we can't get a list
        if r.status_code != 200:
            print('[!] PROXY REQUEST FAILED!')
            print('[!] EXITING!')
            quit()
        soup = bs4.BeautifulSoup(r.text,'lxml')
        table = soup.find('table',attrs={'id':'proxylisttable'})
        rows = table.find_all('tr')
        for row in rows[1:-2]: #only view rows with proxy data
            data = row.find_all('td')
            ip = data[0].text
            port = int(data[1].text)
            proxies.append((ip,port))
            self.proxies = proxies
        return None

    def set_user_agent(self):
        agent = random.choice(self.agents)
        self.profile.set_preference('general.useragent.override',agent)
        return None
                                                
    def set_http_proxy(self):
        # take a webdriver profile (Firefox) and a tuple (IP:PORT)
        # as arguments and update the profile
        proxy = self.validate_proxy()
        self.profile.set_preference('network.proxy.type',1)
        self.profile.set_preference('network.proxy.http',proxy[0])
        self.profile.set_preference('network.proxy.http_port',proxy[1])
        self.profile.update_preferences()
        return None

    def validate_proxy(self):
        # Verify that a given proxy can connect to Google and return 200
        print('Testing proxies')
        validated = False
        count = 0
        while not validated:
            count += 1
            proxy = random.choice(self.proxies)
            p = {'http':proxy[0]+':'+str(proxy[1])} # Consider HTTPS support later
            print('\rConnection attempts: [{0}]'.format(count),end='',flush=True)
            testpage = requests.get('http://www.google.com',proxies=p)
            if testpage.status_code == 200:
                print('\nSuccess!')
                validated = True
        return proxy            
                                                
    def set_tor_proxy(self):
        # Set preferences to connect through TOR
        self.profile.set_preference('network.proxy.type',1)
        self.profile.set_preference('network.proxy.socks',self.tor_ip)
        self.profile.set_preference('network.proxy.socks_port',self.tor_port)
        self.profile.update_preferences()
        return None

    def start(self):
        # Launch a webdriver with our preferences set.
        self.set_user_agent()
        if self.flags['proxy']:
            self.fetch_proxies()
            self.set_http_proxy()
        if self.flags['tor']:
            self.set_tor_proxy()
        driver = webdriver.Firefox(self.profile)
        return driver
            
    def refresh(self,driver):
        driver.close()
        self.set_user_agent()
        if self.flags['proxy']:
            self.set_http_proxy()
        if self.flags['tor']:
            self.set_tor_proxy()
        driver = webdriver.Firefox(self.profile)
        return driver

class Crawler:
    '''
    The crawler class provides the bulk of the logic for the
    webdriver. This includes connecting to domains, crawling pages
    within the domain and handling wait times and random number
    generation to determine the webdriver's behavior.
    '''
    def __init__(self, webdriver, **kwargs):
        self.webdriver = webdriver
        with open('Domains') as infile:
            self.domains = infile.read().split()
        # default max values for options to be overwritten by keyword args
        # TODO: Gracefully remove these since the argparser already does this
        self.options = {
            'min_wait':2.0,
            'interval':1.0,
            'reset':0.25,
            'domain':0.50,
            'crawl':0.75,}
        self.options.update(kwargs)
        # Randomize variables to evade traffic pattern recognition
        self.reset = random.random() % self.options['reset']
        self.domain = random.random() % self.options['domain']
        self.crawl = random.random() % self.options['crawl']

    def new_domain(self):
        random_domain = random.choice(self.domains)
        self.webdriver.get(random_domain)
        # Get all links within the domain. These could be relative
        # paths, absolute paths or both.
        source = self.webdriver.page_source
        soup = bs4.BeautifulSoup(source,'lxml')
        links = soup.find_all('a')
        # Strip everyting but href
        hrefs = [x['href'] for x in links if 'href' in x.attrs]
        top = ('.').join(random_domain.split('.')[1:3]) # returns 'something.com'
        # Get relative URLs
        relative = [x for x in hrefs if re.match('/',x)]
        # Convert to absolute paths
        local_links = ['http://www.'+top+x for x in relative]
        # Get absolute URLs within the domain
        abs_urls = [x for x in hrefs if re.search(top,x)]
        local_links += abs_urls
        return local_links

    def new_page(self,local_links):
        # Get a random page to follow. If there are none, get a random domain
        if local_links:
            random_page = random.choice(local_links)
        else:
            random_page = random.choice(self.domains)
        self.webdriver.get(random_page)
        sleep(self.options['min_wait'])
        return None

class BanePost:
    '''
    This is a big class
    '''
    def __init__(self):
        self.files = ['Bane/CIA.txt','Bane/big_guy.txt','Bane/crash.txt']

    def post_rare_bane(self):
        filename = random.choice(self.files)
        with open(filename) as maymay:
            print(maymay.read())

# Main loop
if __name__ == "__main__":
    #Handle User supplied arguments and provide help information
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--proxy',help="Connect through random proxy", action="store_true")
    parser.add_argument('-t','--tor',help="Connect through tor (localhost:9050)",action="store_true")
    parser.add_argument('-i','--interval',help='Time in seconds to wait before the webdriver will \
                        choose its next action',default=1.0)
    parser.add_argument('-c','--crawl',help='Maximum probability (0.0-1.0) the webdriver will choose \
to follow a link within a website. Site.com -> Site.com/blog',default=0.75)
    parser.add_argument('-d','--domain',help='Maximum probability (0.0-1.0) the webdriver will choose \
to go to a new domain. Site.com -> Othersite.com',default=0.50)
    parser.add_argument('-r','--reset',help='Maximum probability (0.0-1.0) the program will close the \
                        current webdriver and start a new driver with new settings, including user \
                        agent and proxy, if selected',default=0.25)
    parser.add_argument('-b','--bane',help="Dr. Pavel, I'm CIA",action="store_true")
    args = parser.parse_args()
    driver_options = {
                    'proxy':args.proxy,
                    'tor':args.tor}
    crawler_options = {
                    'interval':float(args.interval),
                    'reset':float(args.reset),
                    'domain':float(args.domain),
                    'crawl':float(args.crawl)}
    if args.bane:
        bp = BanePost()
        bp.post_rare_bane()
        quit()

    print('Press ctl+c to end program') # TODO Write in a graceful exit.
    print('Initializing webdriver . . .')
    s = Setup() # Set UA and proxies, if applicable
    s.set_user_agent()
    if s.flags['proxy']:
        s.fetch_proxies()
        s.set_http_proxy()
    if s.flags['tor']:
        s.set_tor_proxy()
    print('Launching webdriver')
    driver = s.start()
    c = Crawler(driver)
    links = c.new_domain()
    while True: # TODO tie this condition to an exit other than keyboard interrupt
        try:
            if random.random() < c.crawl:
                c.new_page(links)
            elif random.random() < c.domain:
                links = c.new_domain()
            elif random.random() < c.reset:
                driver = s.refresh(driver)
                c = Crawler(driver)
                links = c.new_domain()
            else:
                sleep(c.options['interval'])
        except Exception as e:
            print('Exception caught:')
            print(e)
            driver = s.refresh(driver)
            c = Crawler(driver)
            links = c.new_domain()

