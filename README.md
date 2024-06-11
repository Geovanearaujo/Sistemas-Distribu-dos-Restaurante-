**Projeto de gestão de restaurante**

O projeto é um sistema de gestão de restaurante que faz a interação entre cliente e servidor utilizando sockets e threads para otimizar as operações do estabelecimento. Através de uma arquitetura de comunicação baseada em sockets, viabilizando a realização de pedidos, consultas de menu em tempo real. A implementação de threads possibilita o processamento concorrente de múltiplas solicitações, garantindo uma resposta ágil e sem interrupções mesmo em períodos de alta demanda. Essa abordagem visa aprimorar a experiência do cliente e otimizar a eficiência operacional do restaurante, proporcionando uma gestão mais ágil e precisa.

**Breve explicação de cada arquivo do projeto**

**Server.py**

O arquivo server.py configura um servidor XML-RPC e um servidor socket para gerenciar pedidos em um sistema de restaurante. O servidor XML-RPC escuta na porta 8080 e oferece funções para obter o menu, receber pedidos e verificar o status do pedido. O servidor socket escuta na porta 8082, aceitando conexões para enviar e receber mensagens dos clientes. Funções adicionais, como "prepare_food", simulam a preparação do pedido, atualizando o status quando o pedido estiver pronto.

**Server_mult.py**

O arquivo server_mult.py configura servidores XML-RPC e socket em portas diferentes, 8080 e 12345, respectivamente. Apresentando uma estrutura semelhante ao server.py, incluindo a função de "client_handler" que lida com as conexões dos clientes de forma mais robusta, respondendo a mensagens e aceitando múltiplas conexões simultaneamente por meio de threads. O servidor XML-RPC oferece as mesmas funções do server.py, enquanto o servidor socket usa threads para gerenciar conexões e responder aos clientes.

**Client.py**

O arquivo client.py representa um cliente que se conecta ao servidor XML-RPC para interagir com o sistema. Permitindo que o cliente obtenha o menu com os departamentos e serviços oferecidos, podendo fazer pedidos e verificar o status do pedido. O cliente se conecta ao servidor socket, mas a conexão é usada principalmente para inicializar a comunicação.

**Client_mult.py**

O arquivo client_mult.py é semelhante ao client.py, mas utiliza um servidor socket em uma porta diferente, 12345, para interações mais robustas. Estabelecendo uma conexão com o servidor socket e recebendo uma mensagem de boas-vindas antes de iniciar a interação com o servidor XML-RPC. A estrutura do código permite que o cliente faça pedidos, verifique o menu e obtenha o status do pedido, além de armazenar uma lista dos pedidos feitos para referência posterior. O código inclui exceções para garantir que as conexões de socket sejam encerradas corretamente no final da interação.
