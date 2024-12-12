import pandas as pd

data_vencimento = "25102024"

df = pd.read_excel('inputs/Extrato mensal Ecos.xlsx')
df_modificate = df.copy()

df_proventos = df_modificate[['cp_codi_epr', 'cp_nome_epr', 'cp_situacao', 'cp_cpf', 'cp_codi_eve_p', 'cp_nome_eve_p', 'cp_eve_inf_p', 'cp_eve_val_p', 'cp_eve_pod_p']]
df_proventos = df_proventos.dropna()

df_funcinarios = pd.read_excel('dados/funcionarios_cigam.xlsx') # planilha com o codigo dos funcionarios no sistema CIGAM
df_depara_contas = pd.read_excel('dados/depara_contas.xlsx')    # planilha com depara de contas financeiras com os eventos

# Passo 1: Converter 'cp_codi_eve_p' para inteiro
df_proventos['cp_codi_eve_p'] = df_proventos['cp_codi_eve_p'].astype(int)

# Passo 2: Limpar e converter 'cp_eve_val_p' para float
df_proventos['cp_eve_val_p'] = (
    df_proventos['cp_eve_val_p']
    .str.replace('.', '', regex=False)  # Remove o separador de milhar
    .str.replace(',', '.', regex=False)  # Substitui a vírgula pelo ponto
    .astype(float)  # Converte para float
)

df_descontos = df_modificate[['cp_codi_epr', 'cp_nome_epr', 'cp_situacao', 'cp_cpf', "cp_codi_eve_d", "cp_nome_eve_d", "cp_eve_inf_d", "cp_eve_val_d", "cp_eve_pod_d"]]    
df_descontos = df_descontos.dropna()

# Passo 1: Converter 'cp_codi_eve_p' para inteiro
df_descontos['cp_codi_eve_d'] = df_descontos['cp_codi_eve_d'].astype(int)

# Passo 2: Limpar e converter 'cp_eve_val_p' para float
df_descontos['cp_eve_val_d'] = (
    df_descontos['cp_eve_val_d']
    .str.replace('.', '', regex=False)  # Remove o separador de milhar
    .str.replace(',', '.', regex=False)  # Substitui a vírgula pelo ponto
    .astype(float)  # Converte para float
)

df_merge_p = pd.merge(pd.merge(df_proventos, df_funcinarios, left_on='cp_cpf', right_on='CNPJ/CPF'), df_depara_contas, left_on='cp_codi_eve_p', right_on='codigo_dominio')  # Merge para conseguir o codigo do funcionario e o depara das contas dos eventos de proventos
df_merge_d = pd.merge(pd.merge(df_descontos, df_funcinarios, left_on='cp_cpf', right_on='CNPJ/CPF'), df_depara_contas, left_on='cp_codi_eve_d', right_on='codigo_dominio')  # Merge para conseguir o codigo do funcionario e o depara das contas dos eventos de descontos

# Unificar as informações em uma lista ja no modelo da planilha de gerador de linha
dados_gerador_linhas = []

# transformar df proventos em lista e deixar no formato do gerador de linhas
lista_df_proventos = df_merge_p.values.tolist()
for dado in lista_df_proventos:
    dados_gerador_linhas.append(
        [
            f"{dado[1]}", "CTB", "000001", "0", f"{data_vencimento}", "000000", "000000", f"{str(round(dado[7], 2)).replace('.', '')}",
            "P09", f"{str(dado[9]).zfill(6)}", f"{dado[-1].replace('.', '')}", "000000", f"FOLHA PAGAMENTO - {dado[17]}",
            f"CTB;000001;0;{data_vencimento};000000;000000;{str(round(dado[7], 2)).replace('.', '')};P09;{str(dado[9]).zfill(6)};{dado[-1].replace('.', '')};000000;FOLHA PAGAMENTO - {dado[17]}"
        ]
    )

# transformar df proventos em lista e deixar no formato do gerador de linhas
lista_df_descontos = df_merge_d.values.tolist()
for dado in lista_df_descontos:
    dados_gerador_linhas.append(
        [
            f"{dado[1]}", "CTB", "000001", "0", f"{data_vencimento}", "000000", "000000", f"{str(round(dado[7], 2)).replace('.', '')}",
            "P09", f"{str(dado[9]).zfill(6)}", f"{dado[-1].replace('.', '')}", "000000", f"FOLHA PAGAMENTO - {dado[17]}",
            f"CTB;000001;0;{data_vencimento};000000;000000;{str(round(dado[7], 2)).replace('.', '')};P09;{str(dado[9]).zfill(6)};{dado[-1].replace('.', '')};000000;FOLHA PAGAMENTO - {dado[17]}"
        ]
    )


# Definindo as colunas
colunas = ['Nome campo', 'CTB', 'UN', 'VAR3', 'VENCIMENTO', 'DEBITO', 'CREDITO', 'VALOR', 'CODIGO HISTORICO', 'EMPRESA', ' CONTA', 'CENTRO CUSTO', 'COMPLEMENTO HIT.', 'Linha']

df_gerador = pd.DataFrame(dados_gerador_linhas, columns=colunas)

df_gerador.to_excel('Gerador_linhas_layout.xlsx', index=False)
