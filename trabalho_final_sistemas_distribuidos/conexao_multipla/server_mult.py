
import xmlrpc.server
import time
import threading
import socket

# Definição de constantes para a configuração do servidor
HOST_RPC = 'localhost'
PORT_RPC = 8080
HOST_SOCKET = '127.0.0.1'
PORT_SOCKET = 12345

# Menu do restaurante
menu = {
    'sanduiches': {'presunto': 5, 'queijo': 3, 'vegetariano': 7},
    'pratos_prontos': {'macarrao': 10, 'frango': 7, 'salada': 5},
    'bebidas': {'cafe': 2, 'suco': 2, 'agua': 1},
    'sobremesas': {'bolo': 7, 'salada_de_frutas': 5, 'sorvete': 3}
}

# Status dos pedidos
order_status = {}

def setup_server():
    # Configuração do servidor XML-RPC
    server = xmlrpc.server.SimpleXMLRPCServer((HOST_RPC, PORT_RPC))
    server.register_multicall_functions()
    server.register_function(receive_order, "receive_order")
    server.register_function(get_menu, "get_menu")
    server.register_function(get_order_status, "get_order_status")
    print(f"Listening on XMLRPC port {PORT_RPC}...")
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # Configuração do servidor socket
    SocketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        SocketServer.bind((HOST_SOCKET, PORT_SOCKET))
    except socket.error as e:
        print(str(e))
    print(f"Servidor está na escuta na porta {PORT_SOCKET}...")
    SocketServer.listen()
    accept_connection(SocketServer)

def accept_connection(SocketServer):
    while True:
        client, address = SocketServer.accept()
        print(f"Conexão estabelecida com {address}.")
        threading.Thread(target=client_handler, args=(client,)).start()

def client_handler(client):
    client.send(str.encode('Bem-vindo ao servidor! Digite BYE para sair.'))
    try:
        while True:
            data = client.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f'Dados recebidos: {message}')
            if message == 'BYE':
                break
            reply = f'Server: {message}'
            client.sendall(reply.encode('utf-8'))
    finally:
        client.close()

def get_menu(department):
    return menu.get(department, "Departamento não encontrado.")

def receive_order(order, department):
    if order in menu.get(department, {}):
        threading.Thread(target=prepare_food, args=(order, department)).start()
        return f"Pedido de {order} recebido em {department}. Está sendo preparado."
    else:
        return "Pedido indisponível."

def get_order_status(order, department):
    return order_status.get((order, department), "Seu pedido Pronto! Deseja algo a mais?")

def prepare_food(order, department):
    time.sleep(menu[department][order])
    order_status[(order, department)] = f"O pedido {order} está pronto."

if __name__ == "__main__":
    setup_server()
