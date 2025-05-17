import os
import pandas as pd
from dotenv import load_dotenv
from typing import List, Dict, Any

from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

# --- Load Environment ---
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env')
load_dotenv(dotenv_path=env_path, override=True)

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_MODEL_NAME = "gpt-4o"

# --- Initialize LLM ---
llm = AzureChatOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_version=AZURE_API_VERSION,
    api_key=AZURE_API_KEY,
    azure_deployment=AZURE_MODEL_NAME,
    temperature=0,
    max_tokens=2000
)

class ComponentList(BaseModel):
    serial_numbers: List[str]

# Chain setup
structured_llm = llm.with_structured_output(
    schema=ComponentList,
    method="function_calling",
    include_raw=False
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert in electronic components. For each row in the following Markdown BOM table, "
        "identify the component and extract a concise identifier for it. "
        "Return a list of serial numbers, one per component, that uniquely represents each component row. "
        "Do not include any other information or explanations. Just serial numbers longer than 5 characters. "
    ),
    ("human", "{markdown_chunk}")
])

chain = prompt | structured_llm

# --- Helpers ---
def load_excel_data(file_bytes: bytes) -> List[Dict[str, Any]]:
    excel_data = pd.read_excel(file_bytes, sheet_name=None)
    all_rows = []
    for df in excel_data.values():
        df = df.fillna('')
        all_rows.extend(df.to_dict('records'))
    return all_rows

def chunk_rows(data: List[Dict[str, Any]], chunk_size: int) -> List[List[Dict[str, Any]]]:
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

def extract_serial_numbers(data: List[Dict[str, Any]], chunk_size: int = 200) -> List[str]:
    row_chunks = chunk_rows(data, chunk_size)
    serials = []

    for idx, chunk in enumerate(row_chunks):
        print(f"🔄 Processing chunk {idx + 1}/{len(row_chunks)}...")
        markdown_chunk = pd.DataFrame(chunk).to_markdown(index=False)
        try:
            response = chain.invoke({"markdown_chunk": markdown_chunk})
            filtered_serials = [s for s in response.serial_numbers if len(s) >= 5]
            serials.extend(filtered_serials)
            serials.extend(response.serial_numbers)
        except Exception as e:
            print(f"❌ Error in chunk {idx + 1}: {e}")
            
    unique_serials = list(dict.fromkeys(serials))
    return unique_serials