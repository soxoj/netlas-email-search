#!/usr/bin/env python3
import os
import sys

import netlas


KEYFILE = '.key'


def email_query(conn, descr, query, email):
    query_res = conn.query(query=query.format(email=email))
    results_count = len(query_res['items'])
    print(f'{descr} search returned {results_count} results')
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
        'Whois': f'whois.val.raw:{email}',
        'SSL': f'certificate.subject.email_address:{email}',
        'Contacts': f'contacts.email:{email}',
        'Webpage': f'http.body:{email}',
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

    filenames = filter(lambda x: x, search(key, email))

    if filenames:
        print('\nFound data saved to following files:')
        for f in filenames:
            print(f'\t{f}')
