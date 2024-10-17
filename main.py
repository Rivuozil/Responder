import streamlit as st
from test import checkOne
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

# Function to get response using llama2 model
def get_response(email_text, email_style, word_count=150):
    llm = CTransformers(model='llama-2-7b-chat.Q4_K_M.gguf',
                        model_type='llama',
                        config={'max_new_tokens': 400,
                                'temperature': 0.01})

    template = ("Write an email body, in response to the email: {}, in a human-like, "
                "comprehensive and {} nature within {} words.").format(
        email_text, email_style, word_count)

    prompt = PromptTemplate(input_variables=["email_style", "email_text", "word_count"],
                            template=template)

    response = llm(prompt.format(email_style=email_style, email_text=email_text, word_count=word_count))
    return response

# Streamlit app
st.set_page_config(page_title="E-Mailer", layout='centered', initial_sidebar_state='collapsed')
st.header('FastMailer ✉️')
st.subheader('Check for spams, generate custom e-mail replies: all in one click!')

input_text = st.text_input("Enter the e-mail text")

col1, col2 = st.columns([5, 5])

with col1:
    word_count = st.text_input("Enter word count of e-mail")
with col2:
    email_style = st.selectbox("Writing the reply as",
                               ('Affirmative', 'Negative', 'Descriptive', 'Greeting'),
                               index=0)

if st.button("Check"):
    st.write("This is a {} email".format(checkOne(input_text)))

if st.button("Generate"):
    if not input_text or not word_count:
        st.error("Please fill in all fields.")
    else:
        # Custom caching based on input parameters
        @st.cache_data
        def cached_response(email_text, email_style, word_count):
            return get_response(email_text, email_style, word_count)

        response = cached_response(input_text, email_style, int(word_count))
        st.write(response)
