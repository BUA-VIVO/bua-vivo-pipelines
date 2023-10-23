import streamlit as st
from datetime import datetime
from funcs.mongo import Person

def login(tokenDict):
    st.markdown("<h1 style='text-align: center;'><u>VIVO - Einwilligung ins Datenschutzkonzept</u></h1>", unsafe_allow_html=True)
    _,col,_ = st.columns([6,8,6])
    with col:
        with st.form(key='my_form'):
            lcol,rcol = st.columns([1,1])
            with lcol: 
                st.session_state.fname = st.text_input('Vorname')
                st.session_state.lname = st.text_input('Nachname')
            with rcol:
                st.session_state.token = st.text_input('Token')
                st.session_state.affil = st.selectbox('Organisation',['Matters of Activity','Neurocure','Science of Intelligence','Scripts','Temporal Communities'])
            loginButton = st.form_submit_button('Login')
            responseBox = st.container()

    if loginButton:
        firstName = st.session_state.fname.strip()
        lastName = st.session_state.lname.strip()
        db = Person.objects(__raw__={'$and':[
            {"firstName":{"$in":[firstName]}},
            {"lastName":{"$in":[lastName]}}]})
        if len(db) > 0:
            if st.session_state.affil in db[0].flag_owner:
                tokenlist = tokenDict[st.session_state.affil]
                if st.session_state.token in tokenlist:
                    with open('static/user.log', 'a') as f:
                        f.write(f'{datetime.now()} - {lastName}, {firstName} - {st.session_state.token}' )
                    st.session_state['login'] = True
                    st.experimental_rerun()
                else:
                    with responseBox: 
                        with open('static/user.log', 'a') as f:
                            f.write(f'DENIED: invalid Token - {datetime.now()} - {lastName}, {firstName} - {st.session_state.token}' )
                        st.markdown('<p style="color:red">Please enter a valid token</p>',unsafe_allow_html=True)
            else:
                with responseBox: 
                    with open('static/user.log', 'a') as f:
                        f.write(f'DENIED: wrong Organisation - {datetime.now()} - {lastName}, {firstName} - {st.session_state.token}' )
                    st.markdown('<p style="color:red">'+F'{firstName} {lastName} not found in {st.session_state.affil}'+'</p>',unsafe_allow_html=True)
        else:
            with responseBox: 
                with open('static/user.log', 'a') as f:
                    f.write(f'DENIED: wrong Name - {datetime.now()} - {lastName}, {firstName} - {st.session_state.token}' )
                st.markdown('<p style="color:red">'+f'{firstName} {lastName} not found in Database'+'</p>',unsafe_allow_html=True)