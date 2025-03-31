import streamlit as st

def category_component(category):
    st.markdown(
        f"""
        <div style="background-color: #FBD8FD; border-radius: 10px; padding: 0.5rem; margin-bottom: 0.5rem; text-align: center;">
            <span style="color: #000; font-weight: bold;">{category}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )