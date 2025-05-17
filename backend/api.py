from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
from io import BytesIO
from main_processor_input import process_bom_data
from openaispecsheetsearch import get_component_model_from_partnumber
import json
from fastapi.middleware.cors import CORSMiddleware
import traceback



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # oder "*" für alle Domains (unsicher in Produktion)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-excel", response_class=StreamingResponse)
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Bitte lade eine gültige Excel-Datei hoch.")
    try:
        contents = await file.read()
        print (f"Received file: {file.filename}, size: {len(contents)} bytes")  # Debug print
        excel_data = pd.read_excel(BytesIO(contents), sheet_name=None) # Limit to first 5 sheets
        all_rows = []
        for _, df in excel_data.items():
            df = df.fillna('')
            all_rows.extend(df.to_dict('records'))

        # Process all rows at once to get the complete list of components
        all_components = []
        for row in all_rows:
            components_from_row = process_bom_data([row])
            if components_from_row:
                all_components.extend(components_from_row)
                
        all_components = all_components[:5]

        results = []
        async def event_generator(components_list):
            # Send initial message with total count and basic info
            initial_data = {
                "status": "initial",
                "total_components": len(components_list),
                "partnumbers": [comp.partnumber for comp in components_list]
            }
            yield f"data: {json.dumps(initial_data)}\n\n"

            for i, component in enumerate(components_list):
                try:
                    partnumber = component.partnumber
                    print(f"Processing partnumber: {partnumber}") # Debug print

                    # Get component model from part number
                    component_model_result = get_component_model_from_partnumber(partnumber)
                    results.append(component_model_result)

                    # Format result for SSE
                    event_data = {
                        "id": i,
                        "productType:": component_model_result.category,
                        "manufacturer": component_model_result.manufacturer,
                        "partnumber": partnumber,
                        "status": "identified",
                    }
                    yield json.dumps(event_data)

                except Exception as e:
                    # Handle errors for individual row processing
                    error_data = {
                        "id": i,
                        "productType:": "failed",
                        "manufacturer": "failed",
                        "partnumber": partnumber,
                        "status": f"Error processing row: {str(e)}",
                    }
                    yield json.dumps(error_data)

            # Optional: Send a completion message
            yield "data: {\"status\": \"complete\"}\n\n"

        return StreamingResponse(event_generator(all_components), media_type="text/event-stream")

    except Exception as e:
        print("❌ Fehler:", traceback.format_exc())  # <- DAS HINZUFÜGEN
        raise HTTPException(status_code=500, detail=f"Fehler beim Verarbeiten der Excel-Datei: {str(e)}")
