import streamlit as st
import pandas as pd

# ==============================
# Dados base dos produtos
# ==============================
produtos = {
    "Inc 6mm eng": 128.96,
    "Inc 8mm eng": 143.43,
    "Inc 10mm eng": 225.96,
    "Fume 6mm eng": 156.86,
    "Fume 8mm eng": 182.69,
    "Fume 10mm eng": 318.87,
    "Verde 6mm eng": 156.86,
    "Verde 8mm eng": 182.69,
    "Verde 10mm eng": 318.87,
    "Bronze 10mm eng": 310.00,
    "Box inc 8mm": 134.32,
    "Espelho 4mm lap.": 160.99,
    "Laminado inc 8mm 4+4": 248.83,
    "Laminado 4+4 silver": 348.92,
    "Refletivo cinza 10mm": 392.46
}

# ==============================
# Interface Streamlit
# ==============================
st.set_page_config(page_title="Orçamento Cristal Valle", layout="centered")

st.title("💎 Orçamento de Vidros - Cristal Valle")
st.markdown("Calcule automaticamente o valor conforme as medidas e produtos escolhidos.")

# ==============================
# Entrada de dados do usuário
# ==============================
with st.form("form_orcamento"):
    col1, col2 = st.columns(2)
    produto = col1.selectbox("Produto:", list(produtos.keys()))
    preco_m2 = produtos[produto]
    col1.metric("Preço por m²", f"R$ {preco_m2:,.2f}")

    largura = col1.number_input("Largura (m)", min_value=0.0, step=0.01)
    altura = col2.number_input("Altura (m)", min_value=0.0, step=0.01)
    quantidade = col2.number_input("Quantidade", min_value=1, step=1, value=1)
    desconto = st.slider("Desconto (%)", 0, 30, 10)

    calcular = st.form_submit_button("Adicionar ao Orçamento")

# ==============================
# Inicializa lista de orçamento
# ==============================
if "orcamento" not in st.session_state:
    st.session_state.orcamento = []

# ==============================
# Cálculo e adição de itens
# ==============================
if calcular:
    area = largura * altura
    valor_total = area * preco_m2 * quantidade
    valor_desconto = valor_total * (1 - desconto / 100)

    st.session_state.orcamento.append({
        "Produto": produto,
        "Preço m² (R$)": preco_m2,
        "Largura (m)": largura,
        "Altura (m)": altura,
        "Área (m²)": area,
        "Qtd": quantidade,
        "Valor Total (R$)": valor_total,
        f"Valor c/ {desconto}% Desc (R$)": valor_desconto
    })

# ==============================
# Exibir tabela
# ==============================
if st.session_state.orcamento:
    df = pd.DataFrame(st.session_state.orcamento)
    st.markdown("### 🧾 Itens do Orçamento")
    st.dataframe(df, use_container_width=True)

    total_sem_desc = df["Valor Total (R$)"].sum()
    col_desc = [c for c in df.columns if "Desc" in c][0]
    total_com_desc = df[col_desc].sum()

    st.markdown("---")
    st.subheader("Totais:")
    st.metric("Total sem desconto", f"R$ {total_sem_desc:,.2f}")
    st.metric("Total com desconto", f"R$ {total_com_desc:,.2f}")

    # Exportar para Excel
    if st.button("💾 Exportar para Excel"):
        df.to_excel("Orcamento_CristalValle.xlsx", index=False)
        st.success("Arquivo 'Orcamento_CristalValle.xlsx' gerado com sucesso!")

