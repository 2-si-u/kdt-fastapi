from fastapi import FastAPI
from app.security.cors import setup_cors
from app.security.security_headers import set_up_security
from contextlib import asynccontextmanager
from app.infrastructure.postgressql import engine, Base
import app.models
from app.apis import member_api, post_api

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 비동기 연결
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)    # await: 비동기 작업이 끝날 때까지 기다릴 때 사용하는 키워드
        print("PostgreSQL 연결 성공!")

    yield

app = FastAPI(
    lifespan=lifespan,
    title="Fast API Service",
    description="파이썬 백엔드 구축!😎",
    version="1.0.0",
    docs_url="/docs", # Swagger
    redoc_url="/redoc"
)

setup_cors(app) 
set_up_security(app)

@app.get("/")
def health_check():
    return {"message": "Hello World"}

app.include_router(member_api.router, prefix="/members", tags=["members"])
app.include_router(post_api.router, prefix="/posts",tags=["posts"])