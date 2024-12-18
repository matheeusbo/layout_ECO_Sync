import streamlit as st
from read_files import gerar_layout_eco
import pandas as pd
import time
st.set_page_config(page_title="Sync", page_icon=":robot:", layout='wide')


def main():
    st.header('Gerar Layout')

    tab1, tab2 = st.tabs(['Gerar', 'Configurações'])
    with tab1:
        arquivo_file = st.file_uploader('Incluir arquivo folha', type='xlsx')
        data_vencimento = st.text_input('Data Vencimento (dd/mm/AAAA)', help='Formato: dd/mm/AAAA')

        if arquivo_file != None and data_vencimento != '':
            if st.button('Importar'):
                # st.write(arquivo_file)

                df = gerar_layout_eco(data_vencimento.replace('/', ''), planilha=arquivo_file)
                st.dataframe(df)
                
                # Convertendo o DataFrame para CSV
                csv = df['Linha'].to_csv(index=False, header=False)

                # Adicionando o botão de download
                st.download_button(
                    label="Baixar CSV",
                    data=csv,
                    file_name="layout.csv",
                    mime="text/csv"
                )
    
    with tab2:
        tab21, tab22 = st.tabs(['Cadastro Funcionarios', 'Depara Contas'])

        with tab21:
            df_funcinarios = pd.read_excel('dados/funcionarios_cigam.xlsx')
            data_func_edited = st.data_editor(df_funcinarios, use_container_width=True, num_rows='dynamic')

            if st.button('Salvar', key='salvar_funcionario'):
                data_func_edited.to_excel('dados/funcionarios_cigam.xlsx', index=False)
                st.success('Salvo com Sucesso')

                time.sleep(3)
                st.rerun()
        
        with tab22:
            df_depara_contas = pd.read_excel('dados/depara_contas.xlsx')    # planilha com depara de contas financeiras com os eventos
            data_depara_edited = st.data_editor(df_depara_contas, use_container_width=True, num_rows='dynamic')

            if st.button('Salvar', key='salvar_depara'):
                data_depara_edited.to_excel('dados/depara_contas.xlsx', index=False)
                st.success('Salvo com Sucesso')

                time.sleep(3)
                st.rerun()



if __name__ == "__main__":
    main()