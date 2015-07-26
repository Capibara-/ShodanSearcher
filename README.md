<h1>==ShodanSearcher==</h1>

Searches shodanhq.io by keyword and country and only returns the IPs that respons HTTP 200 to GET requests.

Usage: ShodanSearcher.py [-h] [--country COUNTRY] [--timeout TIMEOUT]
                         [--verbose]
                         keywords [keywords ...]

positional arguments:
  keywords              Search term.

optional arguments:
  -h, --help            show this help message and exit
  --country COUNTRY, -c COUNTRY
                        Country code.
  --timeout TIMEOUT, -t TIMEOUT
                        Timeout for GET requests in seconds.
  --verbose, -v         Verbose output.