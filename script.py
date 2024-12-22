import os
import openai
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain

# Set your OpenAI API key
openai_api_key = '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'


# Initialize LangChain's OpenAI LLM model
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)


# Define a prompt to instruct the model to add type hints to Python code
prompt_template = """
The following Python code lacks type hints. Add type hints to it and return the type-hinted version.

Code:
{code}
"""
prompt = PromptTemplate(input_variables=["code"], template=prompt_template)
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Function to read a .py file and return its content as a string
def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

# Function to write content back to a .py file
def write_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)

# Function to process a .py file and get a type-hinted version
def add_type_hints(file_path):
    try:
        # Read the original content of the file
        original_code = read_file(file_path)
        
        # Ask the LLM to add type hints to the code
        type_hinted_code = llm_chain.run(original_code)
        
        # Write the type-hinted code back to the file
        write_file(file_path, type_hinted_code)
        print(f"Type-hinted version written to {file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

# Function to traverse through directories and process .py files
def process_directory(directory):
    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):  # Check if the file is a Python file
                file_path = os.path.join(root, file)
                add_type_hints(file_path)

if __name__ == "__main__":
    # Input directory from user
    directory_name = input("Enter the directory name: ")

    if os.path.isdir(directory_name):
        process_directory(directory_name)
    else:
        print(f"{directory_name} is not a valid directory.")
