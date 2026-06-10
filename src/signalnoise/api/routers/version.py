from fastapi import APIRouter

router = APIRouter(tags=["Version"])


@router.get("/version")
def version():

    return {
        "service": "signalnoise-ai",
        "version": "1.0.0"
    }
