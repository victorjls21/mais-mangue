# Importa a biblioteca os para trabalhar com caminhos de arquivos
import os

# Importa sqlite3 para usar banco de dados SQLite
import sqlite3


# Define o nome e caminho do banco de dados
DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mangue.db")


# Função para conectar ao banco de dados
def conectar():
    # Cria conexão com o banco SQLite
    conn = sqlite3.connect(DB_NAME)

    # Permite acessar os dados pelo nome das colunas
    conn.row_factory = sqlite3.Row

    # Retorna a conexão
    return conn


# Função para criar as tabelas do sistema
def criar_tabelas():
    # Abre conexão com o banco
    conn = conectar()

    # Cria tabela para armazenar denúncias da população
    conn.execute("""
        CREATE TABLE IF NOT EXISTS denuncias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            localizacao TEXT NOT NULL,
            descricao TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Cria tabela para armazenar projetos ambientais
    conn.execute("""
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            area TEXT NOT NULL,
            valor REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Cria tabela para armazenar investimentos das empresas
    conn.execute("""
        CREATE TABLE IF NOT EXISTS investimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            projeto TEXT NOT NULL,
            valor REAL NOT NULL,
            carbono_compensado REAL NOT NULL
        )
    """)

    # Salva as tabelas criadas
    conn.commit()

    # Fecha conexão
    conn.close()


# FUNÇÕES DO APP - POPULAÇÃO

# Função para registrar denúncia ambiental
def registrar_denuncia(tipo, localizacao, descricao):
    # Abre conexão com o banco
    conn = conectar()

    # Insere a denúncia na tabela denuncias
    cursor = conn.execute(
        """INSERT INTO denuncias
           (tipo, localizacao, descricao, status)
           VALUES (?, ?, ?, ?)""",
        (tipo, localizacao, descricao, "Em análise"),
    )

    # Salva no banco
    conn.commit()

    # Fecha conexão
    conn.close()

    # Retorna o ID da denúncia criada
    return cursor.lastrowid


# Função para listar denúncias cadastradas
def listar_denuncias():
    # Abre conexão
    conn = conectar()

    # Busca todas as denúncias registradas
    linhas = conn.execute(
        "SELECT id, tipo, localizacao, descricao, status FROM denuncias ORDER BY id"
    ).fetchall()

    # Fecha conexão
    conn.close()

    # Converte as linhas em lista de dicionários
    return [dict(linha) for linha in linhas]


# Função para atualizar o status de uma denúncia
def atualizar_status_denuncia(denuncia_id, novo_status):
    # Abre conexão
    conn = conectar()

    # Atualiza o status da denúncia pelo ID
    cursor = conn.execute(
        "UPDATE denuncias SET status = ? WHERE id = ?",
        (novo_status, denuncia_id),
    )

    # Salva alteração
    conn.commit()

    # Fecha conexão
    conn.close()

    # Retorna True se alguma denúncia foi atualizada
    return cursor.rowcount > 0


# Função para calcular EcoPontos da população
def calcular_ecopontos(qtd_denuncias, qtd_participacoes):
    # Cada denúncia vale 10 pontos e cada participação vale 30 pontos
    pontos = (qtd_denuncias * 10) + (qtd_participacoes * 30)

    # Define ranking com base na pontuação
    if pontos >= 200:
        ranking = "Ouro"
    elif pontos >= 100:
        ranking = "Prata"
    else:
        ranking = "Bronze"

    # Retorna pontuação e ranking
    return pontos, ranking



# FUNÇÕES DA PLATAFORMA - EMPRESAS


# Função para criar projeto ambiental
def criar_projeto(nome, area, valor):
    # Abre conexão
    conn = conectar()

    # Insere projeto ambiental no banco
    cursor = conn.execute(
        """INSERT INTO projetos
           (nome, area, valor, status)
           VALUES (?, ?, ?, ?)""",
        (nome, area, valor, "Ativo"),
    )

    # Salva no banco
    conn.commit()

    # Fecha conexão
    conn.close()

    # Retorna o ID do projeto criado
    return cursor.lastrowid


# Função para listar projetos ambientais
def listar_projetos():
    # Abre conexão
    conn = conectar()

    # Busca todos os projetos cadastrados
    linhas = conn.execute(
        "SELECT id, nome, area, valor, status FROM projetos ORDER BY id"
    ).fetchall()

    # Fecha conexão
    conn.close()

    # Retorna projetos como lista de dicionários
    return [dict(linha) for linha in linhas]


# Função para calcular carbono emitido pela empresa
def calcular_carbono(consumo_energia, km_frota, residuos):
    # Fórmula simples e simulada para estimar carbono
    carbono = (consumo_energia * 0.0005) + (km_frota * 0.0002) + (residuos * 0.8)

    # Retorna o valor estimado em toneladas de CO2
    return carbono


# Função para registrar investimento de empresa em projeto ambiental
def investir_em_projeto(empresa, projeto, valor):
    # Estimativa simples de carbono compensado
    carbono_compensado = valor * 0.05

    # Abre conexão
    conn = conectar()

    # Insere investimento no banco
    cursor = conn.execute(
        """INSERT INTO investimentos
           (empresa, projeto, valor, carbono_compensado)
           VALUES (?, ?, ?, ?)""",
        (empresa, projeto, valor, carbono_compensado),
    )

    # Salva no banco
    conn.commit()

    # Fecha conexão
    conn.close()

    # Retorna ID do investimento e carbono compensado
    return cursor.lastrowid, carbono_compensado


# Função para listar investimentos feitos pelas empresas
def listar_investimentos():
    # Abre conexão
    conn = conectar()

    # Busca investimentos cadastrados
    linhas = conn.execute(
        "SELECT id, empresa, projeto, valor, carbono_compensado FROM investimentos ORDER BY id"
    ).fetchall()

    # Fecha conexão
    conn.close()

    # Retorna investimentos em formato de lista
    return [dict(linha) for linha in linhas]


# Função para gerar relatório ESG simples
def gerar_relatorio_esg():
    # Busca dados de denúncias, projetos e investimentos
    denuncias = listar_denuncias()
    projetos = listar_projetos()
    investimentos = listar_investimentos()

    # Soma o valor total investido pelas empresas
    total_investido = sum(i["valor"] for i in investimentos)

    # Soma o carbono compensado estimado
    total_carbono = sum(i["carbono_compensado"] for i in investimentos)

    # Exibe relatório no terminal
    print("\n===== RELATÓRIO ESG +MANGUE =====")
    print(f"Denúncias registradas: {len(denuncias)}")
    print(f"Projetos ativos: {len(projetos)}")
    print(f"Total investido: R$ {total_investido:.2f}")
    print(f"Carbono compensado estimado: {total_carbono:.2f} tCO2e")
    print("Certificação: Selo ODS 13")
    print("=================================\n")


# FUNÇÃO DE EXIBIÇÃO


# Função para exibir qualquer lista de registros
def exibir_lista(lista):
    # Se a lista estiver vazia, mostra mensagem
    if not lista:
        print("Nenhum registro encontrado.")
        return

    # Percorre e imprime cada item da lista
    for item in lista:
        print(item)



# MENU DO APP


# Menu que representa o aplicativo da população
def menu_app():
    # Mantém o menu aberto até o usuário escolher voltar
    while True:
        print("\n===== APP POPULAÇÃO =====")
        print("1 - Registrar denúncia")
        print("2 - Listar denúncias")
        print("3 - Ver EcoPontos")
        print("0 - Voltar")

        # Recebe opção digitada
        opcao = input("Escolha uma opção: ")

        # Registra denúncia
        if opcao == "1":
            tipo = input("Tipo do problema: ")
            localizacao = input("Localização: ")
            descricao = input("Descrição: ")

            novo_id = registrar_denuncia(tipo, localizacao, descricao)

            print(f"Denúncia registrada com id {novo_id}.")

        # Lista denúncias
        elif opcao == "2":
            exibir_lista(listar_denuncias())

        # Calcula EcoPontos
        elif opcao == "3":
            qtd_denuncias = len(listar_denuncias())
            qtd_participacoes = int(input("Quantidade de ações ambientais que participou: "))

            pontos, ranking = calcular_ecopontos(qtd_denuncias, qtd_participacoes)

            print(f"Você possui {pontos} EcoPontos. Ranking: {ranking}")

        # Volta ao menu principal
        elif opcao == "0":
            break

        # Caso a opção não exista
        else:
            print("Opção inválida.")



# MENU DA PLATAFORMA


# Menu que representa a plataforma das empresas
def menu_plataforma():
    # Mantém o menu aberto até o usuário escolher voltar
    while True:
        print("\n===== PLATAFORMA EMPRESAS =====")
        print("1 - Criar projeto ambiental")
        print("2 - Listar projetos")
        print("3 - Calcular carbono")
        print("4 - Investir em projeto")
        print("5 - Gerar relatório ESG")
        print("0 - Voltar")

        # Recebe opção escolhida
        opcao = input("Escolha uma opção: ")

        # Cria projeto ambiental
        if opcao == "1":
            nome = input("Nome do projeto: ")
            area = input("Área/local do projeto: ")
            valor = float(input("Valor necessário: "))

            novo_id = criar_projeto(nome, area, valor)

            print(f"Projeto criado com id {novo_id}.")

        # Lista projetos
        elif opcao == "2":
            exibir_lista(listar_projetos())

        # Calcula carbono
        elif opcao == "3":
            energia = float(input("Consumo de energia (kWh): "))
            km = float(input("Km rodados pela frota: "))
            residuos = float(input("Resíduos gerados (toneladas): "))

            carbono = calcular_carbono(energia, km, residuos)

            print(f"Pegada de carbono estimada: {carbono:.2f} tCO2e")

        # Registra investimento
        elif opcao == "4":
            empresa = input("Nome da empresa: ")
            projeto = input("Nome do projeto apoiado: ")
            valor = float(input("Valor do investimento: "))

            investimento_id, carbono = investir_em_projeto(empresa, projeto, valor)

            print(f"Investimento registrado com id {investimento_id}.")
            print(f"Carbono compensado estimado: {carbono:.2f} tCO2e")

        # Gera relatório ESG
        elif opcao == "5":
            gerar_relatorio_esg()

        # Volta ao menu principal
        elif opcao == "0":
            break

        # Opção inválida
        else:
            print("Opção inválida.")



# MENU PRINCIPAL


# Menu principal do sistema +Mangue
def menu_principal():
    # Cria as tabelas no banco caso ainda não existam
    criar_tabelas()

    # Mantém o menu principal aberto
    while True:
        print("\n===== +MANGUE =====")
        print("1 - App da população")
        print("2 - Plataforma das empresas")
        print("0 - Sair")

        # Recebe opção do usuário
        opcao = input("Escolha uma opção: ")

        # Abre menu do app
        if opcao == "1":
            menu_app()

        # Abre menu da plataforma
        elif opcao == "2":
            menu_plataforma()

        # Encerra o sistema
        elif opcao == "0":
            print("Saindo...")
            break

        # Opção inválida
        else:
            print("Opção inválida.")


# Verifica se o arquivo está sendo executado diretamente
if __name__ == "__main__":
    # Inicia o sistema
    menu_principal()