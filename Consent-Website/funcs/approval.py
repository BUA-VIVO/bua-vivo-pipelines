import streamlit as st
import base64
from funcs.mongo import Person

def approve():
    firstName = st.session_state.fname.strip()
    lastName = st.session_state.lname.strip()
    db = Person.objects(__raw__={'$and':[
        {"firstName":{"$in":[firstName]}},
        {"lastName":{"$in":[lastName]}}]})
    dbEntry = db[0]
    _,lcol,rcol,_ = st.columns([1,9,6,1])
    with lcol:
        with open('data/Einwilligungserklärung – Forschungsinformationsplattform.pdf',"rb") as f:    
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="1200" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    with rcol:
        st.markdown('## Zustimmung zur Datenschutzvereinbarung ')
        st.write("Mit einem Klick auf 'Zustimmen' werden Ihre Einwahldaten (Vorname, Name, Token) sowie Ihre Zustimmung zur Datenschutzvereinbarung gespeichert und auf Servern der Berlin University Alliance hinterlegt.")
        st.write("Mit der Zustimmung werden Ihre Daten im Vivo der BUA freigegeben.")
        try:
            approv = dbEntry.flag_approval
        except:
            approv = 'false'
            st.session_state.approvalState = 'aktueller Status: Einverständnis zur Dateverabteitung nicht erteilt' 
        else:
            if approv == 'true':
                st.session_state.approvalState = 'aktueller Status: Einverständnis zur Dateverabteitung erteilt' 
            else:
                st.session_state.approvalState = 'aktueller Status: Einverständnis zur Dateverabteitung nicht erteilt' 

        
        if approv == 'false':
            if st.button('Zustimmen'):

                dbEntry.flag_approval = 'true'
                dbEntry.save()
                st.write('...')
                st.write('Zustimmung hinterlegt')

                st.experimental_rerun()
        else:
            if st.button('Zustimmung widerrufen'):
                dbEntry.flag_approval = 'false'
                dbEntry.save()
                st.write('...')
                st.write('Zustimmung widerufen')
                st.experimental_rerun()
        st.write(st.session_state.approvalState)
