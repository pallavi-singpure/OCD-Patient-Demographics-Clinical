from pydantic import BaseModel

class OCDInput(BaseModel):
    Age: int
    Gender: str
    Ethnicity: str
    Marital_Status: str
    Education_Level: str
    Previous_Diagnoses: str
    Family_History_of_OCD: str
    Obsession_Type: str
    Compulsion_Type: str
    Depression_Diagnosis: str
    Anxiety_Diagnosis: str
    Medications: str
    Duration_of_Symptoms_months: int
    YBOCS_Obsessions: int
    YBOCS_Compulsions: int
