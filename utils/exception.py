from fastapi import HTTPException

def raise_exception(status_code, detail):
    return HTTPException(status_code=status_code, detail=detail)