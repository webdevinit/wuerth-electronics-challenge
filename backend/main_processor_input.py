import os
import pandas as pd
from dotenv import load_dotenv
from typing import Optional, Tuple, Union, List, Dict, Any

from pydantic import BaseModel, Field, ConfigDict

# Langchain imports
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Import your component classes
# Assuming classes.py is in the same directory or accessible via PYTHONPATH
try:
    # These are your actual application classes
    from classes import Component, Capacitor as AppCapacitor, Inductor as AppInductor, Resistor as AppResistor
except ImportError:
    # Fallback for direct execution if classes.py is in a different relative path
    import sys
    sys.path.append(os.path.dirname(__file__))
    from classes import Component, Capacitor as AppCapacitor, Inductor as AppInductor, Resistor as AppResistor
# --- Pydantic Models for Langchain Structured Output ---
from component_models import CapacitorModel, InductorModel, ResistorModel, ComponentBaseModel

# --- Environment Variable Loading ---
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env')
load_dotenv(dotenv_path=env_path, override=True)

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_MODEL_NAME = "gpt-4o" # Or your specific deployment name for gpt-4o

# --- LLM Client Initialization ---
if not all([AZURE_ENDPOINT, AZURE_API_VERSION, AZURE_API_KEY]):
    print("Azure OpenAI environment variables not fully set. Please check your 'env' file.")
    exit(1)

llm = AzureChatOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_version=AZURE_API_VERSION,
    api_key=AZURE_API_KEY,
    azure_deployment=AZURE_MODEL_NAME, # Use azure_deployment for the model name
    temperature=0,
    max_tokens=2000
)

# --- Excel Data Reading ---
def load_excel_data(file_path: str) -> List[Dict[str, Any]]:
    try:
        excel_data = pd.read_excel(file_path, sheet_name=None) # Read all sheets
        all_rows = []
        for sheet_name, df in excel_data.items():
            print(f"Processing sheet: {sheet_name}")
            # Convert dataframe to list of dictionaries (each dict is a row)
            # Handle potential NaN values by converting them to None or empty strings
            df = df.fillna('') 
            all_rows.extend(df.to_dict('records'))
        return all_rows
    except FileNotFoundError:
        print(f"Error: Excel file not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []

# --- Prompt Engineering ---
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert in electronic components and data extraction. "
            "Your task is to analyze the provided Bill of Materials (BOM) row data. "
            "First, determine if the component is a Capacitor, Inductor, or Resistor. "
            "Then, extract all relevant specifications for that component type. "
            "Format your output strictly using the 'ComponentBaseModel', ensuring the 'final_ouput' field "
            "contains an instance of either CapacitorModel, InductorModel, or ResistorModel. " # Updated prompt
            "Ensure all required fields in the chosen model are populated. If a value is not present or applicable, use null or an appropriate default if the model allows. "
            "Pay close attention to units and formats as described in the model fields."
        ),
        ("human", "Please process the following BOM row data:\n\n```\n{row_data}\n```"),
    ]
)

# --- Main Processing Logic ---
def process_bom_data(excel_rows: List[Dict[str, Any]]) -> List[Component]: # Return type is your app's Component
    created_objects = []
    
    structured_llm = llm.with_structured_output(
        schema=ComponentBaseModel, # This is the schema the LLM will fill
        method="function_calling",
        include_raw=False
    )
    
    chain = prompt_template | structured_llm

    for i, row in enumerate(excel_rows):
        print(f"\nProcessing row {i+1}: {row}")
        row_data_str = "\n".join([f"{k}: {v}" for k, v in row.items()])

        try:
            # parsed_model will be an instance of ComponentBaseModel
            parsed_model_wrapper = chain.invoke({"row_data": row_data_str})
            
            # The actual component data (CapacitorModel, InductorModel, or ResistorModel)
            # is in the 'final_ouput' field of the wrapper.
            actual_component_data = parsed_model_wrapper.final_ouput 

            print(f"LLM Parsed Output Type: {type(actual_component_data)}")
            print(f"LLM Parsed Data: {actual_component_data.dict()}")

            component_obj = None
            # Now check component_type on actual_component_data
            if actual_component_data.component_type == "Capacitor" and isinstance(actual_component_data, CapacitorModel):
                component_obj = AppCapacitor( # Use aliased AppCapacitor from classes.py
                    name=actual_component_data.name,
                    manufacturer=actual_component_data.manufacturer,
                    partnumber=actual_component_data.partnumber,
                    capacitance=actual_component_data.capacitance,
                    rated_voltage=actual_component_data.rated_voltage,
                    case_code=actual_component_data.case_code,
                    dimensions=tuple(actual_component_data.dimensions) if actual_component_data.dimensions else None, # Convert list back to tuple if your class expects it
                    tolerance=actual_component_data.tolerance,
                    dielectric_material=actual_component_data.dielectric_material,
                    temp_coefficient=actual_component_data.temp_coefficient,
                    min_operating_temp=actual_component_data.min_operating_temp,
                    max_operating_temp=actual_component_data.max_operating_temp
                )
            elif actual_component_data.component_type == "Inductor" and isinstance(actual_component_data, InductorModel):
                component_obj = AppInductor( # Use aliased AppInductor
                    name=actual_component_data.name,
                    manufacturer=actual_component_data.manufacturer,
                    partnumber=actual_component_data.partnumber,
                    inductance=actual_component_data.inductance,
                    rated_current=actual_component_data.rated_current,
                    case_code=actual_component_data.case_code,
                    dimensions=tuple(actual_component_data.dimensions) if actual_component_data.dimensions else None,
                    shielding=actual_component_data.shielding,
                    dc_resistance=actual_component_data.dc_resistance,
                    tolerance=actual_component_data.tolerance,
                    min_operating_temp=actual_component_data.min_operating_temp,
                    max_operating_temp=actual_component_data.max_operating_temp,
                    self_resonant_freq=actual_component_data.self_resonant_freq
                )
            elif actual_component_data.component_type == "Resistor" and isinstance(actual_component_data, ResistorModel):
                component_obj = AppResistor( # Use aliased AppResistor
                    name=actual_component_data.name,
                    manufacturer=actual_component_data.manufacturer,
                    partnumber=actual_component_data.partnumber,
                    resistance=actual_component_data.resistance,
                    power_rating=actual_component_data.power_rating,
                    case_code=actual_component_data.case_code,
                    dimensions=tuple(actual_component_data.dimensions) if actual_component_data.dimensions else None,
                    tolerance=actual_component_data.tolerance,
                    temp_coefficient=actual_component_data.temp_coefficient,
                    min_operating_temp=actual_component_data.min_operating_temp,
                    max_operating_temp=actual_component_data.max_operating_temp
                )

            if component_obj:
                created_objects.append(component_obj)
                print(f"Successfully created: {component_obj.category} - {component_obj.name}")
            else:
                print(f"LLM returned an unexpected model type or failed to match for row: {row_data_str}")
                print(f"Received component_type: {actual_component_data.component_type if hasattr(actual_component_data, 'component_type') else 'N/A'}")

        except Exception as e:
            print(f"Error processing row {i+1} with LLM: {e}")
            print(f"Problematic row data: {row_data_str}")
        # break # Consider removing or commenting out this break for full processing
    return created_objects

def save_components_to_csv(components: List[Component], output_dir: str):
    if not components:
        print("No components to save.")
        return

    os.makedirs(output_dir, exist_ok=True)

    capacitors_list = []
    inductors_list = []
    resistors_list = []

    for comp in components:
        comp_data = {
            "name": getattr(comp, 'name', None),
            "manufacturer": getattr(comp, 'manufacturer', None),
            "partnumber": getattr(comp, 'partnumber', None),
            "category": getattr(comp, 'category', None),
            "case_code": getattr(comp, 'case_code', None),
            # Convert dimensions to string for CSV compatibility
            "dimensions": str(getattr(comp, 'dimensions', None)) if getattr(comp, 'dimensions', None) is not None else None,
            "tolerance": getattr(comp, 'tolerance', None),
            "min_operating_temp": getattr(comp, 'min_operating_temp', None),
            "max_operating_temp": getattr(comp, 'max_operating_temp', None),
        }
        if isinstance(comp, AppCapacitor):
            comp_data.update({
                "capacitance": getattr(comp, 'capacitance', None),
                "rated_voltage": getattr(comp, 'rated_voltage', None),
                "dielectric_material": getattr(comp, 'dielectric_material', None),
                "temp_coefficient": getattr(comp, 'temp_coefficient', None),
            })
            capacitors_list.append(comp_data)
        elif isinstance(comp, AppInductor):
            comp_data.update({
                "inductance": getattr(comp, 'inductance', None),
                "rated_current": getattr(comp, 'rated_current', None),
                "shielding": getattr(comp, 'shielding', None),
                "dc_resistance": getattr(comp, 'dc_resistance', None),
                "self_resonant_freq": getattr(comp, 'self_resonant_freq', None),
            })
            inductors_list.append(comp_data)
        elif isinstance(comp, AppResistor):
            comp_data.update({
                "resistance": getattr(comp, 'resistance', None),
                "power_rating": getattr(comp, 'power_rating', None),
                "temp_coefficient": getattr(comp, 'temp_coefficient', None),
            })
            resistors_list.append(comp_data)

    if capacitors_list:
        df_caps = pd.DataFrame(capacitors_list)
        # Define column order for capacitors based on attributes from matching rules
        cap_cols = [
            "name", "manufacturer", "partnumber", "category", "capacitance", "rated_voltage", 
            "case_code", "dimensions", "tolerance", "dielectric_material", 
            "temp_coefficient", "min_operating_temp", "max_operating_temp"
        ]
        # Reorder and ensure all specified columns are present
        df_caps = df_caps.reindex(columns=cap_cols)
        df_caps.to_csv(os.path.join(output_dir, "capacitors.csv"), index=False)
        print(f"Saved {len(df_caps)} capacitors to {os.path.join(output_dir, 'capacitors.csv')}")

    if inductors_list:
        df_inds = pd.DataFrame(inductors_list)
        # Define column order for inductors
        ind_cols = [
            "name", "manufacturer", "partnumber", "category", "inductance", "rated_current", 
            "case_code", "dimensions", "shielding", "dc_resistance", 
            "tolerance", "min_operating_temp", "max_operating_temp", "self_resonant_freq"
        ]
        df_inds = df_inds.reindex(columns=ind_cols)
        df_inds.to_csv(os.path.join(output_dir, "inductors.csv"), index=False)
        print(f"Saved {len(df_inds)} inductors to {os.path.join(output_dir, 'inductors.csv')}")

    if resistors_list:
        df_ress = pd.DataFrame(resistors_list)
        # Define column order for resistors
        res_cols = [
            "name", "manufacturer", "partnumber", "category", "resistance", "power_rating", 
            "case_code", "dimensions", "tolerance", "temp_coefficient", 
            "min_operating_temp", "max_operating_temp"
        ]
        df_ress = df_ress.reindex(columns=res_cols)
        df_ress.to_csv(os.path.join(output_dir, "resistors.csv"), index=False)
        print(f"Saved {len(df_ress)} resistors to {os.path.join(output_dir, 'resistors.csv')}")


if __name__ == "__main__":
    excel_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "samples", "bom.xlsx")
    # Output directory changed to the current script's directory
    output_directory = os.path.dirname(os.path.abspath(__file__)) 
    
    print(f"Attempting to load Excel data from: {excel_file_path}")
    bom_rows = load_excel_data(excel_file_path)

    if bom_rows:
        print(f"\nFound {len(bom_rows)} rows in the Excel file. Starting LLM processing...")
        final_component_objects = process_bom_data(bom_rows)
        
        print("\n--- Final List of Created Objects ---")
        if final_component_objects:
            for obj in final_component_objects:
                # Basic representation; you might want to implement __str__ or __repr__ in your classes
                print(f"Type: {obj.category}, Name: {obj.name}, Manufacturer: {obj.manufacturer}")
                # Print more attributes as needed
                if hasattr(obj, 'capacitance'): print(f"  Capacitance: {obj.capacitance}")
                if hasattr(obj, 'inductance'): print(f"  Inductance: {obj.inductance}")
                if hasattr(obj, 'resistance'): print(f"  Resistance: {obj.resistance}")
            
            # Save the components to CSV files
            print(f"\n--- Saving components to CSV files in {output_directory} ---")
            save_components_to_csv(final_component_objects, output_directory)
        else:
            print("No component objects were successfully created.")
    else:
        print("No data loaded from Excel. Exiting.")
