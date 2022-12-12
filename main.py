import requests
import hashlib
import sys

def send_api(hash_str):
    url = 'https://api.pwnedpasswords.com/range/' + hash_str
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'During handling the above exception occured: {response.status_code}')
    return response

def get_num_leaks(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for hash, num in hashes:
        if hash == hash_to_check:
            return num
    return 0


def hash_password(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first, last = sha1_password[:5], sha1_password[5:]
    response = send_api(first)
    return get_num_leaks(response, last)


def main(passwords):
    for password in passwords:
        count = hash_password(password)
        if count:
            print(f'{password} was found {count} times. You should probably change the password!')
        else:
            print(f'{password} was NOT found. You can use it safely.')
    return 'Finished!'




if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))