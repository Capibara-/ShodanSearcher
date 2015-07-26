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
    args = parser.parse_args()


    keywords = ' '.join(args.keywords)
    search_term = "%s country:%s" % (keywords, args.country) if args.country else keywords
    print search_term
    return
    api = shodan.Shodan(SHODAN_API_KEY)

    try:
        results = api.search(search_term)
    except shodan.APIError, e:
        print "Error while querying Shodan: %s." % e

    print "Matching IP addresses that return HTTP 200:"
    for result in results['matches']:
        if get_status_code(result['ip_str']) == 200:
            print result['ip_str']


def get_status_code(host, path="/"):
    try:
        r = requests.get("http://%s%s" % (host.encode('ascii', 'ignore'), path.encode('ascii', 'ignore')))
        return r.status_code
    except requests.ConnectionError:
        return None

if __name__ == '__main__':
    main(sys.argv)
