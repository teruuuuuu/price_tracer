from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.connection import get_db
from repository.instrument_repository import InstrumentRepository

# 💡 APIRouterインスタンスを作成
# prefixでURLの共通部分を指定しておくと便利です
router = APIRouter(
    prefix="/instruments",
    tags=["Instruments"], # Swagger UIでグループ化するためのタグ
)

@router.get("/")
async def list_instruments(
    db: AsyncSession = Depends(get_db)
):
    """全ての銘柄情報を取得"""
    repository = InstrumentRepository(db)
    instruments = await repository.select_all_instruments()
    return instruments

@router.post("/")
async def create_instrument():
    pass