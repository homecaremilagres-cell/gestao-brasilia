# --- SEÇÃO DE TABELAS DESTRINCHADAS EMPILHADAS (Fim do Scroll Lateral) ---
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-top: 15px; margin-bottom: 25px;'>📋 Detalhe de Pacientes Ativos por Categoria</h3>", unsafe_allow_html=True)
    
    colunas_exibicao = ['Paciente', 'Operadora', 'Tipo de Atendimento']
    
    # --- 1. TABELA DE INTERNAÇÃO DOMICILIAR (ID) - NO TOPO ---
    st.markdown("<p class='titulo-compacto' style='text-align: left; margin-left: 5px;'>🔵 Internação Domiciliar (ID)</p>", unsafe_allow_html=True)
    st.html("<div style='height: 10px;'></div>") # Espaço entre o título e a tabela
    
    if not df_id.empty:
        colunas_validas_id = [col for col in colunas_exibicao if col in df_id.columns]
        df_id_exibir = df_id[colunas_validas_id] if colunas_validas_id else df_id
        
        st.dataframe(
            df_id_exibir.reset_index(drop=True), 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.info("Não há pacientes ID ativos.")
        
    # Espaço generoso de respiro entre a primeira e a segunda tabela
    st.html("<div style='height: 40px;'></div>")
    
    # --- 2. TABELA DE ATENDIMENTO DOMICILIAR (AD) - ABAIXO ---
    st.markdown("<p class='titulo-compacto' style='text-align: left; margin-left: 5px;'>🟢 Atendimento Domiciliar (AD)</p>", unsafe_allow_html=True)
    st.html("<div style='height: 10px;'></div>") # Espaço entre o título e a tabela
    
    if not df_ad.empty:
        colunas_validas_add = [col for col in colunas_exibicao if col in df_ad.columns]
        df_ad_exibir = df_ad[colunas_validas_add] if colunas_validas_add else df_ad
        
        st.dataframe(
            df_ad_exibir.reset_index(drop=True), 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.info("Não há pacientes AD ativos.")
