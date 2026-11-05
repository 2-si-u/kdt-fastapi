from fastapi import APIRouter, Query, Depends
from app.services.post_service import get_post_service, PostService
from app.schemas.common_schema import ApiResponseDTO
from app.schemas.post_schema import PostCreateDTO

from app.models.post_model import Post, PostSortEnum
from app.infrastructure.postgressql import get_postgresql_db, AsyncSession
import random

router = APIRouter()

# /post, POST
@router.post(
    "",
    summary="게시글 작성",
    response_model=ApiResponseDTO
)
async def write_post(
    member_id: int,
    post:PostCreateDTO,
    post_service: PostService = Depends(get_post_service)
):

    new_post_id = await post_service.write_post(member_id, post)

    return ApiResponseDTO(
        success = True,
        message="게시글 작성 성공",
        data={
            "newPostId": new_post_id
        }
    )

@router.get(
        "/{post_id}",
        summary="게시물 조회(post_id)",
        response_model=ApiResponseDTO
)
async def read_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service)
):
    found_post = await PostService.read_post(post_id)

    return ApiResponseDTO(
        success=True,
        message=f"{post_id}번 게시글 조회 성공",
        data=found_post
    )

@router.get(
        "",
        summary="게시판 전체 조회",
        response_model=ApiResponseDTO
)
async def get_posts(
    offset: int =  Query(0, ge=0, description="시작오프셋"),
    limit: int = Query(10, ge=1, le=100, description="가져올 개수"),
    sort_by: PostSortEnum = Query):""






















# 더미 데이터 추가
@router.post("/dummies", summary="게시판 더미데이터 추가")
async def get_dummies(
    count: int = 100,
    db:AsyncSession = Depends(get_postgresql_db)
):
    target_member_ids = [1, 2, 3]

    for i in range(1, count + 1):
        random_member_id = random.choice(target_member_ids)
        random_view = random.randint(0, 10000)

        new_post = Post(
            post_title=f"랜덤 테스트 제목 {i}",
            post_content=f"랜덤한 글 내용 {i}",
            post_read_count=random_view,
            member_id=random_member_id
        )

        db.add(new_post)

    await db.commit()

    return {
        "message": "더미데이터 추가 성공!"
    }
