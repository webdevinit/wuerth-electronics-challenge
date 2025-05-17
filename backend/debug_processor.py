import pandas as pd
from io import BytesIO
from main_processor_input import process_bom_data
from openaispecsheetsearch import get_component_model_from_partnumber
from component_models import *
import json
import traceback
import sys # Import sys to read command line arguments

# This function is a modified version of the original upload_excel logic
# It takes a file path string as input instead of a FastAPI UploadFile
# Removed 'async' keyword to make it synchronous for easier debugging
def process_excel_file_for_debug(file_path: str):
    """
    Processes an Excel file directly for debugging purposes.

    Args:
        file_path: The path to the Excel file.
    """
    if not file_path.lower().endswith((".xls", ".xlsx")):
        print("Error: Please provide a valid Excel file path (.xls or .xlsx).")
        return

    try:
        print(f"Processing file: {file_path}")

        # Read the file content from the path
        with open(file_path, 'rb') as f:
            contents = f.read()

        excel_data = pd.read_excel(BytesIO(contents), sheet_name=None)
        all_rows = []
        for _, df in excel_data.items():
            df = df.fillna('')
            all_rows.extend(df.to_dict('records'))
        all_rows = all_rows[:5] # Limit to the first 5 rows for debugging, similar to the origina

        # Process all rows at once to get the complete list of components
        all_components = []
        for row in all_rows:
            components_from_row = process_bom_data([row])
            if components_from_row:
                all_components.extend(components_from_row)

        # Limit to the first 5 components for debugging, similar to the original API
        all_components = all_components[:5]

        print(f"Found {len(all_components)} components to process.")

        results = []
        for i, component in enumerate(all_components):
            try:
                partnumber = component.partnumber
                print(f"Processing partnumber: {partnumber}")

                # Get component model from part number
                # Removed 'await' keyword
                component_model_result = get_component_model_from_partnumber(partnumber)
                results.append(component_model_result)

                # Print processed result
                print(f"  Processed component {i}:")
                print(f"    Component Group: {component_model_result.category}")
                print(f"    Component Type: {pdtype}")
                print(f"    Manufacturer: {component_model_result.manufacturer}")
                print(f"    Part Number: {partnumber}")

            except Exception as e:
                # Handle errors for individual row processing
                print(f"  Error processing component {i} (Part Number: {component.partnumber if component else 'unknown'}): {str(e)}")
                traceback.print_exc() # Print traceback for detailed error info

        print("\nProcessing complete.")
        # You can optionally print the full results list here if needed
        # print("Full Results:", results)

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print("❌ An error occurred during file processing:")
        traceback.print_exc() # Print traceback for detailed error info
        print(f"Error details: {str(e)}")

# Main execution block to run the function directly
if __name__ == "__main__":

        # Call the synchronous function directly
    process_excel_file_for_debug("/Users/marcrodig/Development/wuerth-electronics-challenge/samples/bom.xlsx")

