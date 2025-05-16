from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
import pandas as pd
from io import BytesIO

app = FastAPI()

@app.post("/upload-excel", response_class=PlainTextResponse)
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Please upload a valid Excel file.")

    try:
        contents = await file.read()
        excel_data = pd.read_excel(BytesIO(contents), sheet_name=None)  # Read all sheets
        text_output = ""

        for sheet_name, df in excel_data.items():
            text_output += f"Sheet: {sheet_name}\n"
            text_output += df.to_string(index=False)
            text_output += "\n\n"

        return text_output.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process the Excel file: {str(e)}")
