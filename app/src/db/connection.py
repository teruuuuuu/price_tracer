import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 環境変数から設定を取得 (os.getenvを使用)
# .envファイルから読み込む場合は、メインの起動スクリプトで load_dotenv() を実行済みであることを前提
USER = os.getenv("POSTGRES_USER", "price_generator")
PASS = os.getenv("POSTGRES_PASSWORD", "price_generator")
DB = os.getenv("POSTGRES_DB", "price_generator")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", "5432")

# PostgreSQLの非同期接続URL
DATABASE_URL = f"postgresql+psycopg://{USER}:{PASS}@{HOST}:{PORT}/{DB}"

# 非同期Engineの作成
# poolclass=NullPool は、FastAPIのライフサイクルで接続プーリングを管理しない場合にシンプル
async_engine = create_async_engine(DATABASE_URL, echo=True)

# 非同期セッションファクトリ
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False, # セッション終了後もオブジェクトの属性アクセスを許可
)



# DBセッションを取得するための依存性注入関数 (FastAPIで利用)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

