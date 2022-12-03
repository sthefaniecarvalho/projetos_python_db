import redis


def gera_id():
    try:
        conn = conectar()
        chave = conn.get('chave')

        if chave:
            chave = conn.incr('chave')
            return chave
        else:
            conn.set('chave', 1)
            return 1
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível gerar a chave. {e}')


def conectar():
    """
    Função para conectar ao servidor
    """
    return redis.Redis(host='localhost', port=6379)


def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
    conn.connection_pool.disconnect()


def listar():
    """
    Função para listar os produtos
    """
    conn = conectar()
    try:
        dados = conn.keys(pattern='produtos:*')

        if len(dados) > 0:
            print('Listando produtos...')
            print('--------------------')
            for chave in dados:
                produto = conn.hgetall(chave)
                print(f"ID: {str(chave, 'utf-8', 'ignore')}")
                print(f"Produto: {str(produto[b'nome'], 'utf-8', 'ignore')}")
                print(f"Preço: {str(produto[b'preco'], 'utf-8', 'ignore')}")
                print(f"Estoque: {str(produto[b'estoque'], 'utf-8', 'ignore')}")
                print('------------------')
        else:
            print('Não existem produtos cadastrados.')
    except redis.exceptions.ConnectionError as e:
        print(f"Não foi possível listar produtos. {e}")
    desconectar(conn)


def inserir():
    """
    Função para inserir um produto
    """  
    conn = conectar()
    
    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço: '))
    estoque = int(input('Informe o estoque: '))

    produto = {"nome": nome, "preco": preco, "estoque": estoque}
    chave = f'produtos:{gera_id()}'

    try:
        res = conn.hmset(chave, produto)
        if res:
            print(f'O produto {nome} foi inserido com sucesso.')
        else:
            print('Não foi possível inserir o produto.')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível inserir o produto: {e}')
    desconectar(conn)


def atualizar():
    """
    Função para atualizar um produto
    """
    conn = conectar()

    chave = input('Informe a chave: ')
    dados = conn.keys(pattern='produtos:*')
    dados = [str(chave, 'utf-8', 'ignore') for chave in dados]

    if chave not in dados:
        print(f"Chave não encontrada: {chave}")
        desconectar(conn)
    else:
        nome = input('Informe o nome do produto: ')
        preco = float(input('Informe o preço: '))
        estoque = int(input('Informe o estoque: '))

        produto = {"nome": nome, "preco": preco, "estoque": estoque}

        try:
            res = conn.hmset(chave, produto)
            if res:
                print(f'O produto {nome} foi atualizado com sucesso.')
        except redis.exceptions.ConnectionError as e:
            print(f'Não foi possível atualizar o produto: {e}')
        desconectar(conn)


def deletar():
    """
    Função para deletar um produto
    """
    conn = conectar()
    chave = input('Informe a chave: ')
    dados = conn.keys(pattern='produtos:*')
    dados = [str(chave, 'utf-8', 'ignore') for chave in dados]

    if chave not in dados:
        print(f"Chave não encontrada: {chave}")
        desconectar(conn)
    else:
        try:
            res = conn.delete(chave)
            if res == 1:
                print(f'O produto foi deletado com sucesso.')
            else:
                print("Não foi possível deletar o produto.")

        except redis.ConnectionError as e:
            print(f"Error: {e}")
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
    print('5 - Sair')

    opcao = 1
    while opcao in [1, 2, 3, 4, 5]:
        opcao = int(input())
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        elif opcao == 5:
            print('Encerrado.')
            exit()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
