import yaml
from pathlib import Path
import streamlit as st

class Config():

    def __init__(self,path):
        with open(Path(path,'config.yaml'),'r') as cp:
            config = yaml.load(cp, Loader=yaml.FullLoader)
        with open(Path(path,'token.yaml'), 'r') as tp:
            token =  yaml.load(tp, Loader=yaml.FullLoader)

        self.mongoHost = config['mongoHost']
        self.tokenDict = token



class Layout():

    def __init__(self):
        hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
        st.markdown(hide_menu_style, unsafe_allow_html=True)

        hide_st_style = """
        <style>
        MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .css-k1ih3n {
            padding: 0rem 5rem 10rem;
        }
        </style>
        """
        st.markdown(hide_st_style, unsafe_allow_html=True)
