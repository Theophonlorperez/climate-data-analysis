
import csv
import matplotlib.pyplot as plt

# Função para carregar os dados do arquivo CSV
def carregar_dados_csv(caminho_arquivo):
    dados = []
    with open(caminho_arquivo, 'r') as arq:
        leitor = csv.reader(arq)
        cabecalho = next(leitor)  # Ler o cabeçalho
        for linha in leitor:
            # Verificar se a linha não está vazia e tem o número esperado de colunas
            if linha and len(linha) >= 8:
                dados.append(linha)
    return dados

# Função para pedir mês e ano válidos
def pedir_mes_ano(tipo="inicial"):
    while True:
        mes = input(f"Digite o mês {tipo} (01-12), para saber os dados: ")
        mes = mes.zfill(2)  # Garantir que o mês tenha 2 dígitos, mesmo que o usuário digite "5"
        if mes not in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            print("Mês inválido! Por favor, insira um mês de 01 a 12.")
            continue
        ano = input(f"Digite o ano {tipo} (entre 1961 e 2016), para saber os dados: ")
        if not ano.isdigit() or int(ano) < 1961 or int(ano) > 2016:
            print("Ano inválido! O ano deve estar entre 1961 e 2016.")
            continue
        return mes, int(ano)

# Função para filtrar os dados conforme o período e tipo de dado
def filtrar_dados(dados, mes_inicio, ano_inicio, mes_fim, ano_fim, tipo_dado):
    dados_filtrados = []
    for linha in dados:
        # Certificar-se de que a linha tenha dados suficientes
        if len(linha) >= 8:
            data = linha[0]  
            dia, mes, ano = data.split('/')
            
            # Verificar se o mês e o ano estão dentro do intervalo solicitado
            if ((int(ano) > ano_inicio or (int(ano) == ano_inicio and int(mes) >= int(mes_inicio))) and
                (int(ano) < ano_fim or (int(ano) == ano_fim and int(mes) <= int(mes_fim)))):

                # Verificar o tipo de dado solicitado
                if tipo_dado == '1':  # Todos os dados
                    dados_filtrados.append(linha)
                elif tipo_dado == '2' and linha[1] != '':  # Apenas precipitação
                    dados_filtrados.append(linha)
                elif tipo_dado == '3' and linha[3] != '' and linha[4] != '':  # Apenas temperatura
                    dados_filtrados.append(linha)
                elif tipo_dado == '4' and linha[6] != '' and linha[7] != '':  # Apenas umidade e vento
                    dados_filtrados.append(linha)
    return dados_filtrados

# Função para calcular a média da temperatura mínima para um mês específico entre 2006 e 2016
def calcular_media_temperatura_minima(dados, mes):
    medias = {}
    for ano in range(2006, 2017):
        for linha in dados:
            if len(linha) >= 8:
                data = linha[0]
                dia, mes_dado, ano_dado = data.split('/')
                if mes_dado == mes and ano_dado == str(ano):
                    temp_minima = float(linha[3]) if linha[3] else None
                    if temp_minima is not None:
                        if mes+str(ano) not in medias:
                            medias[mes+str(ano)] = []
                        medias[mes+str(ano)].append(temp_minima)

    medias_ano = {k: sum(v)/len(v) for k, v in medias.items()}
    return medias_ano

# Função para gerar o gráfico das médias de temperatura mínima
def gerar_grafico_temperaturas(medias_ano):
    anos = [ano for ano in medias_ano]
    medias = [media for media in medias_ano.values()]
    
    plt.figure(figsize=(10,6))
    plt.bar(anos, medias, color='blue')
    plt.title('Média da Temperatura Mínima por Ano (2006-2016)')
    plt.xlabel('Ano')
    plt.ylabel('Temperatura Mínima (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Função para pedir mês válido (de 01 a 12)
def pedir_mes():
    while True:
        mes = input("Digite o mês para calcular a média da temperatura mínima (01-12): ")
        
        # Garantir que o mês tenha dois dígitos
        mes = mes.zfill(2)
        
        # Verificar se o mês está entre 01 e 12
        if mes.isdigit() and 1 <= int(mes) <= 12:
            return mes
        else:
            print("Mês inválido! Por favor, insira um mês entre 01 e 12.")

# Função para encontrar o mês e ano mais chuvoso
def mes_ano_mais_chuvoso(dados):
    precipitacao_por_mes = {}
    
    for linha in dados:
        if len(linha) >= 8:
            data = linha[0]  # Data no formato dd/mm/yyyy
            dia, mes, ano = data.split('/')
            precipitacao = linha[1]  # Precipitação 
            
            if precipitacao and precipitacao != '':
                precipitacao = float(precipitacao)
                mes_ano = f"{mes}/{ano}"
                if mes_ano not in precipitacao_por_mes:
                    precipitacao_por_mes[mes_ano] = 0
                precipitacao_por_mes[mes_ano] += precipitacao
    
    # Encontrar o mês/ano com maior precipitação
    mes_ano_max = max(precipitacao_por_mes, key=precipitacao_por_mes.get)
    maior_precipitacao = precipitacao_por_mes[mes_ano_max]
    
    return mes_ano_max, maior_precipitacao

# Função principal
def main():
    # Carregar os dados do arquivo
    dados = carregar_dados_csv('Anexo_Arquivo_Dados_Projeto_Logica_e_programacao_de_computadores.csv')

    # Encontrar o mês/ano com maior precipitação
    mes_ano_max, maior_precipitacao = mes_ano_mais_chuvoso(dados)
    print(f'\nO mês/ano mais chuvoso foi {mes_ano_max} com uma precipitação total de {maior_precipitacao:.2f} mm.\n')

    # Pedir mês e ano inicial
    mes_inicio, ano_inicio = pedir_mes_ano(tipo='inicial')

    # Pedir mês e ano final
    mes_fim, ano_fim = pedir_mes_ano(tipo='final')

    # Verificar se o intervalo é válido
    while (ano_fim < ano_inicio) or (ano_fim == ano_inicio and int(mes_fim) < int(mes_inicio)):
        print('O período final não pode ser anterior ao período inicial.')
        mes_fim, ano_fim = pedir_mes_ano(tipo='final')

    # Solicitar tipo de dado a visualizar
    print('\nEscolha o tipo de dado a visualizar:')
    print('1 - Todos os dados')
    print('2 - Apenas os dados de precipitação')
    print('3 - Apenas os dados de temperatura')
    print('4 - Apenas os dados de umidade e vento')
    tipo_dado = input('Digite o número correspondente à opção desejada: ')

    # Validar a escolha do tipo de dado
    while tipo_dado not in ['1', '2', '3', '4']:
        print('Opção inválida! Por favor, escolha uma das opções: 1, 2, 3 ou 4.')
        tipo_dado = input('Digite o número correspondente à opção desejada: ')

    dados_filtrados = filtrar_dados(dados, mes_inicio, ano_inicio, mes_fim, ano_fim, tipo_dado)

    # Exibir os dados filtrados
    if dados_filtrados:
        if tipo_dado == '1':  # Todos os dados
            print(f'\n{'Data':<12}{'Precipitação':<15}{'Temp. Máxima':<15}{'Temp. Mínima':<15}{'Umidade':<15}{'Vento':<15}')
            print('='*90)  
            for linha in dados_filtrados:
                data = linha[0]  
                print(f'{data:<12}{linha[1]:<15}{linha[2]:<15}{linha[3]:<15}{linha[6]:<15}{linha[7]:<15}')
        else:  # Para as opções 2, 3 ou 4
            if tipo_dado == '2':  # Apenas precipitação
                print('\nData e Precipitação:')
                print(f'{'Data':<12}{'Precipitação':<15}')
            elif tipo_dado == '3':  # Apenas temperatura
                print('\nData, Temperatura Máxima e Mínima:')
                print(f'{'Data':<12}{'Temp. Máxima':<15}{'Temp. Mínima':<15}')
            elif tipo_dado == '4':  # Apenas umidade e vento
                print('\nData, Umidade e Vento:')
                print(f'{'Data':<12}{'Umidade':<15}{'Vento':<15}')

            for linha in dados_filtrados:
                data = linha[0]
                if tipo_dado == '2':  # Apenas precipitação
                    print(f"{data:<12}{linha[1]:<15}")
                elif tipo_dado == '3':  # Apenas temperatura
                    print(f"{data:<12}{linha[3]:<15}{linha[4]:<15}")
                elif tipo_dado == '4':  # Apenas umidade e vento
                    print(f"{data:<12}{linha[6]:<15}{linha[7]:<15}")
    else:
        print('Nenhum dado encontrado para o período solicitado.')

    # Calcular a média da temperatura mínima para o mês solicitado de 2006 a 2016
    mes = pedir_mes()

    medias_ano = calcular_media_temperatura_minima(dados, mes)

    print(f'\nMédia da temperatura mínima para o mês {mes} de 2006 a 2016:')
    for mes_ano, media in medias_ano.items():
        print(f'{mes_ano}: {media:.2f}°C')
        
    medias = list(medias_ano.values())
    media_das_medias = sum(medias) / len(medias) if medias else 0
    
    print(f'\nMédia das médias das temperaturas mínimas para o mês {mes} de 2006 a 2016: {media_das_medias:.2f}°C')

    # Gerar gráfico das médias de temperatura mínima
    gerar_grafico_temperaturas(medias_ano)

if __name__ == '__main__':
    main()























