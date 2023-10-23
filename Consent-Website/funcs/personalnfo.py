import streamlit as st
from funcs.mongo import Person, MembershipRole, Project, Authorship, Publication

def info():
    exclude = ['flag_owner','ARG_2000028','id','familyName','label']
    links = ['bearerof','relatedBy']
    mapper = {'membership_role': MembershipRole,
              'project':Project,
              'authorship':Authorship,
              'publication':Publication}
    firstName = st.session_state.fname.strip()
    lastName = st.session_state.lname.strip()
    db = Person.objects(__raw__={'$and':[
        {"firstName":{"$in":[firstName]}},
        {"lastName":{"$in":[lastName]}}]})
    object = db[0]
    _,lcol,mcol,rcol,_ = st.columns([3,3,3,3,3])
    with lcol:
        st.subheader('Persönliche Informationen')
        st.markdown("""---""") 
    with mcol:
        st.subheader('Mitgliedschaften')
        st.markdown("""---""") 
    with rcol:
        st.subheader('Autorenschaften')
        st.markdown("""---""") 
    for x in object:
        if x  not in exclude:
            if x not in links:
                with lcol:
                    st.write(x,': ',object[x])
            elif x == 'bearerof':
                for memRoleRef in object[x]:
                    with mcol:
                        memRoleDB = mapper[memRoleRef.collection].objects(id = memRoleRef.id)[0]
                        projectRef = memRoleDB.roleContributesTo
                        projectDB = mapper[projectRef.collection].objects(id = projectRef.id)[0]
                        try:
                            memRoleLabel = memRoleDB.label
                        except:
                            memRoleLabel = 'member'
                        st.write(memRoleLabel,': ',projectDB.name)
            elif x == 'relatedBy':
                for authorshipRef in object[x]:
                    with rcol:
                        authorshipDB = mapper[authorshipRef.collection].objects(id = authorshipRef.id)[0]
                        relatesArray = authorshipDB.relates
                        publicationRef = [x for x in relatesArray if x.collection == 'publication'][0]
                        publicationDB = mapper[publicationRef.collection].objects(id = publicationRef.id)[0]
                        st.write(publicationDB.name+', ',publicationDB.year)

