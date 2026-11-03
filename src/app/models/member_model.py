from datetime import datetime, timedelta, timezone
from sqlalchemy import BigInteger, Text, DateTime, Identity,UniqueConstraint, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.enums.member_enum import MemberProvider

# PostgreSQL의 Base를 상속받아서 서버가 켜질 때 동기화시킨다.
from app.infrastructure.postgressql import Base

KST = timezone(timedelta(hours=9)) # UTC+9

class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    member_email: Mapped[str] = mapped_column(Text, nullable=False)
    member_password: Mapped[str | None] = mapped_column(Text)
    member_name: Mapped[str | None] = mapped_column(Text)
    member_age: Mapped[int | None] = mapped_column(Integer)
    member_profile: Mapped[str | None] = mapped_column(Text, default="/members/defult.jpg")
    member_provider_id: Mapped[str | None] = mapped_column(Text, unique=True)
    member_provider: Mapped[MemberProvider] = mapped_column(
        Enum(MemberProvider, native_enum=False),
        nullable=False,
        default=MemberProvider.LOCAL
    )
    member_created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime)

    __table_args__ = (
        UniqueConstraint("member_email", "member_provider", name="uq_member_email_provider"),
    )

