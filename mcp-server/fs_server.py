from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from mcp.server.fastmcp import FastMCP

from utils.stocks_common_metrics import StocksCommonMetrics
from utils.news_report import News_Report


# Initialize the MCP server
mcp = FastMCP()
stocks_common_metrics=StocksCommonMetrics()
news_report=News_Report()


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

# ----------------- 股票常用指标类。 ----------------- #
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

    return stocks_common_metrics.get_stock_code(name)


# 经营业务结构
@mcp.tool()
def get_stock_business_structure(stock_code: str)  -> List[Dict[str, Any]]:
    """
    Retrieve the main business structure of Chinese A-share listed companies for analyzing the company's core business, products, services, and revenue distribution.

    Args:
        stock_code: Stock code, e.g., "000001".

    Returns:
        List[Dict[str, Any]]: Returns a list of dictionaries, where each dictionary represents the report content for a specific reporting period. Each dictionary contains the following elements:
            | reporting_period               | str  | Reporting period |
            | classification_direction       | str  | Classification direction |
            | classification                 | str  | Classification |
            | operating_revenue              | str  | Operating revenue (Note: Unit is in yuan) |
            | operating_revenue_yoy_growth   | str  | Year-on-year growth of operating revenue |
            | operating_revenue_pct_of_main  | str  | Percentage of operating revenue to main business revenue |
            | operating_cost                 | str  | Operating cost (Note: Unit is in yuan) |
            | operating_cost_yoy_growth      | str  | Year-on-year growth of operating cost |
            | operating_cost_pct_of_main     | str  | Percentage of operating cost to main business cost |
            | gross_profit_margin            | str  | Gross profit margin |
            | gross_profit_margin_yoy_growth | str  | Year-on-year growth of gross profit margin |
    """

    return stocks_common_metrics.get_stock_business_structure(stock_code)

# 历史价格数据
@mcp.tool()
def get_historical_stockprice_data(stock_code: str ,
                                   start_date: str,
                                   end_date: str, 
                                   period: Optional[str] = 'daily', 
                                   adjust: Optional[str] = '') -> List[Dict[str, Any]]:
    """
    Retrieve historical price data of companies listed on China's A-share market.

    Args:
        stock_code: Stock code.
        start_date: The start date of the query, formatted as 'YYYYMMDD'.
        end_date: The end date of the query, formatted as 'YYYYMMDD'.
        period: Data frequency. Optional values: {'daily', 'weekly', 'monthly'}, representing daily, weekly, and monthly data respectively.
        adjust: Whether to adjust prices. Optional values: {'', 'qfq', 'hfq'}, representing no adjustment, forward adjustment, and backward adjustment respectively.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents the stock price for a specific period. Each dictionary contains the following elements:
            | date          | object  | Trading date              |
            | stock_code    | object  | Stock code (without market identifier) |
            | open          | float | Opening price             |
            | close         | float | Closing price             |
            | high          | float | Highest price             |
            | low           | float | Lowest price              |
            | volume        | int   | Trading volume (unit: lots)|
            | turnover      | float | Trading turnover (unit: yuan)|
            | amplitude     | float | Amplitude (unit: %)       |
            | change_rate   | float | Change rate (unit: %)     |
            | change_amount | float | Change amount (unit: yuan)|
            | turnover_rate | float | Turnover rate (unit: %)   |
    """

    return stocks_common_metrics.get_historical_stockprice_data(stock_code, start_date, end_date, period, adjust)

# 关键财报数据
@mcp.tool()
def get_stock_financial_abstract(stock_code: str ,
                                 indicator: Optional[str] = '按报告期')  -> List[Dict[str, Any]]:
    """
    Retrieve the financial report summary data of companies listed on China's A-share market.

    Args:
        stock_code: Stock code.
        indicator: Type of indicator. Optional values: {'按报告期', '按年度', '按单季度'} (By reporting period, by year, or by single quarter).

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a financial summary record.  Each dictionary contains the following elements:
            | reporting_period               | object   | Reporting period              |
            | net_profit                     | object   | Net profit                    |
            | net_profit_growth_rate         | object   | Net profit growth rate (YoY)  |
            | non_recurring_net_profit       | object   | Non-recurring net profit      |
            | non_recurring_net_profit_growth_rate | object | Non-recurring net profit growth rate (YoY) |
            | total_operating_revenue        | object   | Total operating revenue       |
            | total_operating_revenue_growth_rate | object | Total operating revenue growth rate (YoY) |
            | basic_earnings_per_share       | object   | Basic earnings per share      |
            | net_asset_per_share            | object   | Net assets per share          |
            | capital_reserve_fund_per_share | object   | Capital reserve fund per share|
            | undistributed_profit_per_share | object   | Undistributed profit per share|
            | operating_cash_flow_per_share  | object   | Operating cash flow per share |
            | net_profit_margin              | object   | Net profit margin             |
            | gross_profit_margin            | object   | Gross profit margin           |
            | return_on_equity_of_roe        | object   | Return on equity (ROE)        |
            | diluted_return_on_equity_of_roe| object   | Diluted return on equity (ROE)|
            | operating_cycle                | object   | Operating cycle               |
            | inventory_turnover_ratio       | object   | Inventory turnover ratio      |
            | days_inventory_outstanding     | object   | Days inventory outstanding    |
            | days_sales_outstanding         | object   | Days sales outstanding         |
            | current_ratio                  | object   | Current ratio                 |
            | quick_ratio                    | object   | Quick ratio                   |
            | conservative_quick_ratio       | object   | Conservative quick ratio      |
            | debt_to_equity_ratio           | object   | Debt to equity ratio          |
            | asset_to_liability_ratio       | object   | Asset to liability ratio      |
    """

    return stocks_common_metrics.get_stock_financial_abstract(stock_code, indicator)

# 融资融券明细数据。
@mcp.tool()
def get_stock_margin_detail(stock_code: str, start_date: str, end_date: str, freq: str = "D") -> List[Dict[str, Any]]:
    """
    Retrieve the margin trading and short selling details of companies listed on China's A-share market.

    Args:
        stock_code: Stock code, e.g., "000001".
        start_date: Start date, formatted as YYYYMMDD.
        end_date: End date, formatted as YYYYMMDD.
        freq: Date interval type, default is "D" (daily). Optional values include:
                    - "D": Daily
                    - "W": Weekly
                    - "MS": First day of each month
                    - "ME": Last day of each month
                    - "Q": Quarterly
                    - "Y": Annually

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a summary of margin trading and short selling for a trading day. Each dictionary contains the following elements:
            | trading_date           | str        | Trading date                       |
            | target_security_code   | str        | Target security code               |
            | target_security_name   | str        | Target security abbreviation       |
            | margin_balance         | int        | Margin balance (unit: yuan)        |
            | margin_buy_amount      | int        | Margin purchase amount (unit: yuan)|
            | margin_repayment       | int        | Margin repayment amount (unit: yuan)|
            | short_selling_balance  | int        | Short selling balance              |
            | short_selling_volume   | int        | Short selling volume               |
            | short_selling_repayment| int        | Short selling repayment volume     |
        """

    return stocks_common_metrics.get_stock_margin_detail(stock_code, start_date, end_date, freq)

# 分红送配详情数据
@mcp.tool()
def get_stock_fhps_detail(stock_code: str) -> List[Dict[str, Any]]:
    """
    Retrieve the historical dividend and rights issue details of companies listed on China's A-share market.

    Args:
        stock_code: Stock code, e.g., "600000".

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents the details of a dividend or rights distribution.  Each dictionary contains the following elements:
            | reporting_period                     | Reporting period                        | object  |
            | earnings_disclosure_date             | Earnings disclosure date                | object  |
            | total_share_conversion_ratio         | Share conversion - Total conversion ratio | float |
            | bonus_share_ratio                    | Share conversion - Bonus share ratio     | float |
            | capitalization_ratio                 | Share conversion - Capitalization ratio  | float |
            | cash_dividend_payout_ratio           | Cash dividend - Payout ratio             | float |
            | cash_dividend_payout_ratio_description | Cash dividend - Payout ratio description | object  |
            | dividend_yield                       | Cash dividend - Dividend yield           | float |
            | earnings_per_share                   | Earnings per share                      | float |
            | net_asset_value_per_share            | Net asset value per share               | float |
            | surplus_reserve_fund_per_share       | Surplus reserve fund per share          | float |
            | undistributed_profit_per_share       | Undistributed profit per share          | float |
            | net_profit_growth_rate               | Net profit growth rate (YoY)            | float |
            | total_shares_outstanding             | Total shares outstanding                | int   |
            | preliminary_plan_announcement_date   | Preliminary plan announcement date      | object  |
            | record_date                          | Record date                             | object  |
            | ex_dividend_date                     | Ex-dividend and ex-rights date          | object  |
            | proposal_progress                    | Proposal progress                       | object  |
            | latest_announcement_date             | Latest announcement date                | object  |
    """

    return stocks_common_metrics.get_stock_fhps_detail(stock_code)

# ----------------- 新闻报告类。用于获取股票相关的新闻报道。 ----------------- #
@mcp.tool()
def stock_news(stock_code: str, start_date: Optional[ str] = None, end_date: Optional[ str] = None) -> List[Dict[str, Any]]:
    """
    Fetch the latest news articles and information related to a specific stock within a specified date range.

    Args:
        stock_code: Stock code, e.g., "000001".
        start_date: The start date of the query, formatted as 'YYYY-MM-DD'. If not provided, it defaults to one week before the current date.
        end_date: The end date of the query, formatted as 'YYYY-MM-DD'. If not provided, it defaults to the current date.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a news article record.
        Each dictionary contains the following elements:
            | keyword       | str  | Keywords |
            | title         | str  | News Title |
            | content       | str  | News Content |
            | publish_time  | str  | Publication Time (format: YYYY-MM-DD HH:MM:SS) |
            | source        | str  | Source of the Article |
            | url           | str  | URL Link to the News Article |
    """

    return news_report.stock_news(stock_code)

@mcp.tool()
def financial_news(start_date: Optional[ str] = None, end_date: Optional[ str] = None) -> List[Dict[str, Any]]:
    """
    Fetch the latest financial news and market trends.

    Args:
        start_date: The start date of the query, formatted as 'YYYY-MM-DD'. If not provided, it defaults to one week before the current date.
        end_date: The end date of the query, formatted as 'YYYY-MM-DD'. If not provided, it defaults to the current date.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a news record.
        Each dictionary contains the following elements:
            | title         | str  | News Title |
            | content       | str  | News Content |
            | pub_time      | str  | Publication Time (format: YYYY-MM-DD HH:MM:SS) |
            | url           | str  | URL Link to the News Article |
    """

    return news_report.financial_news(start_date, end_date)


# Start the MCP server
if __name__ == "__main__":
    print(f"ASkare Stocks MCP Server starting...")
    mcp.run()
