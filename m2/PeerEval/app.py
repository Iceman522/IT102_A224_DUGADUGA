import streamlit as st
from controllers import AppController

st.set_page_config(
    page_title="PeerEval - Group Health & Evaluation",
    layout="wide",
    page_icon="📊"
)

if __name__ == "__main__":
    controller = AppController()
    controller.run()