from fastapi import Request, Depends
from auth.authentication import verify_token
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy import select
from model import User

async def user_in_response(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    user_id = verify_token(token)
    user = None
    if user_id:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().one_or_none()
        
        
    return user