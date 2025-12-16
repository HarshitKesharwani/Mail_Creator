import streamlit as st 
from langchain_groq import ChatGroq
from langchain_classic.chains import LLMChain
from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains.summarize import load_summarize_chain
import os
from dotenv import load_dotenv
load_dotenv()



st.title("EMAIL GENERATOR")
groq_api_key=st.text_input("Enter GROQ_API_KEY")
input=st.text_input("Enter you email content")
tone = st.sidebar.selectbox(
    "Choose the tone of your email:",
    ["Formal", "Friendly", "Persuasive", "Casual"]
)
st.sidebar.success(f"You Selected {tone} tone")
language=st.sidebar.selectbox(
    "Choose th language you want for your email",
    ['Hindi','French','English','Russian'])
st.sidebar.success(f"You selected {language}")
prompt="""
From the given context create a professional email with a well formed structure
Context:{text}
And the tone of the mail will be : {tone}
And I want my mail to be in {language} language
Please mention the tone in your output
Provide multiple subject lines after the mail body which should be visible
"""
final_prompt=PromptTemplate(input_variables=['text','tone','language'],template=prompt)

if st.button("Get Email"):
    with st.spinner("Loading Email ..."):
        llm=ChatGroq(model="openai/gpt-oss-20b",groq_api_key=groq_api_key)
        chain=LLMChain(llm=llm,prompt=final_prompt)
        summary=chain.run({'text':input,'tone':tone,'language':language})
        st.success(summary)
        st.download_button(
        label="Download as TXT",
        data=summary,
        file_name="email.txt",
        mime="text/plain"
        )



