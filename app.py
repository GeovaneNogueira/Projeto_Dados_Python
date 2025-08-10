import streamlit as st
import pandas as pd
import plotly.express as px



# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)



# Carregamento dos Dados
df = pd.read_csv("https://raw.githubusercontent.com/GeovaneNogueira/Projeto_Dados_Python/main/Tabela_de_dados_Python.csv")

#Barra lateral(filtros)---

st.sidebar.header("Filtros")

#filtro de ano--
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)


#filtro de senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridade_selecionada = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

#filtro por tipo de contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contrato_selecionado = st.sidebar.multiselect("Tipo de contrato", contratos_disponiveis, default=contratos_disponiveis)

#filtro por tamanho da empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanho_selecionado = st.sidebar.multiselect("tamanho da empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

#filtragem do DataFrame
df_filtrado = df[
   (df['ano'].isin(anos_selecionados)) &
   (df['senioridade'].isin(senioridade_selecionada)) &
   (df['contrato'].isin(contrato_selecionado)) &
   (df['tamanho_empresa'].isin(tamanho_selecionado))
]

#conteudo principal

st.title('🎲 Dashboard de Análise de Salários na Área de Dados')
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise")



st.subheader('Métricas gerais (salário anual em USD)')

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    
    # Garante que não dá erro se não houver cargos
    cargo_mode = df_filtrado['cargo'].mode()
    cargo_mais_frequente = cargo_mode[0] if not cargo_mode.empty else ""
else:
    salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, ""


col1, col2, col3, col4 = st.columns(4)

col1.metric("Salario Médio", f"${salario_medio:,.0f}")
col2.metric("Salario Maximo", f"${salario_maximo:,.0f}")
col3.metric("Total de Registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")

#Análises visuais com o plotly

st.subheader("Gráfico")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby("cargo")["usd"].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x="usd",
            y="cargo",
            orientation="h",
            title="Top 10 Cargos por salário médio",
            labels={'usd': "Média salarial anual(USD)", "cargo": ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")


# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)
     