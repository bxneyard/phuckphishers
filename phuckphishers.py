#!/usr/bin/env python3
# usage: phuckphishers.py [-h] -u <url> -w <path> [-T <threads>]

import argparse, random, requests, secrets, string, sys, threading

def first(file):
    choice = bool(random.getrandbits(1))
    if choice:
        return chr(random.randint(97,122))
    else:
        with open(file) as f:
            first = random.choice(list(f)).strip().lower()
        return first

def last(file):
    with open(file) as f:
        last = random.choice(list(f)).strip().lower()
    return last         

def cat(first, last):
    choice = bool(random.getrandbits(1))
    if choice:
        return f'{first}{last}'
    else:    
        return f'{first}.{last}'

def nums(fullname):
    choice = bool(random.getrandbits(1))
    if choice:
        num = random.randint(0,9999)
        return f'{fullname}{num}'
    else:
        return fullname

def domain(handle):
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'verizon.net', 'att.net', 'earthlink.net', 'aol.com']
    domain = random.choice(domains)
    return f'{handle}@{domain}'

def create_email(names):
    return domain(nums(cat(first(names),last(names))))

def create_pass():
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    alphabet = letters + digits + special_chars
    password_length = random.randint(8,20)
    while True:
        password = ''
        for i in range(password_length):
            password += ''.join(secrets.choice(alphabet))
        if (any(char in special_chars for char in password) and 
            sum(char in digits for char in password)>=2):
                return password

def get_phucked(site, names):
    while True:
            username = create_email(names)
            password = create_pass()
            payload = {'username': username, 'password': password}
            response = requests.post(site, data=payload)
            print(f'{username} {password}\n{response}')

def main():
    print(f'''
▀██▀▀█▄  ▀██                       ▀██         ▀██▀▀█▄  ▀██       ██         ▀██                             
 ██   ██  ██ ▄▄   ▄▄▄ ▄▄▄    ▄▄▄▄   ██  ▄▄      ██   ██  ██ ▄▄   ▄▄▄   ▄▄▄▄   ██ ▄▄     ▄▄▄▄  ▄▄▄ ▄▄   ▄▄▄▄  
 ██▄▄▄█▀  ██▀ ██   ██  ██  ▄█   ▀▀  ██ ▄▀       ██▄▄▄█▀  ██▀ ██   ██  ██▄ ▀   ██▀ ██  ▄█▄▄▄██  ██▀ ▀▀ ██▄ ▀  
 ██       ██  ██   ██  ██  ██       ██▀█▄       ██       ██  ██   ██  ▄ ▀█▄▄  ██  ██  ██       ██     ▄ ▀█▄▄ 
▄██▄     ▄██▄ ██▄  ▀█▄▄▀█▄  ▀█▄▄▄▀ ▄██▄ ██▄    ▄██▄     ▄██▄ ██▄ ▄██▄ █▀▄▄█▀ ▄██▄ ██▄  ▀█▄▄▄▀ ▄██▄    █▀▄▄█▀                                                                                                                  
⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⡴⠚⠉⠉⠀⠀⠀⠉⠙⠓⢦⡀⠀⠀⠀⠀⠀⠀
⠀⣰⠋⠀⣀⣠⣤⣤⣤⡄⠀⣤⠤⠤⢿⣦⠀⠀⠀⠀⠀
⢰⠇⠀⠰⡅⠀⠰⢆⡼⠀⠀⠳⢤⡼⠟⠈⣧⠀⠀⠀⠀
⣼⠀⠀⠀⢉⣉⣉⣩⣤⠤⠤⠤⠶⢶⠒⠀⢸⡄⠀⠀⠀
⣿⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⢀⠀⣸⠀⢀⡼⠀⠀⢰⠀
⠘⢷⣀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡴⢃⡴⠋⠀⠀⣰⢉⠇
⠀⠀⠉⣳⠦⢤⣤⣤⣤⠤⣮⠶⢻⡏⡀⢤⣲⠝⠚⠁⠀
⠀⠀⣰⠃⢠⠴⣚⡭⠖⠉⠀⠀⢸⡧⠚⠉⠀⠀⠀⠀⠀
⠀⢠⡏⠀⠐⠋⠁⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀
⠰⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠃
''')
    
    parser = argparse.ArgumentParser(description='This program generates credentials and automates site login for the intent of disrupting scammers operating phishing websites; it will continue to run until terminated with ctrl + c. A names wordlist is required in order to generate usernames. Please report scam sites to https://safebrowsing.google.com/safebrowsing/report_phish/')
    parser.add_argument('-u', type=str, metavar='<url>', required=True, help='Scam site url ')
    parser.add_argument('-w', type=str, metavar='<path>', required=True, help='File path of names wordlist')
    parser.add_argument('-T', type=int, metavar='<threads>', default=1, help='Number of threads to run')
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    threads = []
    for _ in range(args.T):
            t = threading.Thread(target=get_phucked, args=(args.u, args.w))
            t.daemon = True
            t.start()
            threads.append(t)
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('>> Keyboard Interrupt')
        sys.exit(130)
