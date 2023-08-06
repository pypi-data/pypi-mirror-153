# -*- coding: utf-8 -*-
import bisect
import threading
import time
import datetime
import ssl
from collections import defaultdict

from rqdatac.services.basic import instruments, get_previous_trading_date
from rqdatac.services.live import current_minute
from rqdatac.validators import ensure_list_of_string
from rqdatac.decorators import export_as_api, retry, ttl_cache
from rqdatac.utils import datetime_to_int14, int8_to_date
from rqdatac.client import get_client
from rqdatac.share.errors import PermissionDenied

try:
    from orjson import dumps as json_dumps, loads as json_loads
except ImportError:
    try:
        import rapidjson as json
    except ImportError:
        import json

    def json_dumps(*args, **kwargs):
        return json.dumps(*args, **kwargs).encode('utf-8')

    def json_loads(*args, **kwargs):
        return json.loads(*args, **kwargs)


def str_to_dt_time(s):
    """ '21:31' -->  datetime.time(21, 31) """
    return datetime.time(int(s[0:2]), int(s[3:5]))


@ttl_cache(1800)
def to_trading_periods(trading_hours, date):
    trading_hours = [t.split("-", 1) for t in trading_hours.split(",")]
    for i, (start, end) in enumerate(trading_hours):
        trading_hours[i][0] = str_to_dt_time(start)
        trading_hours[i][1] = str_to_dt_time(end)

    td = int8_to_date(date)
    prev_td = get_previous_trading_date(date)
    prev_td_next = prev_td + datetime.timedelta(days=1)

    for i, (start, end) in enumerate(trading_hours):
        if start.hour > 16:
            start_dt = prev_td
            end_dt = start_dt if end.hour > 16 else prev_td_next
        else:
            start_dt = end_dt = td
        trading_hours[i][0] = datetime.datetime.combine(start_dt, start)
        trading_hours[i][1] = datetime.datetime.combine(end_dt, end)

    return trading_hours


def get_trading_minutes(order_book_id, trading_date):
    result = []
    delta = datetime.timedelta(minutes=1)
    for start, end in to_trading_periods(instruments(order_book_id).trading_hours, trading_date):
        dt = start
        while dt <= end:
            result.append(dt)
            dt += delta
    return result


def futures_resample_dts(trading_minutes, freq):
    delta = datetime.timedelta(minutes=freq)
    dt = trading_minutes[0] - datetime.timedelta(minutes=1) + delta
    dts = set()
    while dt <= trading_minutes[-1]:
        dts.add(trading_minutes[bisect.bisect_right(trading_minutes, dt) - 1])
        dt += delta
    if trading_minutes[-1] not in dts:
        dts.add(trading_minutes[-1])
    return sorted(dts)


class MinbarResampler:
    def __init__(self, order_book_id, freq):
        self.order_book_id = order_book_id
        self.freq = freq
        self._current_bar = None
        self._max_bar_dt = None
        self._bar_dts = None
        self.channel = 'bar_' + order_book_id + '_' + str(freq) + 'm'

    def get_bar_from_rqdatac(self, dt):
        try:
            current_bar = current_minute(self.order_book_id)
        except PermissionDenied:
            return

        if current_bar is None:
            return
        fields = current_bar.columns.tolist()
        fields = list(set(fields).union({'limit_up', 'limit_down', 'trading_date'}))
        bars = get_client().execute('get_today_minbar', [self.order_book_id], fields, self.freq, market='cn')
        if not bars:
            return
        ob, data = bars[0]
        try:
            index = data['datetime'].index(dt)
        except ValueError:
            return

        bar = {k: v[index] for k, v in data.items()}
        bar['order_book_id'] = ob
        bar['action'] = 'feed'
        return bar

    def reset(self):
        self._current_bar = None

    def enqueue(self, bar):
        dt = bar['datetime']
        if self._max_bar_dt is None or dt > self._max_bar_dt:
            trading_minutes = get_trading_minutes(self.order_book_id, bar['trading_date'])
            ins = instruments(self.order_book_id)
            if ins.type in ('Future', 'Option', 'Spot') and ins.exchange not in ("CFFEX", "CCFX", 'XSHG', 'XSHE'):
                bar_dts = futures_resample_dts(trading_minutes, self.freq)
            elif len(trading_minutes) % self.freq == 0:
                bar_dts = trading_minutes[self.freq-1::self.freq]
            else:
                bar_dts = trading_minutes[self.freq-1::self.freq] + trading_minutes[-1:]

            bar_dts = [datetime_to_int14(dt) for dt in bar_dts]
            self._bar_dts = set(bar_dts)
            self._max_bar_dt = bar_dts[-1]
            trading_minutes = [datetime_to_int14(dt) for dt in trading_minutes]

            if dt == trading_minutes[0] or trading_minutes[trading_minutes.index(dt) - 1] in self._bar_dts:
                self._current_bar = bar.copy()
                return

        if dt in self._bar_dts:
            if self._current_bar is not None:
                self._update_current_bar(bar)
                bar, self._current_bar = self._current_bar, {}
                bar['channel'] = self.channel
                return bar
            else:
                self._current_bar = {}

        if self._current_bar is not None:
            self._update_current_bar(bar)

    def _update_current_bar(self, bar):
        for k, v in bar.items():
            if k in ('volume', 'total_turnover', 'num_trades'):
                self._current_bar[k] = self._current_bar.get(k, 0) + v
            elif k == 'open':
                if 'open' not in self._current_bar:
                    self._current_bar['open'] = v
            elif k == 'low':
                if 'low' not in self._current_bar or self._current_bar['low'] > v:
                    self._current_bar['low'] = v
            elif k == 'high':
                if 'high' not in self._current_bar or self._current_bar['high'] < v:
                    self._current_bar['high'] = v
            else:
                self._current_bar[k] = v


@export_as_api
class LiveMarketDataClient:
    def __init__(self, ws_server_uri="wss://rqdata.ricequant.com/live_md"):
        """websocket对象初始化

        :param ws_server_uri: websocket服务地址, 如 wss://rqdata.ricequant.com/live_md

        """
        self._info = None
        self._client = None
        self._ws_server_uri = ws_server_uri
        self._subscribed = set()
        self._init_websocket_client()
        self._resamplers = defaultdict(dict)
        self._subscribed_by_user = set()
        self._closed = False

    def _init_websocket_client(self):
        _token = get_client().execute(
            "user.get_live_md_auth_token",
        )

        try:
            import websocket
        except ImportError:
            raise ImportError(
                "LiveMarketDataClient requires websocket-client package; run 'pip install websocket-client' to fix.")

        login_data = {
            "action": "auth_by_token",
            "token": _token
        }
        _websocket_client = websocket.WebSocket()
        self._client = _websocket_client
        retry(suppress_exceptions=(websocket.WebSocketException,), count=3)(self._websocket_login)(login_data)

    def _websocket_login(self, login_data):
        try:
            self._client.connect(self._ws_server_uri)
        except ssl.SSLCertVerificationError:
            self._client.sock_opt.sslopt = {"cert_reqs": ssl.CERT_NONE}
            self._client.connect(self._ws_server_uri)
        self._client.send(json_dumps(login_data))
        res = self._client.recv()
        self._info = json_loads(res)

    @property
    def info(self):
        return self._info

    def close(self):
        self._closed = True
        try:
            self._client.close()
        except:
            pass

    def subscribe(self, channels):
        """订阅实时行情

        :param channels: 订阅的标的列表 分钟和tick分别以 bar_ 和tick_开头 以平安银行为例，
            subscribe('bar_000001.XSHE')  # 订阅分钟线的实时行情
            subscribe('bar_AU2112_15m')   # 订阅15分钟线的实时行情
            subscribe('tick_000001.XSHE')  # 订阅tick的实时行情
            可以同时订阅多支标的 subscribe(['bar_000001.XSHE'， 'bar_000002.XSHE')

        """
        if self._closed:
            raise RuntimeError('this connection is closed.')

        channels = ensure_list_of_string(channels)
        to_subscribe = []
        for ch in channels:
            self._subscribed_by_user.add(ch)

            if ch.startswith('bar_') and ch.endswith('m'):
                _, order_book_id, freq = ch.split('_')
                to_subscribe.append('bar_' + order_book_id)
                resampler = MinbarResampler(order_book_id, int(freq[:-1]))
                if resampler.channel not in self._resamplers['bar_' + order_book_id]:
                    self._resamplers['bar_' + order_book_id][resampler.channel] = resampler
            else:
                to_subscribe.append(ch)

        data = {
            "action": "subscribe",
            "channels": to_subscribe,
        }
        self._client.send(json_dumps(data))

    def unsubscribe(self, channels):
        """取消订阅实时行情

        :param channels: 取消订阅的标的列表 分钟和tick分别以 bar_ 和tick_开头 以平安银行为例，
            unsubscribe('bar_000001.XSHE')  # 订阅分钟线的实时行情
            unsubscribe('tick_000001.XSHE')  # 订阅tick的实时行情

        """
        if self._closed:
            raise RuntimeError('this connection is closed.')

        channels = ensure_list_of_string(channels)
        for ch in channels:
            self._subscribed_by_user.discard(ch)
            if ch.startswith('bar_') and ch.endswith('m'):
                _, order_book_id, freq = ch.split('_')
                self._resamplers['bar_' + order_book_id].pop(ch, None)

        channels = [
            ch for ch in channels
            if ch not in self._subscribed_by_user and (ch not in self._resamplers or not self._resamplers[ch])
        ]

        data = {
            "action": "unsubscribe",
            "channels": channels,
        }
        self._client.send(json_dumps(data))

    def _reconnect(self):
        if self._closed:
            return

        self._init_websocket_client()
        self.subscribe(list(self._subscribed_by_user))
        for resamplers in self._resamplers.values():
            for resampler in resamplers.values():
                resampler.reset()

    def _listen(self):
        from websocket import WebSocketException
        while not self._closed:
            try:
                res = self._client.recv()
                if res:
                    data = json_loads(res)
                    if data['action'] == 'feed':
                        ch = data['channel']
                        if ch in self._resamplers:
                            for resampler in self._resamplers[ch].values():
                                bar = resampler.enqueue(data)
                                if bar is not None:
                                    yield bar
                        if ch in self._subscribed_by_user:
                            yield data
                    elif data['action'] == 'subscribe_reply':
                        self._subscribed.update(data['subscribed'])
                    elif data['action'] == 'unsubscribe_reply':
                        self._subscribed -= set(data['unsubscribed'])
            except WebSocketException:
                time.sleep(0.1)
                self._reconnect()

    def listen(self, handler=None):
        """获取实时行情。
        当 handler 参数为 None (默认情况) 时，此函数返回一个generator，用法如下：

            for msg in client.listen():
                process(msg)

        当 handler 不为 None 时，此函数会启动一个新的线程，在线程中执行：

            for msg in client.listen():
                handler(msg)

        注意，此时 handler 在另一个线程中执行；请小心处理线程之间的同步问题。此时函数不再阻塞，返回创建的线程对象。
        当调用 `client.close()` 时，线程会关闭。

        :returns: generator | threading.Thread
        """
        if self._closed:
            raise RuntimeError('this connection is closed.')

        if handler is None:
            return self._listen()

        def _process_msg():
            for msg in self._listen():
                if self._closed:
                    break
                handler(msg)

        thread = threading.Thread(target=_process_msg, daemon=True)
        thread.start()
        return thread
