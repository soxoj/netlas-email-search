#!/usr/bin/env python3
import os
import sys

import netlas


KEYFILE = '.key'
MAX_RESULTS = 20


def email_query(conn, descr, query, email):
    if '@' in email:
        email_str = email
    else:
        email_str = f'"*@{email}"'

    query_str = query.format(email=email_str)
    count_res = conn.count(query=query_str).get("count", 0)

    if not count_res:
        print(f'{descr} search did\'t return results')
        return None

    print(f'{descr} search can return {count_res} results')

    query_res = conn.query(query=query_str)
    results_count = len(query_res['items'])
    print(f'Downloading {results_count} results...')

    if results_count == MAX_RESULTS:
        print(f'Downloaded first {MAX_RESULTS} results only. '
              f'You can get all the results manually with a query <{query_str}>')

    if results_count:
        filename = f'{descr}_{email}_results.json'
        with open(filename, 'w') as f:
            f.write(netlas.helpers.dump_object(data=query_res))
        return filename

    return None


def search(key, email):
    result_files = []
    conn = netlas.Netlas(api_key=key)
    search_methods = {
        'Whois': 'whois.val.raw:{email}',
        'SSL': 'certificate.subject.email_address:{email}',
        'Contacts': 'contacts.email:{email}',
        'Webpage': 'http.body:{email}',
    }
    for descr, query in search_methods.items():
        result_files.append(email_query(conn, descr, query, email))

    return result_files


if __name__ == '__main__':
    key = ''
    if not os.path.exists(KEYFILE):
        key = input('Enter Netlas.io API key, it will be saved to .key file')
        if not key:
            print('No key was provided, exiting')
            sys.exit(1)
        with open(KEYFILE, 'w') as f:
            f.write(key)
    else:
        with open(KEYFILE) as f:
            key = f.read().strip()

    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = input('Enter target email: ')

    filenames = list(filter(lambda x: x, search(key, email)))

    if len(filenames):
        print('\nDownloaded data was saved to following files:')
        for f in filenames:
            print(f'\t{f}')
