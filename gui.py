import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from startLLM import main as startLLM

# Initialization
if "input" not in st.session_state:
    st.session_state.input = ""
    st.session_state.running = False

st.set_page_config(page_title="CASALIOY")

# Sidebar contents
with st.sidebar:
    st.title('CASALIOY')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [su77ungr/CASALIOY](https://github.com/alxspiker/CASALIOY) LLM Toolkit
    
    💡 Note: No API key required!

    GUI does not support live response yet, so you have to wait for the tokens to process.
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [su77ungr/CASALIOY](https://github.com/alxspiker/CASALIOY)')

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I can help you answer questions about the documents you have ingested into the vector store."]

if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi, what can you help me with!']

input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

def generate_response(prompt):
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
    if st.session_state.running==False and prompt.strip() != "":
        st.session_state.running = True
        st.session_state.past.append(prompt)
        message(prompt, is_user=True)
        message("Loading response. Please wait...", key="rmessage")
        response = startLLM(prompt, True)
        st.session_state.generated.append(response)
        message(response)
        st.session_state.running = False
    st.text_input("You: ", "", key="input", disabled=st.session_state.running)

with st.container():
    with st.form("my_form", clear_on_submit=True):
        st.form_submit_button('SUBMIT', on_click=generate_response(st.session_state.input), disabled=st.session_state.running)