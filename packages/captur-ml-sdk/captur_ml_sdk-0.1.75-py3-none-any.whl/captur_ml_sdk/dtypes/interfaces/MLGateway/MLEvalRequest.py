from captur_ml_sdk.dtypes.generics import Image, EvaluationMeta, EvaluationModel
from pydantic import BaseModel
from typing import List, Optional, Dict


class ModelEvaluateRequest(BaseModel):
    data: List[Image]
    meta: Optional[EvaluationMeta] = None
    models: List[EvaluationModel]
    mapping: Optional[Dict[str, Dict[str, str]]]
