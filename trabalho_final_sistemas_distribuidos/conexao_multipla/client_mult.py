
import xmlrpc.client
import time
import socket

host_rpc = 'localhost'
port_rpc = 8080

host_socket = '127.0.0.1'
port_socket = 12345

def submit_order():
    # Conecta ao servidor XML-RPC
    with xmlrpc.client.ServerProxy(f"http://{host_rpc}:{port_rpc}/") as proxy:
        # Cria um socket TCP/IP
        ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Aguardando conexão com o servidor...')
        try:
            # Conecta o socket ao servidor socket
            ClientSocket.connect((host_socket, port_socket))
            Response = ClientSocket.recv(1024)
            print(Response.decode('utf-8'))  # Imprime a mensagem de boas-vindas recebida do servidor
            while True:
                department = input("Entre com o departamento (sanduiches, pratos_prontos, bebidas, sobremesas) ou 'sair' para parar: ").strip()
                if department.lower() == 'sair':
                    break
                menu = proxy.get_menu(department)
                if isinstance(menu, str):
                    print(menu)
                    continue
                print(f"Menu para o departamento de {department}:")
                for item, preparation_time in menu.items():
                    print(f"{item} (Tempo de preparo: {preparation_time} segundos)")
                order = input(f"Entre com o pedido para o departamento de {department} ou 'sair' para parar: ").strip()
                if order.lower() == 'sair':
                    break
                print(proxy.receive_order(order, department))
                while True:
                    status = proxy.get_order_status(order, department)
                    if status == "Seu pedido Pronto! Deseja algo a mais?":
                        print("Conferindo status do pedido...")
                        time.sleep(2)
                    else:
                        print(status)
                        break
        except socket.error as e:
            print(str(e))
        finally:
            # Fecha o socket após o uso
            ClientSocket.close()

if __name__ == "__main__":
    submit_order()
