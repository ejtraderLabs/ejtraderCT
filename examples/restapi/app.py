import os
from pydantic import BaseModel
from fastapi import FastAPI
from ejtraderCT import Ctrader


app = FastAPI()
global api
api = Ctrader(os.getenv("HOST_NAME"), os.getenv("SENDER_COMPID"), os.getenv("PASSWORD"))


class LoginModel(BaseModel):
    server: str
    account: str
    password: str


class SymbolModel(BaseModel):
    symbols: list[str]


class OrderModel(BaseModel):
    symbol: str
    volume: float
    stoploss: float
    takeprofit: float
    price: float = None


class ModifyModel(BaseModel):
    id: str
    stoploss: float
    takeprofit: float
    price: float = None


class IdModel(BaseModel):
    id: str


async def check():
    return api.isconnected()


@app.post("/login")
async def login():
    api = Ctrader(
        os.getenv("HOST_NAME"), os.getenv("SENDER_COMPID"), os.getenv("PASSWORD")
    )
    return {"connected": api.isconnected()}


@app.get("/quote/{symbol}")
async def quote(symbol: str = None):
    if symbol:
        quote = api.quote(symbol)
    else:
        quote = api.quote()
    return quote


@app.post("/buy")
async def buy(order: OrderModel):
    return {
        "Position": api.buy(
            order.symbol, order.volume, order.stoploss, order.takeprofit
        )
    }


@app.post("/sell")
async def sell(order: OrderModel):
    return {
        "Position": api.sell(
            order.symbol, order.volume, order.stoploss, order.takeprofit
        )
    }


@app.post("/buyLimit")
async def buy_limit(order: OrderModel):
    return {"Order": api.buyLimit(order.symbol, order.volume, order.price)}


@app.post("/sellLimit")
async def sell_limit(order: OrderModel):
    return {"Order": api.sellLimit(order.symbol, order.volume, order.price)}


@app.post("/buyStop")
async def buy_stop(order: OrderModel):
    return {"Order": api.buyStop(order.symbol, order.volume, order.price)}


@app.post("/sellStop")
async def sell_stop(order: OrderModel):
    return {"Order": api.sellStop(order.symbol, order.volume, order.price)}


@app.get("/positions")
async def positions():
    return api.positions()


@app.get("/orders")
async def orders():
    return api.orders()


@app.post("/orderCancelById")
async def order_cancel_by_id(id_model: IdModel):
    api.orderCancelById(id_model.id)
    return {"message": "Order cancelled"}


@app.post("/positionCloseById")
async def position_close_by_id(id_model: IdModel):
    api.positionCloseById(id_model.id)
    return {"message": "Position closed"}


@app.post("/cancel_all")
async def cancel_all():
    api.cancel_all()
    return {"message": "All orders cancelled"}


@app.post("/close_all")
async def close_all():
    api.close_all()
    return {"message": "All positions closed"}


@app.post("/logout")
async def logout():
    return {"message": api.logout()}


@app.post("/status")
async def status():
    return {"connected": api.isconnected()}
