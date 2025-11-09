import os
import sys
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf
import psycopg2
from psycopg2.extras import execute_values

# プロジェクトのルートディレクトリをPythonパスに追加
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

# --- DB接続情報 (環境変数から取得するのが望ましい) ---
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "price_generator")
DB_USER = os.getenv("POSTGRES_USER", "price_generator")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "price_generator")

def get_db_connection():
    """データベース接続を取得する"""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def fetch_and_save_prices():
    """
    DBからアクティブな銘柄リストを取得し、yfinanceで価格データを取得してDBに保存する
    """
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # 1. アクティブな銘柄を取得
            cur.execute("SELECT ticker FROM instruments WHERE is_active = TRUE;")
            tickers = [row[0] for row in cur.fetchall()]
            print(f"取得対象の銘柄: {tickers}")

            if not tickers:
                print("対象銘柄がありません。処理を終了します。")
                return

            # 2. 各銘柄のデータを取得してDBに保存
            for ticker in tickers:
                print(f"'{ticker}' のデータを取得中...")
                stock = yf.Ticker(ticker)
                # 5年分のデータを取得
                hist = stock.history(period="5y")

                if hist.empty:
                    print(f"'{ticker}' のデータが取得できませんでした。")
                    continue

                # 3. UPSERT (INSERT ... ON CONFLICT) でデータを保存
                data_to_insert = []
                for index, row in hist.iterrows():
                    data_to_insert.append((
                        ticker, index.date(), row['Open'], row['High'],
                        row['Low'], row['Close'], row['Adj Close'], row['Volume']
                    ))

                sql = """
                    INSERT INTO prices (ticker, date, open, high, low, close, adj_close, volume)
                    VALUES %s
                    ON CONFLICT (ticker, date) DO NOTHING;
                """
                execute_values(cur, sql, data_to_insert)
                print(f"'{ticker}' のデータを保存しました。")
        conn.commit()
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print(f"バッチ処理を開始します: {datetime.now()}")
    fetch_and_save_prices()
    print(f"バッチ処理が完了しました: {datetime.now()}")