import psycopg2


def conectar():
    """
    Função para conectar ao servidor
    """
    try:
        conn = psycopg2.connect(
            database='ppostgresql',
            host='localhost',
            user='geek',
            password='university'
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error na conexão com PostgreSQL {e}")


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
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()

        if len(produtos) > 0:
            print('-----LISTANDO PRODUTOS----')
            print('--------------------------')
            for produto in produtos:
                print(f"ID: {produto[0]}")
                print(f"Produto: {produto[1]}")
                print(f"Preço: {produto[2]}")
                print(f"Estoque: {produto[3]}")
        else:
            print("Não há produtos cadastrados")
        desconectar(conn)
    except AttributeError as e:
        print(f"Erro no cursor: {e}")


def inserir():
    """
    Função para inserir um produto
    """  
    conn = conectar()
    cursor = conn.cursor()
    try:
        nome = input("Informe o nome do produto: ")
        preco = float(input("Informe o preço do produto: "))
        estoque = int(input("Informe a quantidade de estoque: "))

        cursor.execute("INSERT INTO produtos (nome, preco, estoque) "
                       f"VALUES ('{nome}', {preco}, {estoque})")
        conn.commit()

    except ValueError as err:
        print(f"Valor inválido: {err}")

    if cursor.rowcount == 1:
        print("O produto foi adicionado com sucesso!")
    else:
        print("Não foi possivel inserir o produto.")
    desconectar(conn)


def atualizar():
    """
    Função para atualizar um produto
    """
    global id
    conn = conectar()
    cursor = conn.cursor()

    try:
        id = int(input("Informe o id do produto: "))
        nome = input("Informe o novo nome do produto: ")
        preco = float(input("Informe o novo preco do produto: "))
        estoque = int(input("Informe o novo estoque do produto: "))

        cursor.execute(f"UPDATE produtos SET nome='{nome}', preco={preco},"
                       f"estoque={estoque} WHERE id={id}")

        conn.commit()

    except ValueError as err:
        print(f"Valor inválido: {err}")

    if cursor.rowcount == 1:
        print("Produto atualizado com sucesso.")
    else:
        print(f"Não foi possivel atualizar o produto com id {id}.")
    desconectar(conn)


def deletar():
    """
    Função para deletar um produto
    """
    global id
    conn = conectar()
    cursor = conn.cursor()

    try:
        id = input("Informe o id do produto: ")
        cursor.execute(f"DELETE FROM produtos WHERE id={id}")

        conn.commit()
    except ValueError as err:
        print(f"Valor inválido: {err}")

    if cursor.rowcount == 1:
        print("Produto deletado com sucesso.")
    else:
        print(f"Erro ao deletar produto com id {id}..")


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
