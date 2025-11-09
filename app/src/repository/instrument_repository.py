from sqlalchemy.ext.asyncio import AsyncSession
from model.instrument import Instrument


class InstrumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # 💡 data: dict を instance: Instrument に変更
    async def update_or_create_instrument(self, instance: Instrument):
        """
        Instrumentインスタンスを受け取り、トランザクション内でUPSERTを実行
        """
        try:
            # 💡 モデルインスタンスをCRUDMixinのメソッドに渡す
            await Instrument.upsert(
                db=self.db, 
                instance=instance, # ← インスタンスを渡す
                conflict_keys=['ticker']
            )
            
            await self.db.commit()
            return {"status": "success", "ticker": instance.ticker}

        except Exception as e:
            await self.db.rollback()
            print(f"Transaction failed for {instance.ticker}: {e}")
            raise e
    
    async def select_all_instruments(self) -> list[Instrument]:
        return await Instrument.select_all(self.db)