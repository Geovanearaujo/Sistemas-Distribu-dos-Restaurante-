
import xmlrpc.server
import time
import threading
import socket

# Definição de constantes para a configuração do servidor
HOST = 'localhost'
PORT_XMLRPC = 8080
PORT_SOCKET = 8082
DATA_PAYLOAD = 2048  # Quantidade máxima de dados recebidos por vez

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
    # Configuração do servidor XMLRPC
    server = xmlrpc.server.SimpleXMLRPCServer((HOST, PORT_XMLRPC))
    server.register_multicall_functions()
    server.register_function(receive_order, "receive_order")
    server.register_function(get_menu, "get_menu")
    server.register_function(get_order_status, "get_order_status")
    print(f"Listening on XMLRPC port {PORT_XMLRPC}...")
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # Configuração do servidor socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = (HOST, PORT_SOCKET)
    print(f"Inicializando servidor socket em {server_address}")
    sock.bind(server_address)
    sock.listen(5)

    while True:
        print("Esperando por uma conexão...")
        client, _ = sock.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(client,))
        client_thread.start()

def handle_client_connection(client_socket):
    try:
        while True:
            data = client_socket.recv(DATA_PAYLOAD)
            if not data:
                break
            response = b"Received: " + data
            client_socket.send(response)
    finally:
        client_socket.close()

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
