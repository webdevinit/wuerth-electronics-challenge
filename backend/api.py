from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from matchmaking.matchmaking import match_wuerth_components, rules
import pandas as pd
from io import BytesIO
from main_processor_input import load_excel_data, extract_serial_numbers
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
@app.post("/parse-excel")
async def parse_excel(file: UploadFile = File(...)):
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Bitte lade eine gültige Excel-Datei hoch.")

    try:
        content = await file.read()
        rows = load_excel_data(content)
        if not rows:
            raise HTTPException(status_code=400, detail="Keine BOM-Daten in der Excel-Datei gefunden.")
        serial_numbers = extract_serial_numbers(rows)
        return {"partnumbers": serial_numbers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler beim Verarbeiten der Datei: {str(e)}")
    
@app.get("/identify-part")
async def identify_part(partnumber: str):
    try:
        result = get_component_model_from_partnumber(partnumber)
        response = {
            "id": partnumber,
            "partNumber": partnumber,
            "productType": result.category,
            "manufacturer": result.manufacturer,
            "status": "identified"
        }
        return JSONResponse(content=response)

    except Exception as e:
        print("❌ Fehler beim Identifizieren:", traceback.format_exc())
        error_response = {
            "id": partnumber,
            "partNumber": partnumber,
            "status": "failed",
            "error": str(e)
        }
        return JSONResponse(content=error_response, status_code=200)
@app.post("/find-components")
def find_components():
    source = {
        "Order_Code": "890324025031CS",
        "Product_Group": "Capacitors",
        "Product_Series": "WCAP-FTX2 Film Capacitors",
        "Product_Family": "Film Capacitors",
        "Capacitance (µF)": 0.27,
        "Rated_Voltage (V)": 275,
        "Rated_Voltage_2 (V)": 560,
        "Rate_Of_Voltage_Rise (V/µs)": 250,
        "Dissipation_Factor (%)": 3,
        "Operating_Temperature (°C) Minimum": -40,
        "Operating_Temperature (°C) Maximum": 105,
        "Safety_Class": "X2",
        "Pitch (mm)": 15,
        "Length (mm)": 18,
        "Width (mm)": 7.5,
        "Height (mm)": 14.5,
        "Size_Code": "Pitch 15 mm",
    }

    matches = match_wuerth_components(source, top_k=5)

    json_response = {
        "part_competitor": {
            "id": "123456789",
            "manufacturer": "Siemens",
            "partnumber": "123456789",
            "specs": [
                {
                    "attribute": attr,
                    "value": source.get(attr)
                } for attr in source.keys()
            ]
        },
        "wuerth_suggestions": []
    }

    json_response["wuerth_suggestions"] = []

    for match_component, _ in matches:
        suggestion = {
            "Order_Code": match_component.get("Order_Code"),
            "specs": []
        }

        for rule in rules.get_rules_for(source["Product_Group"], source["Product_Family"]):
            attr_keys = rule.attribute_key if isinstance(rule.attribute_key, list) else [rule.attribute_key]

            for attr in attr_keys:
                source_value = source.get(attr)
                match_value = match_component.get(attr)

                if source_value is None or match_value is None:
                    continue

                outcome = "failed"

                if isinstance(source_value, (int, float)) and isinstance(match_value, (int, float)):
                    # Consider operator semantics
                    if rule.operator_str == "=":
                        diff = abs(source_value - match_value) / max(abs(source_value), 1)
                        if diff < 0.15:
                            outcome = "tolerated"
                    elif rule.operator_str == ">=":
                        outcome = "good" if match_value >= source_value else "failed"
                    elif rule.operator_str == "<=":
                        outcome = "good" if match_value <= source_value else "failed"
                else:
                    # fallback to equality check for non-numeric
                    if source_value == match_value:
                        outcome = "good"

                suggestion["specs"].append({
                    "attribute": attr,
                    "values": [match_value, source_value],
                    "rule_outcome": outcome,
                    "operator": rule.operator_str
                })

        json_response["wuerth_suggestions"].append(suggestion)

    return json_response