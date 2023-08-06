# -*- coding: utf-8 -*-
import six
import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from rqdatac.validators import (
    ensure_string,
    ensure_list_of_string,
    ensure_date_int,
    ensure_date_or_today_int,
    ensure_date_range,
    check_items_in_container,
)
from rqdatac import get_trading_dates, get_next_trading_date
from rqdatac.client import get_client
from rqdatac.decorators import export_as_api, ttl_cache
from rqdatac.utils import int8_to_datetime, to_datetime


@export_as_api
def get_dominant_future(underlying_symbol, start_date=None, end_date=None, rule=0, rank=1, market="cn"):
    import warnings

    msg = "'get_dominant_future' is deprecated, please use 'futures.get_dominant' instead"
    warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
    return get_dominant(underlying_symbol, start_date, end_date, rule, rank, market)


@export_as_api(namespace='futures')
def get_dominant(underlying_symbol, start_date=None, end_date=None, rule=0, rank=1, market="cn"):
    """获取指定期货品种当日对应的主力合约

    :param underlying_symbol: 如'IF' 'IC'
    :param start_date: 如 '2015-01-07' (Default value = None)
    :param end_date: 如 '2015-01-08' (Default value = None)
    :param market:  (Default value = "cn")
    :param rule:  主力合约规则 (Default value = 0)
        0：在rule=1的规则上，增加约束(曾做过主力合约的合约，一旦被换下来后，不会再被选上)
        1：合约首次上市时，以当日收盘同品种持仓量最大者作为从第二个交易日开始的主力合约，当同品种其他合约持仓量在收盘后
           超过当前主力合约1.1倍时，从第二个交易日开始进行主力合约的切换。日内不会进行主力合约的切换
    :param rank:  (Default value = 1):
        1: 主力合约
        2: 次主力合约
        3：次次主力合约
    :returns: pandas.Series
        返回参数指定的具体主力合约名称

    """
    if not isinstance(underlying_symbol, six.string_types):
        raise ValueError("invalid underlying_symbol: {}".format(underlying_symbol))

    check_items_in_container(rule, [0, 1], 'rule')
    check_items_in_container(rank, [1, 2, 3], 'order')

    underlying_symbol = underlying_symbol.upper()

    if start_date:
        start_date = ensure_date_int(start_date)

    if end_date:
        end_date = ensure_date_int(end_date)
    elif start_date:
        end_date = start_date

    if rank == 1:
        result = get_client().execute(
            "futures.get_dominant", underlying_symbol, start_date, end_date, rule, market=market)
    else:
        result = get_client().execute(
            "futures.get_dominant_v2", underlying_symbol, start_date, end_date, rule, rank, market=market)

    if not result:
        return
    df = pd.DataFrame(result)
    df["date"] = df["date"].apply(int8_to_datetime)
    return df.set_index("date").sort_index()["dominant"]


@ttl_cache(3600)
def current_real_contract(ob, market):
    today = datetime.date.today()
    if datetime.datetime.now().hour >= 21:
        today = get_next_trading_date(today)
    r = get_dominant(ob, today, today, market=market)
    if isinstance(r, pd.Series) and r.size == 1:
        return r[0]
    return None


_FIELDS = [
    "margin_type",
    "long_margin_ratio",
    "short_margin_ratio",
    "commission_type",
    "open_commission_ratio",
    "close_commission_ratio",
    "close_commission_today_ratio",
]


@export_as_api
def future_commission_margin(order_book_ids=None, fields=None, hedge_flag="speculation"):
    import warnings

    msg = "'future_commission_margin' is deprecated, please use 'futures.get_commission_margin' instead"
    warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
    return get_commission_margin(order_book_ids, fields, hedge_flag)


@export_as_api(namespace='futures')
def get_commission_margin(order_book_ids=None, fields=None, hedge_flag="speculation"):
    """获取期货保证金和手续费数据

    :param order_book_ids: 期货合约, 支持 order_book_id 或 order_book_id list,
        若不指定则默认获取所有合约 (Default value = None)
    :param fields: str 或 list, 可选字段有： 'margin_type', 'long_margin_ratio', 'short_margin_ratio',
            'commission_type', 'open_commission_ratio', 'close_commission_ratio',
            'close_commission_today_ratio', 若不指定则默认获取所有字段 (Default value = None)
    :param hedge_flag: str, 账户对冲类型, 可选字段为: 'speculation', 'hedge',
            'arbitrage', 默认为'speculation', 目前仅支持'speculation' (Default value = "speculation")
    :returns: pandas.DataFrame

    """
    if order_book_ids:
        order_book_ids = ensure_list_of_string(order_book_ids)

    if fields is None:
        fields = _FIELDS
    else:
        fields = ensure_list_of_string(fields, "fields")
        check_items_in_container(fields, _FIELDS, "fields")

    hedge_flag = ensure_string(hedge_flag, "hedge_flag")
    if hedge_flag not in ["speculation", "hedge", "arbitrage"]:
        raise ValueError("invalid hedge_flag: {}".format(hedge_flag))

    ret = get_client().execute("futures.get_commission_margin", order_book_ids, fields, hedge_flag)
    return pd.DataFrame(ret)


@export_as_api
def get_future_member_rank(order_book_id, trading_date=None, info_type='volume'):
    import warnings

    msg = "'get_future_member_rank' is deprecated, please use 'futures.get_member_rank' instead"
    warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
    return get_member_rank(order_book_id, trading_date, info_type)


@export_as_api(namespace='futures')
def get_member_rank(obj, trading_date=None, rank_by='volume', **kwargs):
    """获取指定日期最近的期货会员排名数据
    :param obj： 期货合约或品种代码
    :param trading_date: 日期
    :param rank_by: 排名依据字段
    :keyword start_date
    :keyword end_date
    :returns pandas.DataFrame or None
    """
    if not kwargs:
        trading_date = ensure_date_or_today_int(trading_date)
        ret = get_client().execute("futures.get_member_rank", obj, trading_date, rank_by)
    else:
        start_date = kwargs.pop("start_date", None)
        end_date = kwargs.pop("end_date", None)
        if kwargs:
            raise ValueError('unknown kwargs: {}'.format(kwargs))
        elif start_date and end_date:
            start_date, end_date = ensure_date_int(start_date), ensure_date_int(end_date)
            ret = get_client().execute("futures.get_member_rank_v2", obj, start_date, end_date, rank_by)
        else:
            raise ValueError('please ensure start_date and end_date exist')

    if not ret:
        return

    df = pd.DataFrame(ret).sort_values(by=['trading_date', 'rank'])
    df.set_index('trading_date', inplace=True)
    return df


@export_as_api(namespace="futures")
def get_warehouse_stocks(underlying_symbols, start_date=None, end_date=None, market="cn"):
    """获取时间区间内期货的注册仓单

    :param underlying_symbols: 期货品种, 支持列表查询
    :param start_date: 如'2015-01-01', 如果不填写则为去年的当日日期
    :param end_date: 如'2015-01-01', 如果不填写则为当日日期
    :param market: 市场, 默认为"cn"
    :return: pd.DataFrame

    """
    underlying_symbols = ensure_list_of_string(underlying_symbols, name="underlying_symbols")
    start_date, end_date = ensure_date_range(start_date, end_date, delta=relativedelta(years=1))

    # 有新老两种 symbol 时对传入的 underlying_symbols 需要对应成新的 symbol, 并对并行期结束后仍使用老的 symbol 予以警告
    multi_symbol_map = {'RO': 'OI', 'WS': 'WH', 'ER': 'RI', 'TC': 'ZC', 'ME': 'MA'}
    symbol_date_map = {'RO': 20130515, 'WS': 20130523, 'ER': 20130523, 'TC': 20160408, 'ME': 20150515}
    for symbol in set(underlying_symbols) & set(multi_symbol_map):
        date_line = symbol_date_map[symbol]
        if end_date > date_line:
            import warnings
            msg = 'You are using the old symbol: {}, however the new symbol: {} is available after {}.'.format(symbol, multi_symbol_map[symbol], date_line)
            warnings.warn(msg, category=DeprecationWarning, stacklevel=2)

    # 对传入的 underlying_symbols 依照 multi_symbol_map 生成一个对照 DataFrame
    symbol_map_df = pd.DataFrame([(symbol, multi_symbol_map.get(symbol, symbol)) for symbol in set(underlying_symbols)],
                                 columns=['origin', 'new'])
    # 将 underlying_symbols 中 所有老的 symbol 对应为新的再去 mongo 查询
    underlying_symbols = list(symbol_map_df.new.unique())
    ret = get_client().execute("futures.get_warehouse_stocks", underlying_symbols, start_date, end_date, market=market)
    if not ret:
        return
    columns = ["date", "underlying_symbol", "on_warrant", "exchange", 'effective_forecast', 'warrant_units',
               'contract_multiplier', 'deliverable']
    df = pd.DataFrame(ret, columns=columns)

    df = df.merge(symbol_map_df, left_on='underlying_symbol', right_on='new')
    df.drop(['underlying_symbol', 'new'], axis=1, inplace=True)
    df.rename(columns={'origin': 'underlying_symbol'}, inplace=True)
    df.set_index(['date', 'underlying_symbol'], inplace=True)
    return df.sort_index()


@export_as_api(namespace="futures")
def get_contract_multiplier(underlying_symbols, start_date=None, end_date=None, market="cn"):
    """获取时间区间内期货的合约乘数

    :param underlying_symbols: 期货品种, 支持列表查询
    :param start_date: 开始日期, 如'2015-01-01', 如果不填写则取underlying_symbols对应实际数据最早范围
    :param end_date: 结束日期, 如'2015-01-01', 如果不填写则为当日前一天
    :param market: 市场, 默认为"cn", 当前仅支持中国市场
    :return: pd.DataFrame

    """
    underlying_symbols = ensure_list_of_string(underlying_symbols, name="underlying_symbols")
    ret = get_client().execute("futures.get_contract_multiplier", underlying_symbols)
    if not ret:
        return

    # 因 mongo 数据为时间范围，要返回每一天的数据，需复制合约乘数数据至至范围内所有 trading_date
    if start_date:
        start_date = to_datetime(start_date)
    if not end_date:
        end_date = datetime.datetime.today() - datetime.timedelta(days=1)
    end_date = to_datetime(end_date)

    def fill(group_df):
        # 根据当前合约日期范围及给定范围内获取所有 trading_date
        date_min, date_max = group_df['effective_date'].min(), group_df['cancel_date'].max()
        if start_date is not None:
            date_min = max(start_date, date_min)
        date_max = min(date_max, end_date)
        trading_dates = pd.to_datetime(get_trading_dates(date_min, date_max)+group_df['effective_date'].to_list()).unique()

        # 使用 trading_dates 作为 index 插入并填充数据
        everyday_df = group_df.set_index(['effective_date']).reindex(trading_dates).sort_index().ffill().reset_index().rename(columns={'index': 'date'})
        everyday_df = everyday_df[(everyday_df['date'] >= date_min) & (everyday_df['date'] <= date_max)]

        return everyday_df

    df = pd.DataFrame(ret).groupby(by=['underlying_symbol']).apply(fill)

    df = df[['date', 'underlying_symbol', 'exchange', 'contract_multiplier']]
    df.set_index(['underlying_symbol', 'date'], inplace=True)
    df.sort_index(inplace=True)
    return df


@export_as_api(namespace="futures")
def get_basis(order_book_ids, start_date=None, end_date=None, fields=None, market="cn"):
    """ 获取股指期货升贴水信息.

    :param order_book_ids: 期货合约, 支持 order_book_id 或 order_book_id list.
    :param start_date: 开始时间, 若不传, 为 end_date 前3个月.
    :param end_date: 结束时间, 若不传, 为 start_date 后3个月, 如果 start_date 也不传, 则默认为最近3个月.
    :param fields: 需要返回的字段, 若不传则返回所有字段, 支持返回的字段包括
        open, high, low, close, index, close_index, basis, basis_rate, basis_annual_rate.
    :return: MultiIndex DataFrame.
    """
    start_date, end_date = ensure_date_range(start_date, end_date)
    def _calc_annual_rate(row):
        # row.name[1] is current date.
        order_book_id, current_date = row.name
        dates_to_delisted = calendar.get_trading_dates(current_date, delisted_map[order_book_id])[1:]
        if len(dates_to_delisted) == 0:
            # 在到期的时候, basis_annual_rate 的值本身也没有什么意义, 所以直接赋值为 nan.
            return float("nan")
        else:
            return row["basis_rate"] * 250 / len(dates_to_delisted)

    # filter and check order_book_ids.
    from ..services import basic, get_price, calendar
    from ..services.detail import get_price_df
    insts = basic.instruments(order_book_ids)
    if insts is None:
        return None
    if not isinstance(order_book_ids, list):
        insts = [insts]
    insts = [
        x for x in insts
        if x.type == "Future" and x.listed_date != "0000-00-00" and x.industry_name == "股指"
    ]
    if not insts:
        return None
    underlying_id_map = {x.order_book_id: x.underlying_order_book_id for x in insts}

    # get future price.
    order_book_ids = [x.order_book_id for x in insts]
    future_price = get_price.get_price(order_book_ids, start_date, end_date, fields=["close", "open", "high", "low"], expect_df=True)
    if future_price is None:
        return None
    future_price["index"] = future_price.index.get_level_values("order_book_id").map(underlying_id_map)
    # get index price.
    underlying_ids = list({x.underlying_order_book_id for x in insts})
    index_close = get_price_df.get_future_indx_daybar(underlying_ids, start_date, end_date, fields=["close"])["close"]

    # x.name[1] is relative timestamp.
    future_price["close_index"] = future_price.apply(lambda x: index_close.loc[(x['index'], x.name[1])], axis=1)
    future_price["basis"] = future_price["close"] - future_price["close_index"]
    future_price["basis_rate"] = future_price["basis"] / future_price["close_index"] * 100
    delisted_map = {x.order_book_id: x.de_listed_date for x in insts}
    future_price["basis_annual_rate"] = future_price.apply(lambda x: _calc_annual_rate(x), axis=1)

    # filter by given fields.
    VALID_FIELDS = {"open", "high", "low", "close", "index", "close_index", "basis", "basis_rate", "basis_annual_rate"}
    if fields is not None:
        fields = set(ensure_list_of_string(fields))
    else:
        fields = VALID_FIELDS

    fields = list(fields & VALID_FIELDS)
    return future_price[fields]


VALID_ADJUST_METHODS = ['prev_close_spread', 'open_spread', 'prev_close_ratio', 'open_ratio']


@ttl_cache(1800)
def _get_future_factors_df(market='cn'):
    """ 获取所有复权因子表 """
    data = get_client().execute('futures.__internal__get_future_factors', market=market)
    df = pd.DataFrame(data)
    df['ex_date'] = df['ex_date'].apply(int8_to_datetime)
    df.set_index(['underlying_symbol', 'ex_date'], inplace=True)
    df.sort_index(inplace=True)
    return df


@export_as_api(namespace='futures')
def get_ex_factor(underlying_symbols, start_date=None, end_date=None, adjust_method='prev_close_spread', market='cn'):
    """ 获取期货复权因子

    :param underlying_symbols: 期货合约品种，str or list
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param adjust_method: 复权方法，prev_close_spread, prev_close_ratio, open_spread, open_ratio,
    默认为‘prev_close_spread'
    :param market: 默认是中国内地市场('cn') 。可选'cn' - 中国内地市场
    :return: DataFrame
    """
    df = _get_future_factors_df(market)
    valid_underlying_symbols = df.index.get_level_values('underlying_symbol').unique().tolist()
    underlying_symbols = ensure_list_of_string(underlying_symbols, 'underlying_symbols')
    check_items_in_container(adjust_method, VALID_ADJUST_METHODS, 'adjust_method')
    check_items_in_container(underlying_symbols, valid_underlying_symbols, 'underlying_symbols')

    factor = df.loc[underlying_symbols, adjust_method]
    factor.name = 'ex_factor'
    factor = factor.reset_index()

    spread = adjust_method.endswith('spread')

    def _process(x):
        x['ex_end_date'] = x['ex_date'].shift(-1) - pd.offsets.DateOffset(days=1)
        if spread:
            x['ex_cum_factor'] = x['ex_factor'].cumsum()
        else:
            x['ex_cum_factor'] = x['ex_factor'].cumprod()
        return x

    factor = factor.groupby('underlying_symbol', as_index=False).apply(_process)
    if start_date and end_date:
        start_date, end_date = to_datetime(start_date), to_datetime(end_date)
        factor = factor[(start_date <= factor['ex_date']) & (factor['ex_date'] <= end_date)]
    # _get_future_factors_df 已经排序过了，此处无需再次排序
    return factor.set_index('ex_date')


@ttl_cache(1800)
def __internal_get_ex_factor(adjust_type, adjust_method):
    """ 内部使用，获取复权因子，提供给get_dominant_price进行复权计算用
    :return: pd.Series
    """
    df = _get_future_factors_df()

    factor = df[adjust_method]
    factor.name = 'ex_factor'
    factor = factor.reset_index()
    pre = adjust_type == 'pre'
    ratio = adjust_method.endswith('ratio')
    today = datetime.date.today()

    def _process(x):
        if ratio:
            x['ex_cum_factor'] = x['ex_factor'].cumprod()
            if pre:
                x['ex_cum_factor'] = x['ex_cum_factor'] / x['ex_cum_factor'].iloc[-1]
        else:
            x['ex_cum_factor'] = x['ex_factor'].cumsum()
            if pre:
                x['ex_cum_factor'] = x['ex_cum_factor'] - x['ex_cum_factor'].iloc[-1]

        # 按交易日扩展后ffill
        min_date = x['ex_date'].min()
        tds = get_trading_dates(min_date, today)
        tds = pd.to_datetime(tds)
        # tds 是从小到大排列的， 因此reindex后无需再sort
        return x.set_index('ex_date').reindex(tds).ffill()

    factor = factor.groupby('underlying_symbol', as_index=True).apply(_process)
    return factor['ex_cum_factor']


DOMINANT_PRICE_ADJUST_FIELDS = [
    'open', 'high', 'low', 'close', 'last', 'limit_up', 'limit_down', 'settlement', 'prev_settlement', 'prev_close',
    'a1', 'a2', 'a3', 'a4', 'a5', 'b1', 'b2', 'b3', 'b4', 'b5'
]


@export_as_api(namespace='futures')
def get_dominant_price(
        underlying_symbols, start_date=None, end_date=None,
        frequency='1d', fields=None, adjust_type='pre', adjust_method='prev_close_spread'
):
    """ 获取主力合约行情数据

    :param underlying_symbols: 期货合约品种，可传入 underlying_symbol, underlying_symbol list
    :param start_date: 开始日期, 最小日期为 20210104
    :param end_date: 结束日期
    :param frequency: 历史数据的频率。 支持/日/分钟/tick 级别的历史数据，默认为'1d'。
        1m- 分钟线，1d-日线，分钟可选取不同频率，例如'5m'代表 5 分钟线
    :param fields: 字段名称列表
    :param adjust_type: 复权方式，不复权 - none，前复权 - pre，后复权 - post
    :param adjust_method: 复权方法 ，prev_close_spread/open_spread:基于价差复权因子进行复权，
        prev_close_ratio/open_ratio:基于比例复权因子进行复权，
        默认为‘prev_close_spread',adjust_type为None 时，adjust_method 复权方法设置无效
    :return: MultiIndex DataFrame
    """
    # ensure underlying symbols list
    from ..services.get_price import get_price
    if not isinstance(underlying_symbols, list):
        underlying_symbols = [underlying_symbols]
    if fields and not isinstance(fields, list):
        fields = [fields]
    start_date, end_date = ensure_date_range(start_date, end_date)
    if start_date < 20100104:
        raise ValueError('expect start_date >= 20100104, get {}'.format(start_date))
    # ensure adjust_type and adjust_method
    check_items_in_container(adjust_type, ['none', 'pre', 'post'], 'adjust_type')
    check_items_in_container(adjust_method, VALID_ADJUST_METHODS, 'adjust_method')

    _date_key = 'date' if frequency == '1d' else 'trading_date'
    _fields = fields
    if fields and frequency != '1d' and 'trading_date' not in fields:
        _fields = ['trading_date'] + fields

    obs = [u + '88' for u in underlying_symbols]
    df = get_price(
        order_book_ids=obs, start_date=start_date, end_date=end_date,
        frequency=frequency, adjust_type='none', fields=_fields, expect_df=True
    )
    if df is None:
        return

    df.reset_index(inplace=True)
    df['underlying_symbol'] = df['order_book_id'].str[:-2]
    df.set_index(['underlying_symbol', _date_key], inplace=True)
    if adjust_type != 'none':
        # 复权调整
        factor = __internal_get_ex_factor(adjust_type, adjust_method)
        values = factor.reindex(df.index).values
        _fields = fields if fields else df.columns.tolist()
        adjust_fields = [f for f in DOMINANT_PRICE_ADJUST_FIELDS if f in _fields]
        if adjust_method.endswith('spread'):
            for field in adjust_fields:
                df[field] += values
        elif adjust_method.endswith('ratio'):
            for field in adjust_fields:
                df[field] *= values
        if 'total_turnover' in df.columns:
            df['total_turnover'] = 0

    if frequency != '1d':
        df = df.reset_index().set_index(['underlying_symbol', 'datetime'])
    df.sort_index(inplace=True)
    del df['order_book_id']
    return df[fields] if fields else df
