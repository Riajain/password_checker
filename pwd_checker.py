import requests
import hashlib
import sys

def req_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code} : check again')
    return res

def get_pwd_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

#res.text = number of possible with first 5 chars of our sha1 pwd
def pwnedpassword(password):
    sha1pwd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1pwd[:5], sha1pwd[5:]
    res = req_api_data(first5_char)
    return get_pwd_leaks_count(res, tail)


def main(args):
    for pwd in args:
        count = pwnedpassword((pwd))
        if count:
            print(f'{pwd} was found {count} times. Please try another password')
        else:
            print(f'{pwd} was never used before. Go ahead!')

if __name__ == '__main__':
    main(sys.argv[1:])