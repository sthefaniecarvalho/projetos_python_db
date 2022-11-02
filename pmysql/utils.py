import MySQLdb


def conectar():
    """
    Função para conectar ao servidor
    """
    try:
        conn = MySQLdb.connect(
            db='pmysql',
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


def listar():
    """
    Função para listar os produtos
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()      #transformar em uma lista
    if len(produtos) > 0:
        print('-----LISTANDO PRODUTOS----')
        print('--------------------------')
        for produto in produtos:
            print(f'ID: {produto[0]}')
            print(f'Nome: {produto[1]}')
            print(f'Preco: {produto[2]}')
            print(f'Estoque: {produto[3]}')
            print('--------------------------')
    else:
        print('Não tem produtos cadastrados')
    desconectar(conn)


def inserir():
    """
    Função para inserir um produto
    """
    global nome
    conn = conectar()
    cursor = conn.cursor()
    try:
        nome = input('Nome do produto: ')
        preco = float(input('Preco: '))
        estoque = int(input('Quantidade em estoque: '))

        cursor.execute(f"INSERT INTO produtos (nome, preco, estoque) "
                       f"VALUES ('{nome}',{preco}, {estoque})")
        conn.commit()
    except ValueError as e:
        print(f'Valor inválido: {e}')

    if cursor.rowcount == 1:
        print(f"O produto {nome} foi inserido com sucesso")
    else:
        print('Não foi possivel inserir o produto.')
    desconectar(conn)


def atualizar():
    """
    Função para atualizar um produto
    """
    global nome
    conn = conectar()
    cursor = conn.cursor()

    try:
        id = int(input('Informe o id do produto: '))
        nome = input('Informe o novo nome do produto: ')
        preco = float(input('Informe o novo preco do produto: '))
        estoque = int(input('Informe o estoque do produto: '))

        cursor.execute(f"UPDATE produtos SET nome= '{nome}', preco= {preco}, estoque={estoque} WHERE id ={id}")
        conn.commit()
    except ValueError as e:
        print(f'Valor inválido: {e}')

    if cursor.rowcount == 1:
        print(f"O produto {nome} foi atualizado com sucesso")
    else:
        print('Não foi possivel atualizar o produto.')
    desconectar(conn)


def deletar():
    """
    Função para deletar um produto
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        id = int(input('Informe o id do produto: '))

        cursor.execute(f"DELETE FROM produtos WHERE id = {id}")
        conn.commit()
    except ValueError as e:
        print(f'Valor inválido: {e}')

    if cursor.rowcount == 1:
        print(f"O produto foi deletado")
    else:
        print('Não foi possivel deletar o produto.')
    desconectar(conn)

def menu():
    """
    Função para gerar o menu inicial
    """
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar produtos.')
    print('2 - Inserir produtos.')
    print('3 - Atualizar produto.')
    print('4 - Deletar produto.')
    opcao = int(input())
    if opcao in [1, 2, 3, 4]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
