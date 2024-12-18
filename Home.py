import streamlit as st
from read_files import gerar_layout_eco
st.set_page_config(page_title="Sync", page_icon=":robot:", layout='wide')


def main():
    st.header('Gerar Layout')

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



if __name__ == "__main__":
    main()