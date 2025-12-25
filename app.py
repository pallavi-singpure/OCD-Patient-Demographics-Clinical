from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import joblib
from schema import OCDInput  # Import your schema

app = FastAPI(title="OCD Severity Prediction")

model = joblib.load("ocd_severity_model.pkl")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Helper to map Form data to Schema
def ocd_form_data(
        Age: int = Form(...), Gender: str = Form(...), Ethnicity: str = Form(...),
        Marital_Status: str = Form(...), Education_Level: str = Form(...),
        Previous_Diagnoses: str = Form(...), Family_History_of_OCD: str = Form(...),
        Obsession_Type: str = Form(...), Compulsion_Type: str = Form(...),
        Depression_Diagnosis: str = Form(...), Anxiety_Diagnosis: str = Form(...),
        Medications: str = Form(...), Duration_of_Symptoms_months: int = Form(...),
        YBOCS_Obsessions: int = Form(...), YBOCS_Compulsions: int = Form(...)
):
    return OCDInput(
        Age=Age, Gender=Gender, Ethnicity=Ethnicity, Marital_Status=Marital_Status,
        Education_Level=Education_Level, Previous_Diagnoses=Previous_Diagnoses,
        Family_History_of_OCD=Family_History_of_OCD, Obsession_Type=Obsession_Type,
        Compulsion_Type=Compulsion_Type, Depression_Diagnosis=Depression_Diagnosis,
        Anxiety_Diagnosis=Anxiety_Diagnosis, Medications=Medications,
        Duration_of_Symptoms_months=Duration_of_Symptoms_months,
        YBOCS_Obsessions=YBOCS_Obsessions, YBOCS_Compulsions=YBOCS_Compulsions
    )


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict", response_class=HTMLResponse)
def predict(request: Request, data: OCDInput = Depends(ocd_form_data)):
    # Convert Pydantic model to Dict and then to DataFrame
    # Note: Ensure the keys here match the column names your model was trained on!
    input_df = pd.DataFrame([data.dict()])

    # Renaming columns to match your specific model requirements
    input_df.columns = [
        "Age", "Gender", "Ethnicity", "Marital Status", "Education Level",
        "Previous Diagnoses", "Family History of OCD", "Obsession Type",
        "Compulsion Type", "Depression Diagnosis", "Anxiety Diagnosis",
        "Medications", "Duration of Symptoms (months)",
        "Y-BOCS Score (Obsessions)", "Y-BOCS Score (Compulsions)"
    ]

    prediction = model.predict(input_df)[0]

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "prediction": prediction}
    )