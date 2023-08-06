# -*- coding: utf-8 -*-
import warnings
from collections import defaultdict
import pandas as pd
import numpy as np
from rqdatac.utils import today_int

from rqdatac.validators import (
    ensure_list_of_string,
    ensure_order_book_ids,
    check_items_in_container,
    ensure_date_range,
    ensure_date_int,
    ensure_string_in,
)

from rqdatac.client import get_client
from rqdatac.decorators import export_as_api, ttl_cache


CONSENSUS_INDICATOR_FIELDS = [
    'net_profit_t',
    'net_profit_t1',
    'net_profit_t2',
    'revenue_t',
    'revenue_t1',
    'revenue_t2',
    'net_asset_t',
    'net_asset_t1',
    'net_asset_t2',
    'cash_from_operating_activities_t',
    'cash_from_operating_activities_t1',
    'cash_from_operating_activities_t2',
    'profit_from_operation_t',
    'profit_from_operation_t1',
    'profit_from_operation_t2',
    'cost_of_goods_sold_t',
    'cost_of_goods_sold_t1',
    'cost_of_goods_sold_t2',
    'profit_before_tax_t',
    'profit_before_tax_t1',
    'profit_before_tax_t2',
    'ebit_t',
    'ebit_t1',
    'ebit_t2',
    'operating_revenue_per_share_t',
    'operating_revenue_per_share_t1',
    'operating_revenue_per_share_t2',
    'eps_t',
    'eps_t1',
    'eps_t2',
    'bps_t',
    'bps_t1',
    'bps_t2',
    'share_cap_chg_date',
    'report_main_id',
    'grade_coef',
    'targ_price',
    'ebitda_t',
    'ebitda_t1',
    'ebitda_t2',
    'profit_res_t',
    'profit_res_t1',
    'profit_res_t2',
    'operate_cash_flow_per_share_t',
    'operate_cash_flow_per_share_t1',
    'operate_cash_flow_per_share_t2',
    'profit_chg_t',
    'profit_chg_t1',
    'profit_chg_t2',
    'grade_chg_t',
    'grade_chg_t1',
    'grade_chg_t2',
    'targ_price_chg_t',
    'targ_price_chg_t1',
    'targ_price_chg_t2',
    'chg_reason_t',
    'chg_reason_t1',
    'chg_reason_t2',
    'create_time',
]


DTYPES = {k: '<f8' for k in CONSENSUS_INDICATOR_FIELDS}
DTYPES['fiscal_year'] = '<u4'
DTYPES['data_source'] = 'u1'
del DTYPES['share_cap_chg_date'], DTYPES['report_main_id'], DTYPES['create_time']


CONSENSUS_PRICE_FIELDS = [
    'half_year_target_price',
    'one_year_target_price',
    'quarter_recommendation',
    'half_year_recommendation',
    'one_year_recommendation',
]

CONSENSUS_PRICE_FIELDS_MAP = {
    'half_year_target_price': ('price_raw', 'price_prd', 'M06'),
    'one_year_target_price': ('price_raw', 'price_prd', 'Y01'),
    'quarter_recommendation': ('grd_coef', 'grd_prd', '1'),
    'half_year_recommendation': ('grd_coef', 'grd_prd', '2'),
    'one_year_recommendation': ('grd_coef', 'grd_prd', '3'),
}

PRICE_DTYPES = {
    'half_year_target_price': '<f8',
    'one_year_target_price': '<f8',
    'quarter_recommendation': '<f8',
    'half_year_recommendation': '<f8',
    'one_year_recommendation': '<f8',
    'price_raw': '<f8',
}


@export_as_api
def get_consensus_indicator(order_book_ids, fiscal_year, fields=None, market='cn'):
    """
    获取一致预期数据

    :param order_book_ids: 股票名称
    :param fiscal_year: int/str, 查询年份
    :param fields: list,  一致预期字段
    :param market: (Default value = 'cn')
    :returns: pandas  MultiIndex DataFrame
    """
    order_book_ids = ensure_order_book_ids(order_book_ids, market=market)
    fiscal_year = int(fiscal_year)
    if fields is None:
        fields = CONSENSUS_INDICATOR_FIELDS
    else:
        fields = ensure_list_of_string(fields, 'consensus_indicator')
        check_items_in_container(fields, CONSENSUS_INDICATOR_FIELDS, 'consensus_indicator')
    data = get_client().execute('get_consensus_indicator', order_book_ids, fiscal_year, fields, market=market)
    if not data:
        return None
    df = pd.DataFrame(data)
    df.set_index(['order_book_id', 'date'], inplace=True)
    df.sort_index(inplace=True)
    dtypes = {f: DTYPES[f] for f in df.columns if f in DTYPES}
    df = df.astype(dtypes)
    return df


@export_as_api
def get_consensus_price(order_book_ids, start_date=None, end_date=None, fields=None, adjust_type='none', market='cn'):
    """
    获取一致预期股价预测数据

    :param order_book_ids: 股票名称
    :param start_date: 开始日期， date-like object, 默认三月前那天
    :param end_date: 结束日期， date-like object， 默认当天
    :param fields: list,  一致预期字段
    :param adjust_type: 可选参数,默认为‘none', 返回原始数据
            'pre' 返回前复权数据
            'post' 返回后复权数据
    :param market: (Default value = 'cn')
    :returns: pandas MultiIndex DataFrame
    """
    order_book_ids = ensure_order_book_ids(order_book_ids, market=market)

    if fields is None:
        fields = CONSENSUS_PRICE_FIELDS
    else:
        fields = ensure_list_of_string(fields, 'consensus_price')
        check_items_in_container(fields, CONSENSUS_PRICE_FIELDS, 'consensus_price')

    start_date, end_date = ensure_date_range(start_date, end_date)

    data = get_client().execute('get_consensus_price', order_book_ids, start_date, end_date, market=market)
    if not data:
        return None

    records = defaultdict(dict)
    for r in data:
        key = (r['order_book_id'], r['institute'], r['date'])
        if key not in records:
            records[key].update(r)
        for field in fields:
            name, f, value = CONSENSUS_PRICE_FIELDS_MAP[field]
            if r[f] == value:
                records[key][field] = r[name]
    df = pd.DataFrame(list(records.values()))
    df.set_index(['order_book_id', 'date'], inplace=True)
    df.sort_index(inplace=True)
    for f in fields:
        if f not in df.columns:
            df[f] = None
    df = df.astype({f: PRICE_DTYPES[f] for f in fields if f in PRICE_DTYPES})

    if adjust_type != 'none':
        adjust_fields = list(set(CONSENSUS_PRICE_FIELDS[:2]) & set(fields))
        if not adjust_fields:
            return df

        from rqdatac.services.detail.adjust_price import get_ex_factor_for
        ex_factors = get_ex_factor_for(order_book_ids, market)
        pre = adjust_type == 'pre'

        def adjust(sub):
            factors = ex_factors.get(sub.name)
            if factors is None:
                return sub
            factor = np.take(factors.values, factors.index.searchsorted(sub.index.get_level_values(1), side='right') - 1)
            if pre:
                factor /= factors.iloc[-1]

            sub[adjust_fields] = (sub[adjust_fields].values.T * factor).T
            return sub

        df = df.groupby(level=0).apply(adjust)
        df[adjust_fields] = np.round(df[adjust_fields], 4)

    return df


CONSENSUS_COMP_INDICATOR_FIELDS = [
    'comp_operating_revenue_t',
    'comp_con_operating_revenue_t1',
    'comp_con_operating_revenue_t2',
    'comp_con_operating_revenue_t3',
    'comp_con_operating_revenue_ftm',
    'comp_net_profit_t',
    'comp_con_net_profit_t1',
    'comp_con_net_profit_t2',
    'comp_con_net_profit_t3',
    'comp_con_net_profit_ftm',
    'comp_eps_t',
    'comp_con_eps_t1',
    'comp_con_eps_t2',
    'comp_con_eps_t3',
    'comp_net_asset_t',
    'comp_con_net_asset_t1',
    'comp_con_net_asset_t2',
    'comp_con_net_asset_t3',
    'comp_con_net_asset_ftm',
    'comp_cash_flow_t',
    'comp_con_cash_flow_t1',
    'comp_con_cash_flow_t2',
    'comp_con_cash_flow_t3',
    'comp_con_cash_flow_ftm',
    'comp_roe_t',
    'comp_con_roe_t1',
    'comp_con_roe_t2',
    'comp_con_roe_t3',
    'comp_con_roe_ftm',
    'comp_pe_t',
    'comp_con_pe_t1',
    'comp_con_pe_t2',
    'comp_con_pe_t3',
    'comp_con_pe_ftm',
    'comp_ps_t',
    'comp_con_ps_t1',
    'comp_con_ps_t2',
    'comp_con_ps_t3',
    'comp_con_ps_ftm',
    'comp_pb_t',
    'comp_con_pb_t1',
    'comp_con_pb_t2',
    'comp_con_pb_t3',
    'comp_con_pb_ftm',
    'comp_peg',
    'comp_operating_revenue_growth_ratio_t',
    'comp_con_operating_revenue_growth_ratio_t1',
    'comp_con_operating_revenue_growth_ratio_t2',
    'comp_con_operating_revenue_growth_ratio_t3',
    'comp_con_operating_revenue_growth_ratio_ftm',
    'comp_net_profit_growth_ratio_t',
    'comp_con_net_profit_growth_ratio_t1',
    'comp_con_net_profit_growth_ratio_t2',
    'comp_con_net_profit_growth_ratio_t3',
    'comp_con_net_profit_growth_ratio_ftm',
    'con_grd_coef',
    'con_targ_price',
    'comp_con_eps_ftm',
    'ty_profit_t1',
    'ty_profit_t2',
    'ty_profit_t3',
    'ty_profit_ftm',
    'ty_eps_t1',
    'ty_eps_t2',
    'ty_eps_t3',
    'ty_eps_ftm',
]


@export_as_api
def get_consensus_comp_indicators(order_book_ids, start_date=None, end_date=None, fields=None, market='cn'):
    """
    获取个股一致预期表

    :param order_book_ids: 股票名称
    :param start_date: date-like object, 默认当日
    :param end_date: date-like object, 默认为当日
    :param fields: list,  一致预期字段
    :param market: (Default value = 'cn')

    :returns: pandas MultiIndex DataFrame
    """
    order_book_ids = ensure_order_book_ids(order_book_ids, market=market)
    today = today_int()
    start_date = ensure_date_int(start_date) if start_date else today
    end_date = ensure_date_int(end_date) if end_date else today

    if fields is None:
        fields = CONSENSUS_COMP_INDICATOR_FIELDS
    else:
        fields = ensure_list_of_string(fields, 'consensus_comp_indicator')
        check_items_in_container(fields, CONSENSUS_COMP_INDICATOR_FIELDS, 'consensus_comp_indicator')
    data = get_client().execute('get_consensus_comp_indicators', order_book_ids, start_date, end_date, fields, market=market)
    if not data:
        return None
    df = pd.DataFrame(data)
    df.set_index(['order_book_id', 'date'], inplace=True)
    df.sort_index(inplace=True)
    dtypes = {f: DTYPES[f] for f in df.columns if f in DTYPES}
    df = df.astype(dtypes)
    return df


@ttl_cache(3600)
def _all_consensus_industries(market='cn'):
    return get_client().execute('all_consensus_industries', market=market)


@ttl_cache(3600)
def _all_consensus_industry_dict(market='cn'):
    result = defaultdict(list)
    for v in _all_consensus_industries(market):
        result[v['industry_code']].append(v['industry_code'])
        result[v['industry_name']].append(v['industry_code'])
    return result


def ensure_consensus_industries(industries):
    industries = ensure_list_of_string(industries)
    code_mapping = _all_consensus_industry_dict()
    industry_codes = set()
    for i in industries:
        if i in code_mapping:
            industry_codes.update(code_mapping[i])
    return list(industry_codes)


@export_as_api
def all_consensus_industries(market='cn'):
    data = _all_consensus_industries(market)
    return pd.DataFrame(data).set_index('industry_code')


@export_as_api
def get_consensus_industry_rating(industries, start_date, end_date, market='cn'):
    """
    获取行业评级数据

    :param industries: str or list, 行业code是今日投资行业分类代码, 可通过all_consensus_industries()获取全部
    :param start_date: date-like object， 结束日期
    :param end_date: date-like object, 结束日期
    :param market: str, 默认'cn'
    :return: pandas.DataFrame
    """
    industries = ensure_consensus_industries(industries)
    if not industries:
        warnings.warn('No valid industry found')
        return None

    start_date, end_date = ensure_date_range(start_date, end_date)
    data = get_client().execute('get_consensus_industry_rating', industries, start_date, end_date, market=market)
    if not data:
        return None

    df = pd.DataFrame(data)
    df.set_index(['industry_name', 'info_date'], inplace=True)
    return df


@export_as_api
def get_consensus_market_estimate(indexes, fiscal_year, market='cn'):
    """
    获取今日投资的机构预测大势表

    :param indexes: str or list, 指数列表
    :param fiscal_year: int, 年份
    :param market: str, default 'cn'
    :return: pandas MultiIndex DataFrame

    :example:
    >>> get_consensus_market_estimate('000001.XSHG', 2021)
                                fiscal_year    institute start_date  ...  period  value
    order_book_id info_date                        ...
    000001.XSHG   2020-10-13        2021    财信证券 2021-01-01  ...  策略年度报告     中性
                  2020-10-16        2021    华融证券 2021-01-01  ...  策略年度报告     中性
                  2020-10-23        2021    东北证券 2021-01-01  ...  策略年度报告     中性
                  2020-11-01        2021    方正证券 2021-01-01  ...  策略年度报告     中性
                  2020-11-02        2021    西南证券 2021-01-01  ...  策略年度报告     中性
                                    ...      ...      ...       ...     ...        ...
                  2021-12-31        2021    山西证券 2022-01-01  ...  策略月度报告     中性
                  2021-12-31        2021    方正证券 2021-12-31  ...   策略日报等     中性
                  2021-12-31      2021    东亚前海证券 2022-01-01  ...  策略月度报告     中性
                  2021-12-31        2021    粤开证券 2022-01-01  ...  策略月度报告     乐观
                  2021-12-31        2021    渤海证券 2022-01-01  ...  策略月度报告     中性

    返回字段:
    fiscal_year: 预测年份
    institue: 机构名称
    start_date: 预测开始日期
    end_date: 预测结束日期
    high: 预测高点
    low: 预测低点
    period: 预测时段
    value: 预测值
    """

    indexes = ensure_list_of_string(indexes)
    indexes = ensure_order_book_ids(indexes, type='INDX')
    fiscal_year = int(fiscal_year)
    data = get_client().execute('get_consensus_market_estimate', indexes, fiscal_year, market=market)
    if not data:
        return None
    df = pd.DataFrame(data)
    df.set_index(['order_book_id', 'info_date'], inplace=True)
    df.sort_index(inplace=True)
    return df
