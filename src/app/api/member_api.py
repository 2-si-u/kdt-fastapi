from fastapi import APIRouter, Query, Depends
from app.services.member_service import get_member_service
from app.enums.member_enum import MemberProvider


router = APIRouter

@router.post("/check-member")
async def check_member(
    member_email: str,
    member_provider: str,
    member_service = Depends(get_member_service)
):

    await member_service.check_dupicate_member(member_email, member_provider)