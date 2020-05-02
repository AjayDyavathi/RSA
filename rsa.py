import random
import sys


def xgcd(a, b):
    '''return (g, x, y) such that a*x + b*y = g = gcd(a, b)'''
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = xgcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    '''return x such that (x * a) % b == 1'''
    g, x, y = xgcd(a, m)
    if g != 1:
        raise Exception("Modular inverse doesn't exist: gcd(a, b) != 1")
    else:
        return x % m


def isprime(num):
    '''Check if num is prime'''
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for each_num in range(3, num, 2):
        if num % each_num == 0:
            return False
    return True


def generate_keypair(p, q):
    '''generate public and private key pair'''
    if not (isprime(p) and isprime(q)):
        raise ValueError('p and q should be primes')
    if p == q:
        raise ValueError('p and q cannot be equal')

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    while xgcd(e, phi)[0] != 1:
        e = random.randrange(1, phi)

    d = modinv(e, phi)
    return (e, n), (d, n)


def encrypt(public_key, message):
    '''Encrypt message with public key'''
    key, n = public_key
    cipher = [pow(ord(char), key, n) for char in message]
    return cipher


def decrypt(private_key, cipher):
    '''Decryot message with private key'''
    key, n = private_key
    message = ''.join([chr(pow(char, key, n)) for char in cipher])
    return message


if __name__ == '__main__':
    flag = True
    if len(sys.argv[:]) > 1:
        if sys.argv[1] == 'check_primes':
            flag = False
            print('q for quit')
            inp = input()
            while inp != 'q':
                print(isprime(int(inp)))
                inp = input()

    mode = input('RSA Algorithm: Encryption(enc) or Decryption(dec): ').lower()
    if not mode in ['enc', 'dec']:
        print('Invalid choice!')
        sys.exit()

    if mode == 'enc':
        p = int(input('Enter a prime number (greater than 7): '))
        q = int(input('Enter another prime number (greater than 7): '))
        if flag:
            print('You can try checking primes by running "$ python3 rsa.py check_primes"')
        print('Generating RSA keys...')
        try:
            public_key, private_key = generate_keypair(p, q)
        except ValueError as e:
            print(e)
            sys.exit()
        print(f'Public key: {public_key}, Private key: {private_key}')
        message = input('Enter the text to encrypt: ')
        cipher = encrypt(public_key, message)
        print(cipher)

    if mode == 'dec':
        # private_key should be entered as a tuple
        private_key = eval(input('Enter the private key pair as tuple: '))
        # cipher should be entered as a list of cipher numbers
        cipher = eval(input('Enter the cipher list: '))
        message = decrypt(private_key, cipher)
        print(message)
