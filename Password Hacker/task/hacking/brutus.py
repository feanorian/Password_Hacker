import itertools
import string
import socket
import sys

letters = list(string.ascii_lowercase)
numbers_int = list(range(10))
numbers = [str(num) for num in numbers_int]
characters = list(itertools.chain(letters, numbers))

#This function yields passwords made up of lowercase + digits of lenght count
def pass_generator():

    count = 1
    while count <= len(characters):
        yield from itertools.product(characters, repeat=count)

        count += 1

#takes in output of pass_generator and stops when the correct password is guessed 
with socket.socket() as client_socket:
    args = sys.argv
    hostname = args[1]
    port = int(args[2])
    address = (hostname, port)
    client_socket.connect(address)
    pass_guess = pass_mixer()
    for _ in range(100_000):
        pword = ''.join(next(pass_guess))
        client_socket.send(pword.encode())
        response = client_socket.recv(1024).decode()
        if response == 'Connection success!':
            print(pword)
            break