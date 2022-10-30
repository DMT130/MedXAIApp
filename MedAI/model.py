from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Patient_Form(BaseModel):
    Patient_Name: str
    Age: int
    Image: str
    creation_date: datetime.datetime = datetime.now()

class Predictions(Patient_Form):
    Deseases: Optional[List] = None
    BoundingBox: Optional[List] = None

