import datetime

print(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))

"""


        qtd_pizzas = int(input("Informe a quantidade de pizzas: "))
        for i in range(qtd_pizzas):
            id_pizza = int(input("Id do sabor da pizza: "))
            id_pedido = int(input("Id do pedido: "))
            quantidade = int(input("Quantidade: "))
            tamanho = int(input("Id tamanho: "))

            cursor.execute(f"INSERT INTO pedidos_pizzas (id_pizzas, id_pedido, quantidade, "
                           f"id_tamanho) VALUES ({id_pizza}, {id_pizza}, {id_pedido},"
                           f"{quantidade}, {tamanho}")
        conn.comit()
"""