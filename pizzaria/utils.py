import datetime

import MySQLdb


def conectar():
    """
    Função para conectar ao servidor
    """
    try:
        conn = MySQLdb.connect(
            db='pizzaria',
            host='localhost',
            user='geek',
            passwd='university'
        )
        return conn
    except MySQLdb.Error as e:
        print(f'Error na conexão ao Mysql Server: {e}')


def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
    if conn:
        conn.close()


def listar_pedidos():
    """
    Função para listar os pedidos
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT pp.id_pedido, pe.data, c.nome AS 'Cliente', SUM(pp.quantidade) "
                   "AS quantidade, SUM(pip.preco * pp.quantidade) AS subtotoal,"
                   "b.taxa_entrega, (SUM(pip.preco * pp.quantidade)) + b.taxa_entrega "
                   "AS total, b.tempo_espera, pe.status "
                   "FROM pedidos_pizzas AS pp, pizzas AS p, clientes AS c, pedidos AS pe, "
                   "pizzas_precos AS pip, tamanho AS t, bairros AS b, cep "
                   "WHERE pp.id_pedido = pe.id AND pe.id_cliente = c.id AND pp.id_pizza = "
                   "p.id AND pip.id_pizza = p.id AND pp.id_tamanho = t.id "
                   "AND pip.id_tamanho = t.id AND pe.id_bairro = b.id AND b.id_cep = cep.id "
                   "AND c.id_cep = cep.id "
                   "GROUP BY 1 ORDER BY pp.id_pedido;")

    pedidos = cursor.fetchall()      #transformar em uma lista
    if len(pedidos) > 0:
        print('---------PEDIDOS----------')
        print('--------------------------')
        for pedidos in pedidos:
            print(f'ID: {pedidos[0]}')
            print(f'Data: {pedidos[1]}')
            print(f'Cliente: {pedidos[2]}')
            print(f'Quantidade de pizzas: {pedidos[3]}')
            print(f"Subtotal: {pedidos[4]}")
            print(f'Taxa de entrega: {pedidos[5]}')
            print(f'Total: {pedidos[6]}')
            print(f'Tempo de espera: {pedidos[7]}')
            print(f'Status: {pedidos[8]}')
            print('--------------------------')
    else:
        print('Não tem produtos cadastrados')
    desconectar(conn)


def cardapio():
    """Função para mostar o cardapio"""

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT p.id AS 'id pizza', p.nome, pp.preco, t.id AS 'id tamanho', t.tamanho "
                   "FROM pizzas AS p, pizzas_precos AS pp, tamanho AS t WHERE pp.id_pizza = p.id "
                   "AND pp.id_tamanho = t.id;")

    cardapio = cursor.fetchall()

    print("-------------------CARDAPIO-----------------------------")
    print("--------------------------------------------------------")
    print("ID PIZZA|    PIZZA    | PREÇO     | ID TAMANHO    | TAMANHO |")
    for item in cardapio:
        print(f"  {item[0]}     |  {item[1]}  |   {item[2]}   |   {item[3]}   |   {item[4]} |")


    desconectar(conn)


def listar_clientes_bairros():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT c.id, c.nome, c.telefone, b.id AS 'id bairro' FROM clientes AS c, "
                   "bairros AS b, cep WHERE c.id_cep = cep.id AND b.id_cep = cep.id;")

    clientes = cursor.fetchall()
    print("-----------------------------")
    print("------LISTA CLIENTES---------")
    print("-----------------------------")
    print(f"ID CLIENTE | NOME |   TELEFONE    | ID BAIRRO   | ")
    for cliente in clientes:
        print(f"{cliente[0]} | {cliente[1]} | {cliente[2]} | {cliente[3]}")

    desconectar(conn)


def pedir_pizza():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT pedidos.id FROM pedidos")

    id = cursor.fetchall()

    qtd_pizzas = int(input("Informe a quantidade de pizzas: "))
    count = 0
    while count < qtd_pizzas:
        id_pizza = int(input("Id do sabor da pizza: "))
        id_pedido = max([x for i in id for x in i])
        quantidade = int(input("Quantidade: "))
        tamanho = int(input("Id tamanho: "))

        cursor.execute(f"INSERT INTO pedidos_pizzas (id_pizza, id_pedido, id_tamanho, quantidade) "
                       f"VALUES ({id_pizza},{id_pedido},{tamanho},{quantidade})")
        count += 1

    conn.commit()

    if cursor.rowcount == 1:
        print(f"Pedido feito com sucesso.")
    else:
        print('Não foi possivel realizar o pedido.')
    desconectar(conn)


def adicionar_pedido():
    """
    Função para fazer um pedido
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        data = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        status = "Processando"
        id_cliente = int(input('Id cliente: '))
        id_atendente = int(input('Id atendente: '))
        id_entregador = int(input('Id entregador: '))
        id_bairro = int(input("Id bairro: "))

        cursor.execute(f"INSERT INTO pedidos (data, status, id_cliente, id_atendente, id_entregador, id_bairro) "
                       f"VALUES ('{data}', '{status}', {id_cliente}, {id_atendente}, {id_entregador}, {id_bairro})")

        conn.commit()

    except ValueError as e:
        print(f'Valor inválido: {e}')

    if cursor.rowcount == 1:
        print(f"Informaçoes armazenadas com sucesso")
    else:
        print('Não foi possivel concluir.')
    desconectar(conn)


def alterar_status():
    """
    Função para alterar o status do pedido.
    """
    conn = conectar()
    cursor = conn.cursor()

    id = input("Informe id do pedido que deseja alterar o status: ")
    status = input("Status: ")

    cursor.execute(f"UPDATE pedidos SET status='{status}' WHERE id ={id};")

    if cursor.rowcount > 1:
        print(f"O status do pedido {id} foi atualizado com sucesso.")
    else:
        print("Não foi possível atualiar o status.")
    desconectar(conn)


def atualizar():
    """
    Função para atualizar um pedido
    """
    global id
    conn = conectar()
    cursor = conn.cursor()

    try:
        id = int(input('Informe o id do pedido: '))
        data = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        id_cliente = int(input('Id do novo cliente: '))
        status = input("Informe o novo status do pedido: ")
        id_atendente = int(input('Id do novo atendente: '))
        id_entregador = int(input('Id novo entregador: '))
        id_bairro = int(input("Id novo bairro: "))

        cursor.execute(f"UPDATE pedidos SET data= '{data}', status= '{status}', "
                       f"id_cliente={id_cliente}, id_atendente={id_atendente}, id_entregador={id_entregador},"
                       f"id_bairro={id_bairro} WHERE id ={id}")

        cursor.execute(f"DELETE FROM pedidos_pizzas WHERE id_pedido = {id}")

        qtd_pizzas = int(input("Informe a quantidade de pizzas: "))
        count = 0
        while count < qtd_pizzas:
            id_pizza = int(input("Id do sabor da pizza: "))
            quantidade = int(input("Quantidade: "))
            tamanho = int(input("Id tamanho: "))

            cursor.execute(f"INSERT INTO pedidos_pizzas (id_pizza, id_pedido, id_tamanho, quantidade) "
                           f"VALUES ({id_pizza},{id},{tamanho},{quantidade})")
            count += 1

        conn.commit()

    except ValueError as e:
        print(f'Valor inválido: {e}')

    if cursor.rowcount == 1:
        print(f"O pedido id={id} foi atualizado com sucesso")
    else:
        print('Não foi possivel atualizar o pedido.')
    desconectar(conn)


def deletar():
    """
    Função para deletar um produto
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        id = int(input('Informe o id do pedido: '))
        cursor.execute(f"DELETE FROM pedidos_pizzas WHERE id_pedido = {id}")
        cursor.execute(f"DELETE FROM pedidos WHERE id = {id}")

        conn.commit()
    except ValueError as e:
        print(f'Valor inválido: {e}')

    if cursor.rowcount == 1:
        print(f"O pedido foi deletado com sucesso.")
    else:
        print('Não foi possivel deletar o pedido.')
    desconectar(conn)


def menu():
    """
    Função para gerar o menu inicial
    """
    print('=========Gerenciamento==============')
    print('Selecione uma opção: ')
    print('1 - Listar pedidos')
    print('2 - Adicionar um pedido')
    print('3 - Alterar o status do pedido')
    print('4 - Alterar um pedido')
    print('5 - Deletar um pedido')
    opcao = int(input())
    if opcao in [1, 2, 3, 4, 5]:
        if opcao == 1:
            listar_pedidos()
        elif opcao == 2:
            cardapio()
            listar_clientes_bairros()
            adicionar_pedido()
            pedir_pizza()
        elif opcao == 3:
            alterar_status()
        elif opcao == 4:
            listar_clientes_bairros()
            atualizar()
        elif opcao == 5:
            deletar()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
