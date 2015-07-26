__author__ = 'Capibara'

import shodan
import sys
import requests

SHODAN_API_KEY = "Jvt0B5uZIDPJ5pbCqMo12CqD7pdnMSEd"

def main(argv):
    if len(argv) != 2 and len(argv) != 3:
        print "Usage: %s <search term> [country]." % argv[0]
        return
    search_term = argv[1] if len(argv) == 2 else "%s country:%s" % (argv[1], argv[2])
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
