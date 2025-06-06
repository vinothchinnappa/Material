from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()

@app.post("/process")
async def process_excel(file: UploadFile = File(...)):
    try:
        df = pd.read_excel(file.file)
        required = ["Material_Code", "Material_Name", "Category", "Quantity", "Unit", "Stock_Date"]
        if not all(col in df.columns for col in required):
            return JSONResponse(status_code=400, content={"error": "Missing required columns"})

        df["Stock_Date"] = df["Stock_Date"].astype(str)
        return df.to_dict(orient="records")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
