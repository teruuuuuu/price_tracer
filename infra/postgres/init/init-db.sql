CREATE TABLE IF NOT EXISTS instruments (
    id SERIAL PRIMARY KEY,

    -- 基本情報
    ticker VARCHAR(20) NOT NULL UNIQUE, -- APIで利用するシンボル (例: '7203.T', 'AAPL', 'JPY=X')
    name VARCHAR(255),                   -- 人間が読むための銘柄名 (例: 'トヨタ自動車', 'Apple Inc.')
    instrument_type VARCHAR(20) NOT NULL, -- 種別 (例: 'STOCK', 'FOREX', 'ETF', 'FUTURE', 'INDEX', 'CRYPTO')
    currency VARCHAR(10),                -- 通貨 (例: 'JPY', 'USD')
    exchange VARCHAR(50),                -- 取引所 (例: 'TYO', 'NMS')
    country VARCHAR(50),                 -- 国 (例: 'Japan', 'United States')
    sector VARCHAR(100)                 -- 業種 (株式の場合)
);

CREATE INDEX IF NOT EXISTS idx_instruments_ticker ON instruments (ticker);
CREATE INDEX IF NOT EXISTS idx_instruments_instrument_type ON instruments (instrument_type);


CREATE TABLE IF NOT EXISTS prices (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    open NUMERIC(12, 4),
    high NUMERIC(12, 4),
    low NUMERIC(12, 4),
    close NUMERIC(12, 4),
    adj_close NUMERIC(12, 4),
    volume BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    -- 銘柄と日付の組み合わせでデータが重複しないようにする制約
    UNIQUE (ticker, date)
);