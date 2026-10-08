import streamlit as st
import pandas as pd

# 1. Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_parquet('data_full.parquet')

    #remove linhas onde não temos marca, modelo ou as urlas das imagens
    df = df.dropna(subset=['brand', 'model', 'image_urls'])

    return df


df = load_data()
# 2. Configurar a Pagina
st.set_page_config(page_title="Catálogo de Carros", layout="wide")
st.title("🚗 Catálogo de Carros")

# --- BARRA LATERAL: FILTROS ---
st. sidebar.header("Filtros")
# --- Escolha a Marca
lista_marcas = sorted(df['brand'].unique())
marca_selecionada = st.sidebar.selectbox("Escolhe a Marca", lista_marcas)


# --- Escolha o Carro
df_marca = df[df['brand'] == marca_selecionada]
lista_modelos = sorted(df_marca['model'].unique())
modelo_selecionado = st.sidebar.selectbox("Escolha o Modelo", lista_modelos)


# Pega a linha do carro escolhido
carro_info = df_marca[df_marca['model'] == modelo_selecionado].iloc[0]

# --- TRATAMENTO DAS IMAGENS ---
# Transforma a string "url1, url2, url3" em uma lista ["url1", "url2", "url3"]
urls_string = carro_info['image_urls']
lista_imagens = [url.strip() for url in urls_string.split(',') if url.strip()]

num_imagens = len(lista_imagens)

#
if num_imagens > 0:
    # Reseta o índice da imagem se o usuário trocar de carro
    chave_carro = f"{marca_selecionada}_{modelo_selecionado}"
    
    if 'carro_atual' not in st.session_state or st.session_state.carro_atual != chave_carro:
        st.session_state.foto_index = 0
        st.session_state.carro_atual = chave_carro
    
    # Controles de navegação
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col1:
        if st.button("⬅️ Anterior", use_container_width=True):
            if st.session_state.foto_index > 0:
                st.session_state.foto_index -= 1
            else:
                st.session_state.foto_index = num_imagens - 1 # Loop para o final
                
    with col3:
        if st.button("Próxima ➡️", use_container_width=True):
            if st.session_state.foto_index < num_imagens - 1:
                st.session_state.foto_index += 1
            else:
                st.session_state.foto_index = 0 # Loop para o início


    # Exibe a imagem principal
    url_atual = lista_imagens[st.session_state.foto_index]
    
    col_img1, col_img2, col_img3 = st.columns([1, 6, 1])
    with col_img2:
        st.image(
            url_atual, 
            caption=f"{modelo_selecionado} - Foto {st.session_state.foto_index + 1} de {num_imagens}",
            use_container_width=True
        )
    # --- GALERIA DE MINIATURAS ---
    st.write("###📸 Galeria de Fotos")
    st.write("Clique em uma miniatura para visualizá-la:")

    # Define quantas miniaturas mostrar por linha (ex: 6)
    cols_por_linha =6

    # Cria as colunas necessárias para as miniaturas
    # Se tivermos 10 imagens e 6 colunas, precisamos de 2 linhas
    for i in range(0, num_imagens, cols_por_linha):
        cols = st.columns(cols_por_linha)

        # Preenche as colunas dessa linha
        for j in range(cols_por_linha):
            idx = i + j
            if idx < num_imagens:
                with cols[j]:
                    # Exibe a miniatura como um botão clicável
                    # O 'key' é importante para o streamlit saber qual botão é qual
                    if st.button(f"Foto {idx + 1}", key=f"thumb_{idx}", use_container_width=True):
                        st.session_state.foto_index = idx
                        st.rerun() # Força o recarregamento para mostrar a foto grande

                    # Exiba a imagem pequena abaixo do botão (opcional, mas fica bonito)
                    st.image(lista_imagens[idx], width='stretch')

else:
    st.warning("Nenhuma imagem disponível para este modelo.")

st.divider()




# --- INFORMAÇÕES DO CARRO (MARKDOWN) ---



### 📝 Descrição
{carro_info.get('description', 'Sem descrição disponível.')}


