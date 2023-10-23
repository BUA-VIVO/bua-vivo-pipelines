import streamlit as st
import streamlit_nested_layout
from streamlit_toggle import st_toggle_switch
from mongoengine import *
from funcs.settings import Config, Layout
from funcs.login import login
from funcs.approval import approve
from funcs.personalnfo import info
from funcs.impressum import impressum

# Layout
st.set_page_config(layout='wide')

# Config
config = Config('static')
layout = Layout()

# mongo Connect
disconnect()
connect(host=config.mongoHost)

# Token
tokenDict = config.tokenDict

# SessionState
stateList = ['fname','lname','affil','token','approvalState']
if 'login' not in st.session_state:
    st.session_state['login'] = False
for state in stateList: 
    if state not in st.session_state:
        st.session_state[state] = ''


# App
## Header
_,rtop = st.columns([19,1])
mainCont = st.container()
footCont = st.container()
imp = st_toggle_switch(
        label="Impressum",
        key="impSwitch",
        default_value=False,
        label_after=False)

with mainCont:
    ## Impressum
    if imp:
        impressum()
    ## MainPage
    else:
    ### LoginArea
        if st.session_state.login == False:
            login(tokenDict)
    ### Main Area
        else:
            tab1, tab2 = st.tabs(["Datenschutzvereinbarung", "optional: Persönliche Informationen"])
            with tab1:
                approve()
            with tab2:
                info()
    ### LogoutButton
            with rtop:
                if st.button('Logout'):
                    st.session_state['login'] = False
                    for state in stateList: 
                        st.session_state[state] = ''
                    st.experimental_rerun()

# Footer
with footCont:
    st.markdown('<div style="text-align: center;"> Partners: <a href="https://www.hu-berlin.de/en">Humboldt Universität zu Berlin </a> , <a href="https://www.fu-berlin.de/en/index.html.htm">Freie Universität Berlin </a> , <a href="https://www.tu.berlin/en/">Technische Universität Berlin</a> , <a href="https://www.charite.de/en/">Charité Universitätsmedizin Berlin </a></div>',unsafe_allow_html=True)
    st.markdown('<div style="text-align: center;">Das Projekt wird durch das Bundesministerium für Bildung und Forschung (BMBF) und das Land Berlin im Rahmen der <br> Exzellenzinitiative des Bundes und der Länder gefördert. Die aktuelle Phase des Projekts läuft bis zum 31.12.2023.</div>',unsafe_allow_html=True)


    

