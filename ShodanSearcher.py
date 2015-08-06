__author__ = 'Capibara'


 #  ____    __                  __                   ____                                  __
 # /\  _`\ /\ \                /\ \                 /\  _`\                               /\ \
 # \ \,\L\_\ \ \___     ___    \_\ \     __      ___\ \,\L\_\     __     __     _ __   ___\ \ \___      __   _ __
 #  \/_\__ \\ \  _ `\  / __`\  /'_` \  /'__`\  /' _ `\/_\__ \   /'__`\ /'__`\  /\`'__\/'___\ \  _ `\  /'__`\/\`'__\
 #    /\ \L\ \ \ \ \ \/\ \L\ \/\ \L\ \/\ \L\.\_/\ \/\ \/\ \L\ \/\  __//\ \L\.\_\ \ \//\ \__/\ \ \ \ \/\  __/\ \ \/
 #    \ `\____\ \_\ \_\ \____/\ \___,_\ \__/.\_\ \_\ \_\ `\____\ \____\ \__/.\_\\ \_\\ \____\\ \_\ \_\ \____\\ \_\
 #     \/_____/\/_/\/_/\/___/  \/__,_ /\/__/\/_/\/_/\/_/\/_____/\/____/\/__/\/_/ \/_/ \/____/ \/_/\/_/\/____/ \/_/


import shodan
import sys
import requests
import argparse
from collections import defaultdict

SHODAN_API_KEY = ""

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('keywords', nargs='+', help='Search term.')
    parser.add_argument('--country', '-c', help='Country code.')
    parser.add_argument('--timeout', '-t', help='Timeout for GET requests in seconds.', type=int)
    parser.add_argument('--verbose', '-v', help='Verbose output.', action='store_true')
    args = parser.parse_args()


    keywords = ' '.join(args.keywords)
    searcher = ShodanSearcher(keywords, country_code=args.country) if args.country else ShodanSearcher(keywords)
    results = searcher.search()
    for http_code in results:
        print "\n[+] Matching IP addresses that return HTTP %d:" % http_code
        print "\n".join(results[http_code])



class ShodanSearcher:
    """A class to automate Shodan searches and filter results.
        keywords        Self explanatory.
        country_code    Optional.
        timeout         Timeout for HTTP GET requests.
        verbose         Verbose output.
        http_codes      Optional, defaults to 200 and 401.
    """
    keywords = ""
    country_code = None
    timeout = 5
    verbose = False
    http_codes = None

    def __init__(self, keywords, country_code=None, timeout=5, verbose=False, http_codes=[200, 401]):
        self.keywords = keywords
        self.country_code =  country_code
        self.timeout = timeout
        self.verbose = verbose
        self.http_codes = http_codes

    def search(self):
        """Searches ShodanHQ.io for the given keywords then filters out results that do not respond with the specified HTTP code.
        Returns a dictionary mapping the HTTP code to a list of IPs that returned that code.
        """
        search_term = "%s country:%s" % (self.keywords, self.country_code) if self.country_code else self.keywords
        api = shodan.Shodan(SHODAN_API_KEY)

        try:
            results = api.search(search_term)
        except shodan.APIError, e:
            print "[+] Error while querying Shodan: %s." % e

        print "[+] Got %s results from Shodan search, sending GET requests." % results['total']
        live_results = map(lambda x : (x['ip_str'], self._get_status_code(x['ip_str'],
                                                               timeout=self.timeout,
                                                               verbose=self.verbose)), results['matches'])
        output = defaultdict(list)

        for (ip, http_code) in live_results:
            if http_code in self.http_codes:
                output[http_code].append(ip)
        return output


    def _get_status_code(self, host, path="/", timeout=5, verbose=False):
        try:
            if verbose:
                print "[+] Sending GET request to %s." % host
            r = requests.get("http://%s%s" % (host.encode('ascii', 'ignore'), path.encode('ascii', 'ignore')),
                             timeout=timeout)
            return r.status_code
        except (requests.ConnectionError, requests.exceptions.ConnectTimeout) as e:
            if verbose:
                print "[+] Bad reply from %s: %s." % (host, str(e))
            return None

if __name__ == '__main__':
    main(sys.argv)
