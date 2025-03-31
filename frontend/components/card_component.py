import streamlit as st

def card_component(title, tags, date):
    """
    Componente de tarjeta que utiliza elementos nativos de Streamlit.
    """
    st.markdown(
        f"""
        <div class="card">
            <h4>{title}</h4>
            <p class="card-date">{date}</p>
            <div class="card-tags">
                {" ".join([f'<span class="tag">{tag}</span>' for tag in tags])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )