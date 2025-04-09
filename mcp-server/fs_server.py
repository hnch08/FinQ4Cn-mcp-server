import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from mcp.server.fastmcp import FastMCP

from utils.func_stocks import StockUtils

# Initialize the MCP server
mcp = FastMCP()
stock_utils=StockUtils()

# MCP Tool: 
@mcp.tool()
def get_today_date() -> str:
    """
    获取当前时间的日期。

    Args:

    Returns:
        today: 当前时间的日期，格式为 YYYY-MM-DD
    """
    # 获取当前日期时间
    today = datetime.today()
    
    # 格式化为 YYYY-MM-DD 格式
    today_formatted = today.strftime("%Y-%m-%d")
    
    return today_formatted

# MCP Tool: 
@mcp.tool()
def get_stock_code(name: str)  -> List[Dict[str, Any]]:
    """
    获取中国 A 股上市公司股票代码

    Args:
        name: 股票名称

    Returns:
        返回字典的列表，每个字典表示一家上市公司的股票名称及股票代码。每条记录包含以下字段: 
        | name          | str  | 股票名称 |
        | stock_code    | str  | 股票代码 |
    """

    return stock_utils.get_stock_code(name)

@mcp.tool()
def get_historical_stockprice_data(stock_code: str ,
                                   start_date: str,
                                   end_date: str, 
                                   period: Optional[str] = 'daily', 
                                   adjust: Optional[str] = '') -> List[Dict[str, Any]]:
    """
    获取中国 A 股上市公司股票的历史价格数据。

    Args:
        stock_code: 股票代码
        start_date: 查询的开始日期，格式为 'YYYYMMDD'。
        end_date: 查询的结束日期，格式为 'YYYYMMDD'。
        period: 数据频率，可选值: {'daily', 'weekly', 'monthly'}，分别表示按天、按周、按月。
        adjust: 是否复权，可选值: {'', 'qfq', 'hfq'}，分别表示不复权、前复权、后复权。

    Returns:
      返回字典的列表，每个字典表示一个周期股票价格。每条记录包含以下字段：
            | date          | object  | 交易日期         |
            | stock_code    | object  | 股票代码（不带市场标识） |
            | open          | float64 | 开盘价           |
            | close         | float64 | 收盘价           |
            | high          | float64 | 最高价           |
            | low           | float64 | 最低价           |
            | volume        | int64   | 成交量（单位：手） |
            | turnover      | float64 | 成交额（单位：元） |
            | amplitude     | float64 | 振幅（单位：%）   |
            | change_rate   | float64 | 涨跌幅（单位：%） |
            | change_amount | float64 | 涨跌额（单位：元） |
            | turnover_rate | float64 | 换手率（单位：%） |
    """
    return stock_utils.get_historical_stockprice_data(stock_code, start_date, end_date, period, adjust)

@mcp.tool()
def get_stock_financial_abstract(stock_code: str ,
                                 indicator: Optional[str] = '按报告期')  -> List[Dict[str, Any]]:
    """
    获取中国 A 股上市公司的财务报告概要数据。

    Args:
        stock_code: 股票代码
        indicator: 指标类型，可选值: {'按报告期', '按年度', '按单季度'}

    Returns:
        返回字典的列表，每个字典表示一条财务概要记录。每条记录包含以下字段：
        | reporting_period               | object   | 报告期              |
        | net_profit                     | object   | 净利润              |
        | net_profit_growth_rate         | object   | 净利润同比增长率    |
        | non_recurring_net_profit       | object   | 扣非净利润          |
        | non_recurring_net_profit_growth_rate | object | 扣非净利润同比增长率 |
        | total_operating_revenue        | object   | 营业总收入          |
        | total_operating_revenue_growth_rate | object | 营业总收入同比增长率 |
        | basic_earnings_per_share       | object   | 基本每股收益        |
        | net_asset_per_share            | object   | 每股净资产          |
        | capital_reserve_fund_per_share | object   | 每股资本公积金      |
        | undistributed_profit_per_share | object   | 每股未分配利润      |
        | operating_cash_flow_per_share  | object   | 每股经营现金流      |
        | net_profit_margin              | object   | 销售净利率          |
        | gross_profit_margin            | object   | 销售毛利率          |
        | return_on_equity_of_roe        | object   | 净资产收益率        |
        | diluted_return_on_equity_of_roe| object   | 净资产收益率-摊薄   |
        | operating_cycle                | object   | 营业周期            |
        | inventory_turnover_ratio       | object   | 存货周转率          |
        | days_inventory_outstanding     | object   | 存货周转天数        |
        | days_sales_outstanding         | object   | 应收账款周转天数    |
        | current_ratio                  | object   | 流动比率            |
        | quick_ratio                    | object   | 速动比率            |
        | conservative_quick_ratio       | object   | 保守速动比率        |
        | debt_to_equity_ratio           | object   | 产权比率            |
        | asset_to_liability_ratio       | object   | 资产负债率          |
    """

    return stock_utils.get_stock_financial_abstract(stock_code, indicator)

@mcp.tool()
def get_stock_margin_detail(stock_code: str, start_date: str, end_date: str, freq: str = "D") -> List[Dict[str, Any]]:
    """
    获取中国 A 股上市公司的融资融券明细数据。

    Args:
        stock_code: 股票代码，例如 "600000"。
        start_date: 开始日期，格式为 YYYYMMDD。
        end_date: 结束日期，格式为 YYYYMMDD。
        freq: 日期间隔类型，默认为 "D"（每日）。可选值包括：
                    - "D": 每日
                    - "W": 每周
                    - "MS": 每月的第一天
                    - "ME": 每月的最后一天
                    - "Q": 每季度
                    - "Y": 每年

    Returns:
        返回字典的列表，每个字典表示一个交易日的融资融券概要。每条记录包含以下字段：
        | 字段名                 | 数据类型   | 描述                           |
        |------------------------|------------|--------------------------------|
        | trading_date           | str        | 交易日期                       |
        | target_security_code   | str        | 标的证券代码                   |
        | target_security_name   | str        | 标的证券简称                   |
        | margin_balance         | int        | 融资余额 (单位: 元)             |
        | margin_buy_amount      | int        | 融资买入额 (单位: 元)           |
        | margin_repayment       | int        | 融资偿还额 (单位: 元)           |
        | short_selling_balance  | int        | 融券余量                       |
        | short_selling_volume   | int        | 融券卖出量                     |
        | short_selling_repayment| int        | 融券偿还量                     |
    """

    return stock_utils.get_stock_margin_detail(stock_code, start_date, end_date, freq)

@mcp.tool()
def get_stock_fhps_detail(stock_code: str) -> List[Dict[str, Any]]:
    """
    获取中国 A 股上市公司历年的分红送配详情数据。

    Args:
        stock_code: 股票代码，例如 "600000"。

    Returns:
        List[Dict[str, Any]]: 返回字典的列表，每个字典表示一次分红配送的详情。每条记录包含以下字段：
            | reporting_period | 报告期 | object  |
            | earnings_disclosure_date | 业绩披露日期 | object  |
            | total_share_conversion_ratio | 送转股份-送转总比例 | float64 |
            | bonus_share_ratio | 送转股份-送股比例 | float64 |
            | capitalization_ratio | 送转股份-转股比例 | float64 |
            | cash_dividend_payout_ratio | 现金分红-现金分红比例 | float64 |
            | cash_dividend_payout_ratio_description | 现金分红-现金分红比例描述 | object  |
            | dividend_yield | 现金分红-股息率 | float64 |
            | earnings_per_share | 每股收益 | float64 |
            | net_asset_value_per_share | 每股净资产 | float64 |
            | surplus_reserve_fund_per_share | 每股公积金 | float64 |
            | undistributed_profit_per_share | 每股未分配利润 | float64 |
            | net_profit_growth_rate | 净利润同比增长 | float64 |
            | total_shares_outstanding | 总股本 | int64   |
            | preliminary_plan_announcement_date | 预案公告日 | object  |
            | record_date | 股权登记日 | object  |
            | ex_dividend_date | 除权除息日 | object  |
            | proposal_progress | 方案进度 | object  |
            | latest_announcement_date | 最新公告日期 | object  |
    """

    return stock_utils.get_stock_fhps_detail(stock_code)
    
# Start the MCP server
if __name__ == "__main__":
    print(f"ASkare Stocks MCP Server starting...")
    mcp.run()
