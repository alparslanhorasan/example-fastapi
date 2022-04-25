from fastapi import Depends, APIRouter

router = APIRouter()

def common_parameters():
    return {"a": "a", "b": "b", "c": "c"}

@router.get("/")
def read_items(commons: dict = Depends(common_parameters)):
    return commons