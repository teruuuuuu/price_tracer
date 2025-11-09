import datetime

last_run_time = None

async def async_scheduled_job():
    last_run_time = datetime.datetime.now()
    """非同期対応のバッチ処理ジョブ"""
    print(f"非同期バッチ処理実行: {datetime.datetime.now()}")
