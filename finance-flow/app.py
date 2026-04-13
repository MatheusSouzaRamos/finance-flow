import streamlit as st
import pandas as pd
import plotly.express as px
import databaseAndCrud as dbac

df_mov = pd.DataFrame()
df_cat = pd.DataFrame()
df_pag = pd.DataFrame()
df_mov_filtrado = pd.DataFrame()

def carregarTabelas():
    global df_mov, df_cat, df_pag, df_mov_filtrado
    try:
        df_mov = dbac.selectMovimentos()
        df_mov['data'] = pd.to_datetime(df_mov['data'], format='%d/%m/%Y', dayfirst=True)
        df_mov = df_mov.sort_values('data', ascending=False)
        df_mov['data'] = df_mov['data'].dt.strftime('%d/%m/%Y')
        df_cat = dbac.selectCategorias()
        df_pag = dbac.selectPagamentos()
        df_mov_filtrado = df_mov.copy()
    except Exception as erro:
        st.warning(f'Erro: {erro}')

@st.cache_data
def inicializar():
    dbac.montarBanco()

diasValidos = [str(i) for i in range (1,32)]

def validarData(data):
    try:
        if data in diasValidos:
            hoje = pd.Timestamp.now()
            dataString = str(data).zfill(2) + '/' + hoje.strftime('%m/%Y')
            data = pd.to_datetime(dataString, format="%d/%m/%Y")
            data = data.strftime("%d/%m/%Y")
            return data
        else:
            data = pd.to_datetime(data, format="%d/%m/%Y")
            data = data.strftime("%d/%m/%Y")
            return data
    except ValueError as erro:
        st.title(f'ERRO AO CONverter {erro}')
        raise ValueError('Erro ao converter')

def validarCamposMovimento(descricao, valor, categoria_id, pagamento_id, status, data):
    if descricao.strip() == '':
        return False
    try:
        valor = valor.replace(',','.')
        valor = float(valor)
    except:
        return False
    try:
        categoria_id = int(categoria_id)
    except:
        return False
    try:
        pagamento_id = int(pagamento_id)
    except:
        return False
    if status.strip() == '':
        return False
    try:
        data = validarData(data)
    except:
        return False
    return True

inicializar()
carregarTabelas()
# ==================== SIDEBAR ====================
st.sidebar.subheader('Filtros')
a = pd.Timestamp.today().date()
b = pd.Timestamp.today().date()
primeiroDiaMesAtual = a.replace(day=1)
primeiroDiaMesAtual = primeiroDiaMesAtual.strftime('%d/%m/%Y')
b = b.strftime('%d/%m/%Y')

dataInicialText = st.sidebar.text_input('Data Inicial dd/mm/aaaa', value = primeiroDiaMesAtual)
dataFimText = st.sidebar.text_input('Data Final dd/mm/aaaa', value = b)

#st.sidebar.subheader('#Exportar Excel')

try:
    dataInicial = pd.to_datetime(dataInicialText, format='%d/%m/%Y')
    dataFim = pd.to_datetime(dataFimText, format='%d/%m/%Y')

    if dataInicial > dataFim:
        raise ValueError('DATA INICIAL MAIOR QUE DATA FINAL')
    
    df_mov_filtrado['data'] = pd.to_datetime(df_mov_filtrado['data'], dayfirst=True, format='%d/%m/%Y')
    df_mov_filtrado = df_mov_filtrado[(df_mov_filtrado['data'] >= dataInicial) & (df_mov_filtrado['data'] <= dataFim)]
except Exception as erro:
    st.sidebar.warning(f'Erro: {erro}')

# ==================== MAIN ====================
abaVisaoGeral, abaMovimentos, abaCategorias, abaPagamentos = st.tabs(['Visão Geral','Movimentos', 'Categorias', 'Pagamentos'])

with abaVisaoGeral:
    try:
        
        if df_mov_filtrado.empty:
            raise ValueError('Dados indisponíveis para consulta, confira os filtros.')
        
        st.text(
            f"Dados de: {pd.to_datetime(df_mov_filtrado['data'].min(), format='%d/%m/%Y').strftime('%d/%m/%Y')} "
            f"a {pd.to_datetime(df_mov_filtrado['data'].max(), format='%d/%m/%Y').strftime('%d/%m/%Y')}"
        )
        col1, col2 = st.columns([1,1])
        with col1:
            valorTotal = df_mov_filtrado['valor'].sum()
            st.metric('Gastos Totais', f"R$ {valorTotal:.2f}")
        with col2:
            quantidade = df_mov_filtrado['valor'].count()
            st.metric('Movimentações', quantidade)

        col3, col4 = st.columns([1,1])
        with col3:
            df_plot_cat = df_mov_filtrado.groupby('categoria_id').agg({'valor': sum}).reset_index()
            df_plot_cat = df_plot_cat.merge(df_cat, left_on='categoria_id', right_on='id')
            fig_cat = px.pie(df_plot_cat, values = 'valor', names = 'nome', title = 'Por Categoria', color_discrete_sequence=px.colors.sequential.Rainbow)
            st.plotly_chart(fig_cat)
        with col4:
            df_plot_pag = df_mov_filtrado.groupby('pagamento_id').agg({'valor': sum}).reset_index()
            df_plot_pag = df_plot_pag.merge(df_pag, left_on='pagamento_id', right_on='id')    
            fig_pag = px.pie(df_plot_pag, values='valor', names='nome', title='Por Pagamento', color_discrete_sequence=px.colors.sequential.Magma)
            st.plotly_chart(fig_pag)
    except Exception as erro:
        st.warning(f'Erro ao gerar dados. Confira os campos de filtros. Erro: {erro}')
    
with abaMovimentos:
    with st.form(key='formMovimento', clear_on_submit=True, enter_to_submit=True):
        st.subheader('Inserir Movimento')
        col1, col2, col3, col4, col5, col6 = st.columns([2,2,2,2,1,2])

        with col1:
            descricao = st.text_input('Descrição', key='fieldDescricaoAddMovimento')
        with col2:
            valor = st.text_input('Valor', key='fieldValorAddMovimento')
        with col3:
            categoria_id = st.selectbox(
                'Categoria',
                df_cat['id'],
                format_func= lambda x: df_cat.loc[df_cat['id'] == x, 'nome'].values[0]
            )
        with col4:
            pagamento_id = st.selectbox(
                'Pagamento',
                df_pag['id'],
                format_func= lambda x: df_pag.loc[df_pag['id'] == x, 'nome'].values[0]
            )
        with col5:
            status = st.text_input('Status', key='fielStatusAddMovimento')
        with col6:
            data = st.text_input('Data', key='fieldDataAddMovimento')
        
        if st.form_submit_button('Adcionar', key='buttonAddMovimento'):
            if validarCamposMovimento(descricao, valor, categoria_id, pagamento_id, status, data):
                descricao = descricao.strip()
                valor = float(valor.replace(',','.'))
                categoria_id = int(categoria_id)
                pagamento_id = int(pagamento_id)
                status = status.strip()
                data = validarData(data)
                dbac.insertMovimentos(descricao, valor, categoria_id, pagamento_id, status, data)
                st.rerun()
            else:
                st.warning('Movimentação inválida')

    st.divider()

    for index, row in df_mov.head(150).iterrows():
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1,1,1,1,1,2,1,1])

        col1.write(row['descricao'])
        col2.write(row['valor'])
        with col3:
            result = df_cat.loc[df_cat['id'] == row['categoria_id'], 'nome']
            #st.write(df_cat.loc[df_cat['id'] == row['categoria_id'], 'nome'].values[0])
            if not result.empty:
                st.write(result.values[0])
            else:
                st.write("Não encontrado")
        with col4:
            result = df_pag.loc[df_pag['id'] == row['pagamento_id'], 'nome']
            #st.write(
                #df_pag.loc[df_pag['id'] == row['pagamento_id'], 'nome'].values[0]
                #)
            if not result.empty:
                st.write(result.values[0])
            else:
                st.write("Não encontrado")

        col5.write(row['status'])
        col6.write(row['data'])

        with col7:
            if st.button('✏️', key = f"editarMovimento{row['id']}"):
                st.session_state['editarMovimento_id'] = row['id']
                st.session_state['editarMovimento_descricao'] = row['descricao']
                st.session_state['editarMovimento_valor'] = row['valor']
                st.session_state['editarMovimento_categoria'] = row['categoria_id']
                st.session_state['editarMovimento_pagamento'] = row['pagamento_id']
                st.session_state['editarMovimento_status'] = row['status']
                st.session_state['editarMovimento_data'] = row['data']
        with col8:
            if st.button('🗑️', key= f"deletarMovimento{row['id']}"):
                st.session_state['deletarMovimento_descricao'] = row['descricao']
                st.session_state['deletarMovimento_id'] = row['id']
                st.session_state['deletarMovimento_valor'] = row['valor']
                st.session_state['deletarMovimento_categoria'] = row['categoria_id']
                st.session_state['deletarMovimento_pagamento'] = row['pagamento_id']
                st.session_state['deletarMovimento_status'] = row['status']
                st.session_state['deletarMovimento_data'] = row['data']
        
        if st.session_state.get('editarMovimento_id') == row['id']:
            st.subheader('Editar Movimento')
            id_mov = st.session_state.get('editarMovimento_id')
            descricaoEditar = st.session_state.get('editarMovimento_descricao', '')
            valorEditar = st.session_state.get('editarMovimento_valor')
            categoriaEditar = st.session_state.get('editarMovimento_categoria')
            pagamentoEditar = st.session_state.get('editarMovimento_pagamento')
            statusEditar = st.session_state.get('editarMovimento_status')
            dataEditar = st.session_state.get('editarMovimento_data')

            with st.form(key = f"formEditarMovimento{id_mov}", enter_to_submit=True):
            
                col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
                
                with col1:
                    descricaoEditar = st.text_input('Descrição', key=f"editarMovimento_descricao{id_mov}", value=descricaoEditar)

                with col2:
                    valorEditar = st.text_input('Valor', key=f"editarMovimento_valor{id_mov}", value=valorEditar)

                with col3:
                    catgoriaEditar = st.selectbox(
                        'Categoria',
                        df_cat['id'],
                        format_func = lambda x: df_cat.loc[df_cat['id'] == x, 'nome'].values[0]
                    )

                with col4:
                    pagamentoEditar = st.selectbox(
                        'Pagamento',
                        df_pag['id'],
                        format_func = lambda x: df_pag.loc[df_pag['id'] == x, 'nome'].values[0]
                    )

                with col5:
                    statusEditar = st.text_input('Status', key=f"editarMovimento_status{id_mov}", value=statusEditar)

                with col6:
                    dataEditar = st.text_input('Data', key=f"editarMovimento_data{id_mov}", value=dataEditar)

                col1, col2 = st.columns([1,1])

                with col1:
                    if st.form_submit_button('Confirmar', key = f"buttonEditarMovimento{id_mov}"):
                        if validarCamposMovimento(descricaoEditar, valorEditar, categoriaEditar, pagamentoEditar, statusEditar, dataEditar):
                            descricaoEditar = descricaoEditar.strip()
                            valorEditar = float(valorEditar.replace(',','.'))
                            categoriaEditar = int(categoriaEditar)
                            pagamentoEditar = int(pagamentoEditar)
                            statusEditar = statusEditar.strip()
                            dataEditar = dataEditar.strip()
                            dbac.updateMovimentos(id_mov, descricaoEditar, valorEditar, categoriaEditar, pagamentoEditar, statusEditar, dataEditar)
                            del st.session_state['editarMovimento_id']
                            st.rerun()
                        else:
                            st.warning('Movimento inválido')
                with col2:
                    if st.form_submit_button('Cancelar', key=f"buttonCancelarEditarMovimento{id_mov}"):
                        del st.session_state['editarMovimento_id']
                        st.rerun()

        if st.session_state.get('deletarMovimento_id') == row['id']:
            id_mov = st.session_state.get('deletarMovimento_id')
            descricaoDeletar = st.session_state.get('deletarMovimento_descricao', '')
            valorDeletar = st.session_state.get('deletarMovimento_valor')
            categoriaDeletar = st.session_state.get('deletarMovimento_categoria')
            pagamentoDeletar = st.session_state.get('deletarMovimento_pagamento')
            statusDeletar = st.session_state.get('deletarMovimento_status')
            dataDeletar = st.session_state.get('deletarMovimento_data')
            
            st.subheader('Deletar Movimento')
            st.text(f'Tem certeza que deseja apagar? ID {id_mov} -> {descricaoDeletar} R$ {valorDeletar} {df_cat.loc[df_cat['id'] == categoriaDeletar, 'nome'].values[0]} {df_pag.loc[df_pag['id'] == pagamentoDeletar, 'nome'].values[0]} {statusDeletar} {dataDeletar}')
            col1, col2 = st.columns([1,1])
            with col1:
                if st.button('Confirmar', key=f'buttonDeletarMovimento{id_mov}'):
                    dbac.deleteMovimentos(id_mov)
                    del st.session_state['deletarMovimento_id']
                    st.rerun()
            with col2:
                if st.button('Cancelar', key = f'buttonCancelarDeletarMovimento{id_mov}'):
                    del st.session_state['deletarMovimento_id']
                    st.rerun()

with abaCategorias:
    with st.form(key = 'formCategoria', clear_on_submit=True, enter_to_submit=True):
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            st.write('')
            st.subheader('Inserir Categoria')
        with col2:
            novaCategoria = st.text_input('Nome', key='fieldAddCategoria')
        with col3:
            st.write('')
            st.write('')
            if st.form_submit_button('Adcionar', key='buttonAddCategoria'):
                if novaCategoria.strip() != '':
                    novaCategoria = novaCategoria.strip()
                    dbac.insertCategorias(novaCategoria)
                    st.rerun()
                else:
                    st.warning('Nome Inválido')

    st.divider()

    for index, row in df_cat.iterrows():
        col1, col2, col3, col4 = st.columns([1,1,1,1])

        col1.write(row['id'])
        col2.write(row['nome'])

        with col3:
            if st.button('✏️', key=f"editarCategoria{row['id']}"):
                st.session_state['editarCategoria_id'] = row['id']
                st.session_state['editarCategoria_nome'] = row['nome']
        with col4:
            if st.button('🗑️', key=f"deletarCategoria{row['id']}"):
                st.session_state['deletarCategoria_id'] = row['id']
                st.session_state['deletarCategoria_nome'] = row['nome']

        if st.session_state.get('editarCategoria_id') == row['id']:
            st.subheader('Editar Categoria')    
            with st.form(key=f"formEditarCategoria{st.session_state['editarCategoria_id']}", enter_to_submit=True):
                nomeEditar = st.session_state.get('editarCategoria_nome', '')
                nomeEditar = st.text_input(
                    'Editar Categoria',
                    key= f"nomeEditarCategoria{st.session_state['editarCategoria_id']}",
                    value= nomeEditar
                )

                col1, col2 = st.columns([1,1])

                with col1:
                    if st.form_submit_button('Confirmar', key = f"buttonEditarCategoria{st.session_state['editarCategoria_id']}"):
                        if nomeEditar.strip() != '':
                            dbac.updateCategorias(st.session_state['editarCategoria_id'], nomeEditar)
                            del st.session_state['editarCategoria_id']
                            st.rerun()
                        else:
                            st.warning('Nome inválido')
                with col2:
                    if st.form_submit_button('Cancelar', key = f"buttonCancelarEditarCategoria{st.session_state['editarCategoria_id']}"):
                        del st.session_state['editarCategoria_id']
                        st.rerun()

        if st.session_state.get('deletarCategoria_id') == row['id']:
            st.subheader('Deletar Categoria')
            st.text(f"Tem certeza que deseja apagar? ID {st.session_state['deletarCategoria_id']} -> {st.session_state['deletarCategoria_nome']}")
            with st.form(key=f"formDeletarCategoria{st.session_state['deletarCategoria_id']}"):
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.form_submit_button('Confirmar', key=f"buttonConfirmarDeletarCategoria{st.session_state['deletarCategoria_id']}"):
                        dbac.deleteCategorias(st.session_state['deletarCategoria_id'])
                        del st.session_state['deletarCategoria_id']
                        st.rerun()
                with col2:
                    if st.form_submit_button('Cancelar', key = f"buttonCancelarDeletarCategoria{st.session_state['deletarCategoria_id']}"):
                        del st.session_state['deletarCategoria_id']
                        st.rerun()

with abaPagamentos:
    with st.form(key = 'formPagamento', clear_on_submit=True, enter_to_submit=True):
        col1, col2, col3 = st.columns([2,1,1])
        with col1:
            st.write('')
            st.subheader('Inserir Pagamento')
        with col2:
            novoPagamento = st.text_input('Nome', key='fieldAddPagamento')
        with col3:
            st.write('')
            st.write('')
            if st.form_submit_button('Adcionar', key='buttonAddPagamento'):
                if novoPagamento.strip() != '':
                    novoPagamento = novoPagamento.strip()
                    dbac.insertPagamentos(novoPagamento)
                    st.rerun()
                else:
                    st.warning('Nome Inválido')

    st.divider()

    for index, row in df_pag.iterrows():
        col1, col2, col3, col4 = st.columns([1,1,1,1])

        col1.write(row['id'])
        col2.write(row['nome'])

        with col3:
            if st.button('✏️', key=f"editarPagamento{row['id']}"):
                st.session_state['editarPagamento_id'] = row['id']
                st.session_state['editarPagamento_nome'] = row['nome']
        with col4:
            if st.button('🗑️', key=f"deletarPagamento{row['id']}"):
                st.session_state['deletarPagamento_id'] = row['id']
                st.session_state['deletarPagamento_nome'] = row['nome']

        if st.session_state.get('editarPagamento_id') == row['id']:
            st.subheader('Editar Pagamento')
            with st.form(key=f"editarPagamento{st.session_state['editarPagamento_id']}", enter_to_submit=True):
                nomeEditar = st.session_state.get('editarPagamento_nome', '')
                nomeEditar = st.text_input(
                    'Editar Pagamento',
                    key= f"nomeEditarPagamento{st.session_state['editarPagamento_id']}",
                    value = nomeEditar
                )

                col1, col2 = st.columns([1,1])

                with col1:
                    if st.form_submit_button('Confirmar', key=f"buttonEditarPagamento{st.session_state.get('editarPagamento_nome', '')}"):
                        if nomeEditar.strip() != '':
                            nomeEditar = nomeEditar.strip()
                            dbac.updatePagamentos(st.session_state['editarPagamento_id'], nomeEditar)
                            del st.session_state['editarPagamento_id']
                            st.rerun()
                        else:
                            st.warning('Nome inválido')
                with col2:
                    if st.form_submit_button('Cancelar', key = f"buttonCancelarEditarPagamento{st.session_state['editarPagamento_id']}"):
                        del st.session_state['editarPagamento_id']
                        st.rerun()
        
        if st.session_state.get('deletarPagamento_id') == row['id']:
            st.subheader('Deletar Pagamento')
            st.text(f"Tem certeza que deseja apagar? ID {st.session_state['deletarPagamento_id']} -> {st.session_state['deletarPagamento_nome']}")
            col1, col2 = st.columns([1,1])
            with col1:
                with col1:
                    if st.button('Confirmar', key=f"buttonConfirmarDeletarCategoria{st.session_state['deletarPagamento_id']}"):
                        dbac.deletePagamentos(st.session_state['deletarPagamento_id'])
                        del st.session_state['deletarPagamento_id']
                        st.rerun()
                with col2:
                    if st.button('Cancelar', key = f"buttonCancelarDeletarCategoria{st.session_state['deletarPagamento_id']}"):
                        del st.session_state['deletarPagamento_id']
                        st.rerun()

