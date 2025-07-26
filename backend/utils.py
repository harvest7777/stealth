from pydantic import BaseModel, Field
from typing import Optional, Literal

class JobFormSchema(BaseModel):
    dataset_repo_id: str = Field(..., example="DanqingZ/filtered_pick_yellow_pink")
    model_id: str = Field(..., example="lerobot/pi0")
    gpu_type: str = Field(..., example="A100")
    policy_name: str = Field(..., example="Job name")
    mode: Literal["fine_tuning", "from_scratch"] = Field(..., example="fine_tuning")
    steps: int = Field(..., gt=0, example=20)
    save_freq: int = Field(..., gt=0, example=200000)
    log_freq: int = Field(..., gt=0, example=100)
    batch_size: Optional[int] = Field(None, gt=0, example=64)
