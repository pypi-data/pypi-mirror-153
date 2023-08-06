# -*- coding: utf-8 -*-
import importlib,pdb,itertools
from threading import Lock
from enum import Enum
import pandas as pd
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.event import EVENT_LOG,EVENT_CONTRACT,EVENT_TICK,\
                    EVENT_ORDER,EVENT_POSITION,EVENT_TRADE,EVENT_ACCOUNT
from vnpy.trader.constant import Direction, Exchange, Interval, Offset, Status
from jdw.kdutils.logger import kd_logger
from jdw.mfc.anode.axtell import Axtell

INACTIVE_STATUSES = set([Status.CANCELLED, Status.REJECTED])

EMPTY_STRING = ""
EMPTY_INT = 0

### 持仓缓存信息
class PositionBuffer(object):
    def __init__(self):
        self.vtSymbol = EMPTY_STRING

        # 多头
        self.longPosition = EMPTY_INT
        self.longToday = EMPTY_INT
        self.longYd = EMPTY_INT
        self.longFrozen = EMPTY_INT
        self.longOpen = EMPTY_INT

        # 空头
        self.shortPosition = EMPTY_INT
        self.shortToday = EMPTY_INT
        self.shortYd = EMPTY_INT
        self.shortFrozen = EMPTY_INT
        self.shortOpen = EMPTY_INT

    def updatePositionData(self, pos):
        """更新持仓数据"""
        if pos.direction == Direction.LONG:
            self.longPosition = pos.volume
            self.longYd = pos.yd_volume
            self.longToday = self.longPosition - self.longYd
            #self.longFrozen = pos.frozen
        else:
            self.shortPosition = pos.volume
            self.shortYd = pos.yd_volume
            self.shortToday = self.shortPosition - self.shortYd

    def updateTradeData(self, trade):
        """更新成交数据"""
        if trade.direction == Direction.LONG:
            # 多方开仓，则对应多头的持仓和今仓增加
            if trade.offset == Offset.OPEN:
                self.longPosition += trade.volume
                self.longToday += trade.volume
                self.longOpen += trade.volume
            # 多方平今，对应空头的持仓和今仓减少
            elif trade.offset == Offset.CLOSETODAY:
                self.shortPosition -= trade.volume
                self.shortToday -= trade.volume
                self.shortFrozen -= trade.volume
                if self.shortFrozen < 0:
                    self.shortFrozen = 0
            # 多方平昨，对应空头的持仓和昨仓减少
            else:
                self.shortPosition -= trade.volume
                self.shortYd -= trade.volume
                self.shortFrozen -= trade.volume
                if self.shortFrozen < 0:
                    self.shortFrozen = 0
        else:
            # 空头和多头相同
            if trade.offset == Offset.OPEN:
                self.shortPosition += trade.volume
                self.shortToday += trade.volume
                self.shortOpen += trade.volume
            elif trade.offset == Offset.CLOSETODAY:
                self.longPosition -= trade.volume
                self.longToday -= trade.volume
                self.longFrozen -= trade.volume
                if self.longFrozen < 0:
                    self.longFrozen = 0
            else:
                self.longPosition -= trade.volume
                self.longYd -= trade.volume
                self.longFrozen -= trade.volume
                if self.longFrozen < 0:
                    self.longFrozen = 0

class STATE(Enum):
    INIT = 0
    LOGIN_ON = 1
    CONTRACT = 2
    MARKET_TICK = 3
    POSITION = 4

### 适配引擎
class Conor(object):
    def __init__(self, name='ctp'):
        self._name = name
        self._account_id = None
        self._event_engine = EventEngine()
        self._event_engine.register(EVENT_LOG, self.process_log_event)
        self._event_engine.register(EVENT_TICK, self.process_tick)
        self._event_engine.register(EVENT_ORDER, self.process_order)
        self._event_engine.register(EVENT_POSITION, self.process_position)
        self._event_engine.register(EVENT_TRADE, self.process_trade)
        self._event_engine.register(EVENT_ACCOUNT, self.process_account)
        self._event_engine.register(EVENT_CONTRACT, self.process_contract)


        self._main_engine = MainEngine(self._event_engine)
        module_name = "vnpy_{0}".format(self._name)
        self._market_data = {}
        self._order_list = {}
        try:
            module_class = importlib.import_module(module_name)
            getway_name = "{0}Gateway".format(self._name.capitalize())
            getway_module = module_class.__getattribute__(getway_name)
        except ImportError as e:
            raise(str(e))
            return
        self._main_engine.add_gateway(getway_module)
        self._trader_engine = self._main_engine.add_engine(Axtell)
        self._pos_buffer = {}
        self._listener_callback = {}

        self._state_lock = Lock()
        self._state_list = {STATE.INIT} ##  状态机

    @property
    def account_id(self):
        return self._account_id

    def check_state(self, state):
        with self._state_lock:
            if state in self._state_list:
                return True
        return False


    def listener(self, code, callback):
        self._listener_callback[code] = callback

    def process_log_event(self, event):
        log = event.data
        print(f"{log.time}\t{log.msg}")

    def process_account(self, event):
        with self._state_lock:
            if STATE.LOGIN_ON not in self._state_list:
                self._state_list.add(STATE.LOGIN_ON)
                kd_logger.info("account {0} {1} login on".format(
                    event.data.gateway_name, event.data.accountid))

    def process_order(self, event):
        order_id = event.data.gateway_name + '.' + event.data.orderid
        self._order_list[order_id] = event.data
        if 'order' in self._listener_callback:
            self._listener_callback['order'](event.data)

    def process_tick(self, event):
        with self._state_lock:
            if STATE.MARKET_TICK not in self._state_list:
                self._state_list.add(STATE.MARKET_TICK)
        self._market_data[event.data.symbol] = event.data

    def process_position(self, event):
        with self._state_lock:
            if STATE.POSITION not in self._state_list:
                self._state_list.add(STATE.POSITION)
        pos = event.data
        # 更新持仓缓存数据
        vtSymbol = pos.symbol + '.' + pos.exchange.value
        posBuffer = self._pos_buffer.get(vtSymbol, None)
        if not posBuffer:
            posBuffer = PositionBuffer()
            posBuffer.vtSymbol = vtSymbol#.lower()
            self._pos_buffer[vtSymbol] = posBuffer
        posBuffer.updatePositionData(pos)
        if 'positon' in self._listener_callback:
            self._listener_callback['positon'](event.data)

    def process_trade(self, event):
        trade = event.data
        # 更新持仓缓存数据
        vtSymbol = trade.symbol + '.' + trade.exchange.value
        posBuffer = self._pos_buffer.get(vtSymbol, None)
        if not posBuffer:
            posBuffer = PositionBuffer()
            posBuffer.vtSymbol = vtSymbol
            self._pos_buffer[vtSymbol] = posBuffer
        posBuffer.updateTradeData(trade)
        if 'trade' in self._listener_callback:
            self._listener_callback['trade'](event.data)

    def process_contract(self, event):
        with self._state_lock:
            if STATE.CONTRACT not in self._state_list:
                self._state_list.add(STATE.CONTRACT)

    def _create_config(self, **kwargs):
        config = {}
        config["用户名"] = kwargs['account_id']
        config["密码"] = kwargs['password']
        config["经纪商代码"] = kwargs['broker_id']
        config["交易服务器"] = kwargs['td_address']
        config["行情服务器"] = kwargs['md_address']
        config["产品名称"] = kwargs['app_id']
        config["授权编码"] = kwargs['auth_code']
        return config

    def start(self, **kwargs):
        if 'account_id' in kwargs:
            self._account_id = kwargs['account_id']
        config = self._create_config(**kwargs)
        self._trader_engine.connect_gateway(config, self._name.upper())

    def contract(self, symbol):
        self._trader_engine.contract(symbol)

    def subscribe(self, symbol):
        self._trader_engine.subscribe(symbol)

    def buy(self, vt_symbol, price, volume): ###  开多仓
        return self._trader_engine.buy(vt_symbol, price, volume)

    def sell(self, vt_symbol, price, volume): ### 平多仓
        if 'SHFE' in vt_symbol: ### 判断今仓和昨仓
            order_ref = []
            posBuffer = self._pos_buffer.get(vt_symbol, None)
            if posBuffer.longYd - posBuffer.longFrozen >= volume:
                self._pos_buffer[vt_symbol].longFrozen += volume
                order_ids = []#self._trader_engine.sell(vt_symbol, price, volume)
                order_ref.append(order_ids)
            else:
                if (posBuffer.longYd - posBuffer.longFrozen) > 0:
                    req_volume = posBuffer.longYd - posBuffer.longFrozen
                    volume -= req_volume
                    self._pos_buffer[vt_symbol].longFrozen += req_volume
                    order_ids = []#self._trader_engine.sell(vt_symbol, price, req_volume)
                    order_ref.append(order_ids)
                order_ids = self._trader_engine.sell_today(vt_symbol, price, volume)
                order_ref.append(order_ids)
            return list(itertools.chain.from_iterable(order_ref))
        return self._trader_engine.sell(vt_symbol, price, volume)

    def short(self, vt_symbol, price, volume): ### 开空仓
        return self._trader_engine.short(vt_symbol, price, volume)

    def cover(self, vt_symbol, price, volume): ### 平空仓
        if 'SHFE' in vt_symbol: ### 判断今仓和昨仓
            order_ref = []
            posBuffer = self._pos_buffer.get(vt_symbol, None)
            if (posBuffer.shortYd - posBuffer.shortFrozen) >= volume:
                self._pos_buffer[vt_symbol].shortFrozen += volume
                order_ids = self._trader_engine.cover(vt_symbol, price, volume)
                order_ref.append(order_ids)
            else:
                if (posBuffer.shortYd - posBuffer.shortFrozen) > 0:
                    req_volume = posBuffer.shortYd - posBuffer.shortFrozen
                    volume -= req_volume
                    self._pos_buffer[vt_symbol].shortFrozen += req_volume
                    order_ids = self._trader_engine.cover(vt_symbol, price, req_volume)
                    order_ref.append(order_ids)
                order_ids = self._trader_engine.cover_today(vt_symbol, price, volume)
                order_ref.append(order_ids)
            return list(itertools.chain.from_iterable(order_ref))
        return self._trader_engine.cover(vt_symbol, price, volume)

    def sell_yesterday(self,vt_symbol, price,volume): ### 平昨多仓
        return self._trader_engine.sell_yesterday(vt_symbol, price, volume)

    def cover_yesterday(self, vt_symbol, price, volume): ### 平昨空仓
        return self._trader_engine.cover_yesterday(vt_symbol, price, volume)

    def sell_today(self,vt_symbol, price,volume): ### 平今多仓
        return self._trader_engine.sell_today(vt_symbol, price, volume)

    def cover_today(self, vt_symbol, price, volume): ### 平今空仓
        return self._trader_engine.cover_today(vt_symbol, price, volume)

    def cancel_order(self, symbol, order_id):
        return self._trader_engine.cancel_order(symbol, order_id)


    def get_all_contracts(self, use_df=False):
        """"""
        return self._trader_engine.get_all_contracts(use_df)

    def get_account(self, vt_accountid: str, use_df: bool = False):
        """"""
        return self._trader_engine.get_account(vt_accountid, use_df)

    def get_all_accounts(self, use_df: bool = False):
        """"""
        return self._trader_engine.get_all_accounts(use_df=use_df)

    def get_all_positions(self, use_df: bool = False):
        """"""
        return self._trader_engine.get_all_positions(use_df=use_df)

    def get_tick(self, vt_symbol, use_df=False):
        return self._trader_engine.get_tick(vt_symbol=vt_symbol, use_df=use_df)

    def get_ticks(self, symbols, columns=None):
        cols = ['symbol','exchange','last_price',
                    'bid_price_1','ask_price_1'] if columns is None else columns
        market_data = pd.DataFrame(list(self._market_data.values()))
        if market_data.empty:
            return market_data
        market_data = market_data.set_index('symbol').loc[symbols].reset_index()
        return market_data[cols]