from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import ENUM
from db.base import Base, CRUDMixin

class Instrument(Base, CRUDMixin):
    __tablename__ = "instruments"

    id = Column(Integer, primary_key=True)
    ticker = Column(String(20), unique=True, nullable=False)
    name = Column(String(255))
    instrument_type = Column(String(20), nullable=False)
    currency = Column(String(10))
    exchange = Column(String(50))
    country = Column(String(50))
    sector = Column(String(100))

    def __repr__(self):
        return f"Instrument(ticker='{self.ticker}', name='{self.name}')"
    
    @classmethod
    def from_yfinance_info(cls, info: dict) -> 'Instrument':
        # 銘柄種別を推定するロジック
        quote_type = info.get('quoteType', '').upper()
        if 'EQUITY' in quote_type:
            instrument_type = 'STOCK'
        elif 'ETF' in quote_type:
            instrument_type = 'ETF'
        else:
            instrument_type = 'UNKNOWN'
            
        # インスタンスを生成し、データをマッピング
        return cls(
            ticker=info.get('symbol'),
            name=info.get('longName') or info.get('shortName'),
            instrument_type=instrument_type,
            currency=info.get('currency'),
            exchange=info.get('exchange'),
            country=info.get('country'),
            sector=info.get('sector')
        )