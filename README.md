# netlas-email-search

Search emails with Netlas.io in the following sources:
- Whois data
- SSL certificates
- Sites contact data
- Web pages content

## Installation

1. _pip3 install -r requirements.txt_

2. Copy API key from your [Profile page](https://app.netlas.io/profile/)

3. Just run the script!

## Usage

Search by a specific email address:

	./netlas-email-search.py EMAIL

Search by a email domain (wildcard):

	./netlas-email-search.py protonmail.com

## Example

```
# ./netlas-email-search.py root@localhost
Whois search did't return results
SSL search can return 49710 results
Downloading 20 results...
Downloaded first 20 results only. You can get all the results manually with a query <certificate.subject.email_address:root@localhost>
Contacts search can return 6 results
Downloading 6 results...
Webpage search can return 288451 results
Downloading 20 results...
Downloaded first 20 results only. You can get all the results manually with a query <http.body:root@localhost>

Downloaded data was saved to following files:
	SSL_root@localhost_results.json
	Contacts_root@localhost_results.json
	Webpage_root@localhost_results.json
```

## TODO

- [ ] Data downloading from Netlas
