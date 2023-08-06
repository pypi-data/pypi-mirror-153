import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, BigInteger
from pagexdata.database import Base
from pydantic import BaseModel
from typing import Optional


class RedditHits(Base):
    __tablename__ = 'reddit_hits'

    datetime = Column(DateTime, primary_key=True)
    ticker_symbol = Column(String, primary_key=True)
    subreddit = Column(String, primary_key=True)
    hits = Column(Integer)
    positive_hits = Column(Boolean)
    rank = Column(Integer, nullable=True)
    previous_rank = Column(Integer, nullable=True)
    change_rank = Column(Integer, nullable=True)
    change_hits_one_day = Column(Integer, nullable=True)
    change_hits_two_days = Column(Integer, nullable=True)
    change_hits_three_days = Column(Integer, nullable=True)
    change_hits_one_week = Column(Integer, nullable=True)
    change_hits_two_weeks = Column(Integer, nullable=True)
    change_hits_four_weeks = Column(Integer, nullable=True)
    hits_volatility_one_week = Column(Float, nullable=True)
    hits_volatility_two_weeks = Column(Float, nullable=True)


class StockData(Base):
    __tablename__ = 'stockdata'

    datetime = Column(DateTime, primary_key=True)
    ticker_symbol = Column(String, primary_key=True)  # symbol
    price = Column(Float)  # regularMarketPrice
    volume = Column(BigInteger)  # regularMarketVolume
    averageDailyVolume10Day = Column(BigInteger, nullable=True)  # averageDailyVolume10Day
    averageDailyVolume3Month = Column(BigInteger, nullable=True)  # averageDailyVolume3Month
    bookValue = Column(Float, nullable=True)  # https://www.investopedia.com/articles/investing/110613/market-value-versus-book-value.asp
    currency = Column(String, nullable=True)
    displayName = Column(String, nullable=True)
    epsTrailingTwelveMonths = Column(Float, nullable=True)  # https://www.investopedia.com/ask/answers/070114/what-formula-calculating-earnings-share-eps.asp
    epsCurrentYear = Column(Float, nullable=True)  # https://www.investopedia.com/terms/e/eps.asp
    epsForward = Column(Float, nullable=True)  # https://www.investopedia.com/ask/answers/070114/what-formula-calculating-earnings-share-eps.asp
    priceEpsCurrentYear = Column(Float, nullable=True)  # https://www.investopedia.com/terms/p/price-earningsratio.asp
    trailingPE = Column(Float, nullable=True)  # https://www.investopedia.com/terms/t/trailingpe.asp
    forwardPE = Column(Float, nullable=True)  # https://www.investopedia.com/terms/f/forwardpe.asp
    esgPopulated = Column(Boolean, nullable=True)  # https://finance.yahoo.com/news/esg-investing-135435590.html
    fiftyDayAverage = Column(Float, nullable=True)  # SMA?
    fiftyDayAverageChange = Column(Float, nullable=True)  # SMA change?
    fiftyDayAverageChangePercent = Column(Float, nullable=True)  # SMA change percent?
    twoHundredDayAverage = Column(Float, nullable=True)  # SMA?
    twoHundredDayAverageChange = Column(Float, nullable=True)  # SMA change?
    twoHundredDayAverageChangePercent = Column(Float, nullable=True)  # SMA change percent?
    fiftyTwoWeekHigh = Column(Float, nullable=True)
    fiftyTwoWeekHighChange = Column(Float, nullable=True)
    fiftyTwoWeekHighChangePercent = Column(Float, nullable=True)
    fiftyTwoWeekLow = Column(Float, nullable=True)
    fiftyTwoWeekLowChange = Column(Float, nullable=True)
    fiftyTwoWeekLowChangePercent = Column(Float, nullable=True)
    fiftyTwoWeekRange = Column(String, nullable=True)
    longName = Column(String, nullable=True)
    market = Column(String, nullable=True)
    marketCap = Column(BigInteger, nullable=True)  # https://www.investopedia.com/investing/market-capitalization-defined/
    priceToBook = Column(Float, nullable=True)  # https://www.investopedia.com/investing/using-price-to-book-ratio-evaluate-companies/
    quoteType = Column(String, nullable=True)
    region = Column(String, nullable=True)
    regularMarketChange = Column(Float, nullable=True)
    regularMarketChangePercent = Column(Float, nullable=True)
    regularMarketDayHigh = Column(Float, nullable=True)
    regularMarketDayLow = Column(Float, nullable=True)
    regularMarketDayRange = Column(String, nullable=True)
    regularMarketOpen = Column(Float, nullable=True)
    regularMarketPreviousClose = Column(Float, nullable=True)
    sharesOutstanding = Column(BigInteger, nullable=True)  # https://www.investopedia.com/terms/o/outstandingshares.asp
    trailingAnnualDividendRate = Column(Float, nullable=True)  # https://www.investopedia.com/terms/d/dividendyield.asp
    trailingAnnualDividendYield = Column(Float, nullable=True)  # https://www.investopedia.com/terms/d/dividendyield.asp


class ImportLog(Base):
    __tablename__ = 'importlog'

    log_datetime = Column(DateTime, primary_key=True)
    type = Column(String, primary_key=True)
    trigger_type = Column(String)
    state = Column(String)
    import_time = Column(DateTime, nullable=False)
    message = Column(String, nullable=True)
    extra = Column(String, nullable=True)
    calculated = Column(Boolean, nullable=False)


# pagination entities for rest api
class RedditHitsPage(BaseModel):
    datetime: datetime.datetime
    ticker_symbol: str
    subreddit: str
    hits: int
    rank: Optional[int] = None
    previous_rank: Optional[int] = None
    change_rank: Optional[int] = None
    change_hits_one_day: Optional[int] = None
    change_hits_two_days: Optional[int] = None
    change_hits_three_days: Optional[int] = None
    change_hits_one_week: Optional[int] = None
    change_hits_two_weeks: Optional[int] = None
    change_hits_four_weeks: Optional[int] = None
    hits_volatility_one_week: Optional[float] = None
    hits_volatility_two_weeks: Optional[float] = None

    class Config:
        orm_mode = True


class StockDataPage(BaseModel):
    datetime: datetime.datetime
    ticker_symbol: str  # symbol
    price: Optional[float]  # regularMarketPrice
    volume: Optional[int]  # regularMarketVolume
    averageDailyVolume10Day: Optional[int]  # averageDailyVolume10Day
    averageDailyVolume3Month: Optional[int]  # averageDailyVolume3Month
    bookValue: Optional[float]  # https://www.investopedia.com/articles/investing/110613/market-value-versus-book-value.asp
    currency: Optional[str]
    displayName: Optional[str]
    epsTrailingTwelveMonths: Optional[float]  # https://www.investopedia.com/ask/answers/070114/what-formula-calculating-earnings-share-eps.asp
    epsCurrentYear: Optional[float]  # https://www.investopedia.com/terms/e/eps.asp
    epsForward: Optional[float]  # https://www.investopedia.com/ask/answers/070114/what-formula-calculating-earnings-share-eps.asp
    priceEpsCurrentYear: Optional[float]  # https://www.investopedia.com/terms/p/price-earningsratio.asp
    trailingPE: Optional[float]  # https://www.investopedia.com/terms/t/trailingpe.asp
    forwardPE: Optional[float]  # https://www.investopedia.com/terms/f/forwardpe.asp
    esgPopulated: Optional[bool]  # https://finance.yahoo.com/news/esg-investing-135435590.html
    fiftyDayAverage: Optional[float]  # SMA?
    fiftyDayAverageChange: Optional[float]  # SMA change?
    fiftyDayAverageChangePercent: Optional[float]  # SMA change percent?
    twoHundredDayAverage: Optional[float]  # SMA?
    twoHundredDayAverageChange: Optional[float]  # SMA change?
    twoHundredDayAverageChangePercent: Optional[float]  # SMA change percent?
    fiftyTwoWeekHigh: Optional[float]
    fiftyTwoWeekHighChange: Optional[float]
    fiftyTwoWeekHighChangePercent: Optional[float]
    fiftyTwoWeekLow: Optional[float]
    fiftyTwoWeekLowChange: Optional[float]
    fiftyTwoWeekLowChangePercent: Optional[float]
    fiftyTwoWeekRange: Optional[str]
    longName: Optional[str]
    market: Optional[str]
    marketCap: Optional[int]  # https://www.investopedia.com/investing/market-capitalization-defined/
    priceToBook: Optional[float]  # https://www.investopedia.com/investing/using-price-to-book-ratio-evaluate-companies/
    quoteType: Optional[str]
    region: Optional[str]
    regularMarketChange: Optional[float]
    regularMarketChangePercent: Optional[float]
    regularMarketDayHigh: Optional[float]
    regularMarketDayLow: Optional[float]
    regularMarketDayRange: Optional[str]
    regularMarketOpen: Optional[float]
    regularMarketPreviousClose: Optional[float]
    sharesOutstanding: Optional[int]  # https://www.investopedia.com/terms/o/outstandingshares.asp
    trailingAnnualDividendRate: Optional[float]  # https://www.investopedia.com/terms/d/dividendyield.asp
    trailingAnnualDividendYield: Optional[float]  # https://www.investopedia.com/terms/d/dividendyield.asp

    class Config:
        orm_mode = True


class ImportLogPage(BaseModel):
    log_datetime: datetime.datetime
    type: str
    trigger_type: str
    state: str
    import_time: datetime.datetime
    message: Optional[str] = None
    extra: Optional[str] = None
    calculated: bool

    class Config:
        orm_mode = True
