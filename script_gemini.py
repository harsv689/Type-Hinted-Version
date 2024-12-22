import os
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from typing import Optional
import warnings
# Set up your Gemini API key and model
genai.configure(api_key="AIzaSyAfVPJ3ulIrwxZtWzD2bXxgINGjxo12cM0")
warnings.filterwarnings("ignore", category=UserWarning, message=".*absl::InitializeLog()")

# Function to call Gemini API and get the response
def call_gemini_api(prompt: str) -> Optional[str]:
    # Create the model configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Initialize the Gemini model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    
    # Start the chat session
    chat_session = model.start_chat(history=[])
    
    # Send the prompt message and get the response
    response = chat_session.send_message(prompt)
    
    return response.text if response else None

# Define a prompt to instruct the model to add type hints to Python code
prompt_template: str = """
The following Python code lacks type hints. Add type hints to it and return the type-hinted version.

Code:
{code}
"""
prompt: PromptTemplate = PromptTemplate(input_variables=["code"], template=prompt_template)

# Function to read a .py file and return its content as a string
def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()

# Function to write content back to a .py file
def write_file(file_path: str, content: str) -> None:
    with open(file_path, "w") as file:
        file.write(content)

# Function to process a .py file and get a type-hinted version
def add_type_hints(file_path: str) -> None:
    try:
        # Read the original content of the file
        original_code: str = read_file(file_path)
        
        # Format the prompt with the original code
        formatted_prompt: str = prompt.format(code=original_code)
        
        # Call the Gemini API to add type hints
        type_hinted_code: Optional[str] = call_gemini_api(formatted_prompt)
        
        if type_hinted_code:
            # Write the type-hinted code back to the file
            write_file(file_path, type_hinted_code)
            print(f"Type-hinted version written to {file_path}")
        else:
            print(f"Failed to get type-hinted code for {file_path}")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

# Function to traverse through directories and process .py files
def process_directory(directory: str) -> None:
    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):  # Check if the file is a Python file
                file_path: str = os.path.join(root, file)
                add_type_hints(file_path)

if __name__ == "__main__":
    # Input directory from user
    directory_name: str = input("Enter the directory name: ")

    if os.path.isdir(directory_name):
        process_directory(directory_name)
    else:
        print(f"{directory_name} is not a valid directory.")
