import xmlrpc.client
import time
import socket

def submit_order():
    host_rpc = "localhost"  # Endereço IP do servidor XML-RPC
    port_rpc = 8080         # Porta do servidor XML-RPC

    host_socket = "localhost"  # Endereço IP do servidor socket
    port_socket = 8082         # Porta do servidor socket

    # Conecta ao servidor XML-RPC
    with xmlrpc.client.ServerProxy(f"http://{host_rpc}:{port_rpc}/") as proxy:
        # Cria um socket TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Conecta ao servidor socket
            server_address = (host_socket, port_socket)
            print(f"Conectando ao servidor socket {server_address[0]} na porta {server_address[1]}")
            sock.connect(server_address)
            
            # Lista para armazenar pedidos
            order_list = []
            
            while True:
                department = input("Entre com o departamento (sanduiches, pratos_prontos, bebidas, sobremesas) ou 'sair' para parar: ").strip()
                if department.lower() == 'sair':
                    break
                menu = proxy.get_menu(department)
                if isinstance(menu, str):
                    print(menu)
                    continue
                print(f"Menu para o departamento de {department}:")
                for item, prep_time in menu.items():
                    print(f"{item} (Tempo de preparo: {prep_time} segundos)")
                
                order = input(f"Entre com o pedido para o departamento de {department} ou 'sair' para parar: ").strip()
                if order.lower() == 'sair':
                    break
                
                # Adiciona o pedido à lista
                order_list.append((department, order))
                
                print(proxy.receive_order(order, department))
                while True:
                    status = proxy.get_order_status(order, department)
                    if status == "Seu pedido está pronto! Deseja algo a mais?":
                        print("Conferindo status do pedido...")
                        time.sleep(2)  # Evita redefinições do 'time'
                    else:
                        print(status)
                        break
            
            # Exibe a lista de pedidos no final
            if order_list:
                print("Seus pedidos:")
                for dept, order in order_list:
                    print(f"Departamento: {dept}, Pedido: {order}")
            else:
                print("Você não fez nenhum pedido.")
        
        finally:
            # Fecha o socket após o uso
            sock.close()

if __name__ == "__main__":
    submit_order()  # Executar a função principal
