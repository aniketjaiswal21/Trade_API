import datetime as dt
import random
from typing import Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


# Mock database interaction layer and generate random trade data
def generate_random_trade():
    trade_id = str(random.randint(1, 100))
    asset_class = random.choice(["Equity", "Bond", "FX"])
    counterparty = random.choice(["ABC Corp", "XYZ Corp", "DEF Corp"])
    instrument_id = random.choice(["AAPL", "TSLA", "AMZN", "GOOGL"])
    instrument_name = random.choice(["Apple Inc.", "Tesla Inc.", "Amazon.com Inc.", "Alphabet Inc."])
    trade_date_time = dt.datetime.now()
    buy_sell_indicator = random.choice(["BUY", "SELL"])
    price = round(random.uniform(1.0, 1000.0), 2)
    quantity = random.randint(1, 100)
    trader = random.choice(["John Doe", "Jane Smith", "Michael Brown"])

    return {
        "trade_id": trade_id,
        "asset_class": asset_class,
        "counterparty": counterparty,
        "instrument_id": instrument_id,
        "instrument_name": instrument_name,
        "trade_date_time": trade_date_time,
        "trade_details": {
            "buySellIndicator": buy_sell_indicator,
            "price": price,
            "quantity": quantity
        },
        "trader": trader
    }


mocked_db = [generate_random_trade() for _ in range(20)]


class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")


@app.get("/trades/{trade_id}")
def get_trade_by_id(trade_id: str):
    trade = next((trade for trade in mocked_db if trade["trade_id"] == trade_id), None)
    if trade:
        return trade
    else:
        return {"error": "Trade not found"}


@app.get("/trades")
def get_trades(
    search: Optional[str] = Query(None, description="Search query parameter"),
    assetClass: Optional[str] = None,
    end: Optional[dt.datetime] = None,
    maxPrice: Optional[float] = None,
    minPrice: Optional[float] = None,
    start: Optional[dt.datetime] = None,
    tradeType: Optional[str] = None,
    page: Optional[int] = Query(1, gt=0),
    limit: Optional[int] = Query(10, gt=0),
    sort: Optional[str] = None
):
    filtered_trades = mocked_db

    # Apply search query
    if search:
        search_terms = search.split()
        filtered_trades = [
            trade
            for trade in filtered_trades
            for term in search_terms
            if (
                term.lower() in trade["counterparty"].lower()
                or term.lower() in trade["instrument_id"].lower()
                or term.lower() in trade["instrument_name"].lower()
                or term.lower() in trade["trader"].lower()
            )
        ]

    # Apply filters
    if assetClass:
        filtered_trades = [trade for trade in filtered_trades if trade["asset_class"] == assetClass]

    if end:
        filtered_trades = [trade for trade in filtered_trades if trade["trade_date_time"] <= end]

    if maxPrice:
        filtered_trades = [trade for trade in filtered_trades if trade["trade_details"]["price"] <= maxPrice]

    if minPrice:
        filtered_trades = [trade for trade in filtered_trades if trade["trade_details"]["price"] >= minPrice]

    if start:
        filtered_trades = [trade for trade in filtered_trades if trade["trade_date_time"] >= start]

    if tradeType:
        filtered_trades = [trade for trade in filtered_trades if trade["trade_details"]["buySellIndicator"] == tradeType]

    # Apply sorting
    if sort:
        reverse = False
        if sort.startswith("-"):
            reverse = True
            sort = sort[1:]
        filtered_trades = sorted(filtered_trades, key=lambda trade: trade.get(sort, ""), reverse=reverse)

    # Apply pagination
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_trades = filtered_trades[start_index:end_index]

    return paginated_trades



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
