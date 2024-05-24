import threading
import socket

clients = []
usernames = {}

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 7777))
        server.listen()
        print("Servidor iniciado e escutando na porta 7777")
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = server.accept()
        print(f"Conectado a {addr}")
        client.send("NOME".encode("utf-8"))
        username = client.recv(2048).decode("utf-8")
        print(f"Usuário {username} conectou-se.")
        usernames[client] = username
        clients.append(client)

        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()

def messagesTreatment(client):
    while True:
        try:
            msg = client.recv(2048)
            broadcast(msg, client)
        except:
            deleteClient(client)
            break


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)


def deleteClient(client):
    print(f"Usuário {usernames[client]} desconectou-se.")
    clients.remove(client)
    del usernames[client]

main()
