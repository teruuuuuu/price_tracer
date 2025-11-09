from sqlalchemy.orm import DeclarativeBase

# Baseクラス（モデル定義の基底クラス）
class Base(DeclarativeBase):
    pass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import DeclarativeBase # Baseクラスの型ヒント用
from typing import List, TypeVar, Type

# 型ヒントのためにジェネリック型を定義
T = TypeVar('T', bound='CRUDMixin')

class CRUDMixin:

    @classmethod
    async def select_all(cls: Type[T], db: AsyncSession) -> List[T]:
        """
        現在のモデルクラス (cls) の全てのレコードを取得する
        """
        # 1. SELECT文の構築: select(cls) は "SELECT * FROM <table>" に相当
        stmt = select(cls) 
        
        # 2. クエリの実行: db.scalars() は結果セットからモデルインスタンス（スカラー値）のみを抽出
        result = await db.scalars(stmt)
        
        # 3. 結果をリストとして全て取得
        return result.all()
    

    @classmethod
    async def upsert(cls: Type[T], db: AsyncSession, instance: T, conflict_keys: list = None):
        """
        PostgreSQLのUPSERTを実行する。instanceはモデルのインスタンスである必要がある。
        """
        if not conflict_keys:
             raise ValueError("conflict_keys must be provided for UPSERT.")
            
        # 💡 挿入する値: インスタンスの辞書表現からデータを取得
        values_to_insert = instance.__dict__
        
        # 内部の '_sa_instance_state' などSQLAlchemy内部のキーをクリーンアップ
        values_to_insert = {k: v for k, v in values_to_insert.items() if not k.startswith('_')}
        
        insert_stmt = insert(cls).values(**values_to_insert)

        update_mapping = {
            col.name: getattr(insert_stmt.excluded, col.name)
            for col in cls.__table__.columns
            if col.name not in ('id', 'created_at', 'updated_at')
        }
        
        on_conflict_stmt = insert_stmt.on_conflict_do_update(
            index_elements=conflict_keys,
            set_=update_mapping
        )

        await db.execute(on_conflict_stmt)
        return True # コミットはサービス層に任せる


    # @classmethod
    # async def upsert(cls, db: AsyncSession, data: dict, conflict_keys: list = None):
    #     """
    #     PostgreSQLのINSERT...ON CONFLICT UPDATE (UPSERT) を実行する。
    #     cls は呼び出し元のモデルクラス (例: Instrument) を指す。
    #     """
    #     if not conflict_keys:
    #         # 衝突キーが指定されていない場合は、PRIMARY KEYまたはUNIQUE制約のキーを推定する必要がある
    #         # 簡略化のため、ここでは呼び出し側で'ticker'などを明示することを推奨
    #         raise ValueError("conflict_keys must be provided for UPSERT.")
            
    #     # 挿入する値
    #     insert_stmt = insert(cls).values(**data)

    #     # 衝突した場合に更新するカラムを設定
    #     # 挿入されたデータ(insert_stmt.excluded)から値を取得して更新
    #     # idやcreated_atは更新対象から除外
    #     update_mapping = {
    #         col.name: getattr(insert_stmt.excluded, col.name)
    #         for col in cls.__table__.columns
    #         if col.name not in ('id', 'created_at', 'updated_at')
    #     }
        
    #     # ON CONFLICT DO UPDATE の構築
    #     on_conflict_stmt = insert_stmt.on_conflict_do_update(
    #         index_elements=conflict_keys,
    #         set_=update_mapping
    #     )

    #     await db.execute(on_conflict_stmt)
    #     await db.commit()
    #     return True