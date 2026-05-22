import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS CUSTOMIZADOS (CSS)
# ==============================================================================
st.set_page_config(
    page_title="Painel Integrado de Gestão Hospitalar - HM Brasília",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injeção de CSS para diminuir as fontes das tabelas e títulos específicos
st.html(
    """
    <style>
    /* Diminui o tamanho do texto dentro das tabelas do Streamlit */
    [data-testid="stDataFrame"] table, 
    [data-testid="stDataFrame"] div, 
    [data-testid="stDataFrame"] data-grid {
        font-size: 12px !important;
    }
    /* Estilização compacta para títulos secundários */
    .titulo-compacto {
        font-size: 18px !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    """
)

# ==============================================================================
# 2. CONEXÃO COM O GOOGLE SHEETS
# ==============================================================================
BASE_URL = "https://docs.google.com/spreadsheets/d/1ctBO0MjsMmueXe5kMzRtnQ47vFSPI4ebTi_xVVQTG3o/export?format=csv"

GID_ADMISSAO = "0"          
GID_ATENDIMENTO = "967937234"   
GID_ALTA = "1201607203"          

LINK_ADMISSAO = f"{BASE_URL}&gid={GID_ADMISSAO}"
LINK_ATENDIMENTO = f"{BASE_URL}&gid={GID_ATENDIMENTO}"
LINK_ALTA = f"{BASE_URL}&gid={LINK_ALTA}"

@st.cache_data(ttl=10)
def carregar_dados(link_aba):
    try:
        dados = pd.read_csv(link_aba)
        dados.columns = dados.columns.str.strip()
        return dados
    except Exception as e:
        return pd.DataFrame()

df_admissao = carregar_dados(LINK_ADMISSAO)
df_base_atendimento = carregar_dados(LINK_ATENDIMENTO)
df_alta = carregar_dados(LINK_ALTA)

# ==============================================================================
# 3. PROCESSAMENTO LÓGICO DOS DADOS
# ==============================================================================
if not df_base_atendimento.empty and 'Tipo de Atendimento' in df_base_atendimento.columns:
    df_id = df_base_atendimento[df_base_atendimento['Tipo de Atendimento'].str.startswith('ID', na=False)]
    df_ad = df_base_atendimento[df_base_atendimento['Tipo de Atendimento'].str.startswith('AD', na=False)]
else:
    df_id = df_base_atendimento.copy()
    df_ad = pd.DataFrame()

total_id = len(df_id)
total_ad = len(df_ad)
total_geral = len(df_base_atendimento)

# ==============================================================================
# 4. CABEÇALHO PRINCIPAL CENTRALIZADO (image_4f0576.png)
# ==============================================================================
st.markdown("<h1 style='text-align: center;'>🏥 Painel Integrado de Gestão Hospitalar</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>📍 Filial Atual: <b>HM - Brasília</b></h3>", unsafe_allow_html=True)
st.markdown("---")

# ==============================================================================
# 5. MENU DE ABAS INTERNO
# ==============================================================================
aba_atendimento, aba_admissoes, aba_altas, aba_resumo = st.tabs([
    "🟢 Em Atendimento", "🔵 Admissões", "🔴 Altas", "📊 Resumo por Categoria"
])

# --- ABA 1: EM ATENDIMENTO ---
with aba_atendimento:
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown("<h5 style='text-align: center;'>Total Todas</h5>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>{total_geral}</h2>", unsafe_allow_html=True)
    with col_m2:
        st.markdown("<h5 style='text-align: center;'>Internação (ID)</h5>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>{total_id}</h2>", unsafe_allow_html=True)
    with col_m3:
        st.markdown("<h5 style='text-align: center;'>Atendimento (AD)</h5>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>{total_ad}</h2>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>Análise por Operadora</h3>", unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        if not df_id.empty and 'Operadora' in df_id.columns:
            contagem_id = df_id['Operadora'].value_counts().reset_index()
            contagem_id.columns = ['Operadora', 'Quantidade']
            
            # Título centralizado direto na configuração do gráfico Plotly
            fig_id = px.bar(contagem_id, x='Operadora', y='Quantidade', text='Quantidade',
                            title="Total ID por Operadora", color_discrete_sequence=['#0055ff'])
            fig_id.update_traces(textposition='outside')
            fig_id.update_layout(
                title_x=0.5, # Centraliza o título do gráfico
                xaxis_tickangle=-90, 
                margin=dict(l=20, r=20, t=40, b=20), 
                height=400
            )
            st.plotly_chart(fig_id, use_container_width=True)
        else:
            st.info("Nenhum paciente do tipo 'ID' encontrado.")
            
    with col_g2:
        if not df_ad.empty and 'Operadora' in df_ad.columns:
            contagem_ad = df_ad['Operadora'].value_counts().reset_index()
            contagem_ad.columns = ['Operadora', 'Quantidade']
            
            # Título centralizado direto na configuração do gráfico Plotly
            fig_ad = px.bar(contagem_ad, x='Operadora', y='Quantidade', text='Quantidade',
                            title="Total AD por Operadora", color_discrete_sequence=['#00cc99'])
            fig_ad.update_traces(textposition='outside')
            fig_ad.update_layout(
                title_x=0.5, # Centraliza o título do gráfico
                xaxis_tickangle=-90, 
                margin=dict(l=20, r=20, t=40, b=20), 
                height=400
            )
            st.plotly_chart(fig_ad, use_container_width=True)
        else:
            st.info("Nenhum paciente do tipo 'AD' encontrado.")

    # --- SEÇÃO DE TABELAS DESTRINCHADAS COMPACTAS (image_4f0919.jpg) ---
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>📋 Detalhe de Pacientes Ativos por Categoria</h3>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns(2)
    colunas_exibicao = ['Paciente', 'Operadora', 'Tipo de Atendimento']
    
    with col_t1:
        st.markdown("<p class='titulo-compacto'>🔵 Internação Domiciliar (ID)</p>", unsafe_allow_html=True)
        if not df_id.empty:
            colunas_validas_id = [col for col in colunas_exibicao if col in df_id.columns]
            df_id_exibir = df_id[colunas_validas_id] if colunas_validas_id else df_id
            st.dataframe(df_id_exibir, use_container_width=True, hide_index=True)
        else:
            st.info("Não há pacientes ID ativos.")
            
    with col_t2:
        st.markdown("<p class='titulo-compacto'>🟢 Atendimento Domiciliar (AD)</p>", unsafe_allow_html=True)
        if not df_ad.empty:
            colunas_validas_add = [col for col in colunas_exibicao if col in df_ad.columns]
            df_ad_exibir = df_ad[colunas_validas_add] if colunas_validas_add else df_ad
            st.dataframe(df_ad_exibir, use_container_width=True, hide_index=True)
        else:
            st.info("Não há pacientes AD ativos.")

# --- ABA 2: ADMISSÕES ---
with aba_admissoes:
    st.markdown("<h3 style='text-align: center;'>🔵 Registro Geral de Admissões</h3>", unsafe_allow_html=True)
    if not df_admissao.empty and len(df_admissao) > 0:
        st.dataframe(df_admissao, use_container_width=True)
    else:
        st.info("Não foram registrados dados de admissão para a filial e período informados.")

# --- ABA 3: ALTAS ---
with aba_altas:
    st.markdown("<h3 style='text-align: center;'>🔴 Registro Geral de Altas</h3>", unsafe_allow_html=True)
    if not df_alta.empty and len(df_alta) > 0:
        st.dataframe(df_alta, use_container_width=True)
    else:
        st.info("Não foram registrados dados de alta para a filial e período informados.")

# --- ABA 4: RESUMO POR CATEGORIA ---
with aba_resumo:
    st.markdown("<h2 style='text-align: center;'>📋 Resumo de Pacientes Ativos por Operadora</h2>", unsafe_allow_html=True)
    
    col_r1, col_r2, col_r3 = st.columns(3)
    col_r1.metric("Soma Total ID", total_id)
    col_r2.metric("Soma Total AD", total_ad)
    col_r3.metric("Soma Total Pacientes", total_geral)
    
    st.markdown("---")
    
    if not df_base_atendimento.empty and 'Operadora' in df_base_atendimento.columns:
        resumo_ad = df_ad['Operadora'].value_counts().reset_index() if not df_ad.empty else pd.DataFrame(columns=['Operadora', 'count'])
        resumo_ad.columns = ['Operadora', 'Qtd Pacientes AD']
        
        resumo_id = df_id['Operadora'].value_counts().reset_index() if not df_id.empty else pd.DataFrame(columns=['Operadora', 'count'])
        resumo_id.columns = ['Operadora', 'Qtd Pacientes ID']
        
        todas_operadoras = pd.DataFrame(df_base_atendimento['Operadora'].unique(), columns=['Operadora'])
        
        tabela_resumo = todas_operadoras.merge(resumo_ad, on='Operadora', how='left').merge(resumo_id, on='Operadora', how='left')
        
        tabela_resumo['Qtd Pacientes AD'] = tabela_resumo['Qtd Pacientes AD'].fillna(0).astype(int)
        tabela_resumo['Qtd Pacientes ID'] = tabela_resumo['Qtd Pacientes ID'].fillna(0).astype(int)
        
        tabela_resumo['Total Pacientes'] = tabela_resumo['Qtd Pacientes AD'] + tabela_resumo['Qtd Pacientes ID']
        tabela_resumo = tabela_resumo.sort_values(by='Total Pacientes', ascending=False).reset_index(drop=True)
        
        linha_total = pd.DataFrame([{
            'Operadora': 'TOTAL GERAL',
            'Qtd Pacientes AD': tabela_resumo['Qtd Pacientes AD'].sum(),
            'Qtd Pacientes ID': tabela_resumo['Qtd Pacientes ID'].sum(),
            'Total Pacientes': tabela_resumo['Total Pacientes'].sum()
        }])
        
        tabela_final = pd.concat([tabela_resumo, table_total if 'table_total' in locals() else linha_total], ignore_index=True)
        st.dataframe(tabela_final, use_container_width=True)
    else:
        st.info("Sem dados de atendimento para consolidar o resumo de operadoras.")
