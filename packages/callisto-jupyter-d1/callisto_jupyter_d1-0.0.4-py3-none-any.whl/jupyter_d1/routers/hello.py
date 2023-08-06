from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def hello():
    return {"message": "Hello World"}


@router.get("/{name}")
async def hello_user(name: str):
    return {"message": f"Hello {name}"}
