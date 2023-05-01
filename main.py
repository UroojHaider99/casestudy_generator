import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os
import pyperclip


# Set the page title and icon
st.set_page_config(page_title="Case Study Generator", page_icon="\U0001F916")



# Define the case study prompt template
template = """
    As an interviewer for the {role} role, your task is to generate one creative and detailed case study that will effectively test the candidate's proficiency required for the role. Ensure that the case study is relevant to the role. Provide sufficient context, background information, and specific challenges that will enable the candidate to showcase their skills and problem-solving abilities. The case study should be between 200 to 220 words.
    
    CASE STUDY 1:
"""

# Initialize the PromptTemplate
prompt = PromptTemplate(
    input_variables=["role"],
    template=template,
)

# Define the header
st.markdown("<h1 style='font-family: Bebas Neue;'>Case Study Generator</h1>", unsafe_allow_html=True)
st.write("Use this tool to generate a case study to test candidates for a particular role. "
         "Powered by [LangChain](https://langchain.com/) and [OpenAI](https://openai.com), created by "
         "[@UroojHaider](https://twitter.com/notarooj_).")


popular_roles = ["Software Developer", "Data Scientist", "Product Manager", "Sales Manager", "Marketing Manager",
                 "Customer Support Representative", "Business Analyst", "Graphic Designer", "Content Writer", "UI/UX Designer"]
# Define the role selection
st.markdown("<h4 style='font-family: Bebas Neue;'>Select Role Name</h4>", unsafe_allow_html=True)
role_option = st.selectbox("Choose a popular role or enter a custom role name:",
                           ["Other"] + popular_roles, key="role_option")

if role_option == "Other":
    role_input = st.text_input(label="Enter custom role name:", key="role_input")
else:
    role_input = role_option

if not role_input:
    st.warning("Please select or enter a role name.")
    st.stop()

if "role_input" not in st.session_state:
    st.session_state.role_input = ""

if st.session_state.role_input != role_input:
    llm = OpenAI(temperature=.7, openai_api_key="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")
    prompt_with_role = prompt.format(role=role_input)
    with st.spinner("Generating case study..."):
        generated_case_studies = llm(prompt_with_role)
    st.session_state.generated_case_studies = generated_case_studies
    st.session_state.role_input = role_input

# Display the generated case study
st.markdown("<h2 class='subtitle'>Generated Case Study</h2>", unsafe_allow_html=True)
st.write(st.session_state.generated_case_studies)



# Add a copy button
copy_button_col, _ = st.columns([3, 1])
if copy_button_col.button("Copy to Clipboard"):
    pyperclip.copy(st.session_state.generated_case_studies)
    st.success("Case study copied to clipboard!")


