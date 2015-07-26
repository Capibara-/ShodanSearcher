__author__ = 'Capibara'

import shodan
import sys
import requests
import argparse

SHODAN_API_KEY = ""

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('keywords', nargs='+', help='Search term.')
    parser.add_argument('--country', '-c', help='Country code.')
    parser.add_argument('--timeout', '-t', help='Timeout for GET requests in seconds.', type=int)
    parser.add_argument('--verbose', '-v', help='Verbose output.', action='store_true')
    args = parser.parse_args()


    keywords = ' '.join(args.keywords)
    search_term = "%s country:%s" % (keywords, args.country) if args.country else keywords
    timeout = args.timeout if args.timeout else 5
    api = shodan.Shodan(SHODAN_API_KEY)

    try:
        results = api.search(search_term)
    except shodan.APIError, e:
        print "[+] Error while querying Shodan: %s." % e

    print "[+] Got %s results from Shodan search, sending GET requests." % results['total']

    live_results = map(lambda x: (x['ip_str'], get_status_code(x['ip_str'],
                                                               timeout=args.timeout,
                                                               verbose=args.verbose)), results['matches'])

    print "\n[+] Matching IP addresses that return HTTP 200:"
    print "\n".join([x for (x, y) in filter(lambda (x, y): y == 200, live_results)])

    print "\n[+] Matching IP addresses that return HTTP 401:"
    print "\n".join([x for (x, y) in filter(lambda (x, y): y == 401, live_results)])


def get_status_code(host, path="/", timeout=5, verbose=False):
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
