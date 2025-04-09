import pandas as pd
import akshare as ak
import re
from typing import Any, Dict, List, Optional, Union

from .modules import DateValidator, StockCode, StockPricedata, FinancialAbstract, FhpsDetail

class StocksCommonMetrics:
    """
    股票常用指标类。
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def get_stock_code(self, name: str)  -> List[Dict[str, Any]]:
        """
        获取中国 A 股上市公司股票代码

        Args:
            name: 股票名称

        Returns:
            List[Dict[str, Any]]: 返回字典的列表，每个字典表示一家上市公司的股票名称及股票代码。每条记录包含以下字段: 
                | name          | str  | 股票名称 |
                | stock_code    | str  | 股票代码 |
        """
        result = []
        for stock_data in [
                ak.stock_info_a_code_name()
        ]:
            result.extend(
                [
                    {"name": item['name'], "stock_code": item['code']}
                    for item in stock_data[["name", "code"]].to_dict(orient="records")
                    if re.search(name, item['name'])
                ]
            )

        stock_codes = [StockCode(**row).model_dump() for row in result]

        return stock_codes
    
    def get_stock_zygc_em(self, stock_code: str)  -> Dict[str, Any]:
        """
        获取中国A股上市公司的主要经营业务结构，用于分析公司的核心业务、产品和服务及其收入占比

        Args:
            stock_code: 股票代码，例如 "SH688041"。

        Returns:
            Dict[str, Any]: 返回一个字典，每条记录包含以下字段: 

        名称	类型	描述
        股票代码	object	-
        报告日期	object	-
        分类类型	object	-
        主营构成	int64	-
        主营收入	float64	注意单位: 元
        收入比例	float64	-
        主营成本	float64	注意单位: 元
        成本比例	float64	-
        主营利润	float64	注意单位: 元
        利润比例	float64	-
        毛利率	float64	-
        """

        stock_zygc_em_df = ak.stock_zygc_em(symbol="SH688041")
        print(stock_zygc_em_df)


    def get_historical_stockprice_data(self, 
                                       stock_code: str ,
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
          List[Dict[str, Any]]: 返回字典的列表，每个字典表示一个周期股票价格。每条记录包含以下字段：
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
        if not DateValidator(date=start_date).validate_date_format(start_date) or not DateValidator(date=end_date).validate_date_format(end_date):
            raise ValueError(f"日期格式错误，应为 YYYYMMDD，实际输入：{start_date} 或 {end_date}")

        result = ak.stock_zh_a_hist(symbol=stock_code, 
                                    period=period, 
                                    start_date=start_date, 
                                    end_date=end_date, 
                                    adjust=adjust)
        column_mapping = {
            "日期": "date",
            "股票代码": "stock_code",
            "开盘": "open",
            "收盘": "close",
            "最高": "high",
            "最低": "low",
            "成交量": "volume", 
            "成交额": "turnover",
            "振幅": "amplitude",
            "涨跌幅": "change_rate",
            "涨跌额": "change_amount",
            "换手率": "turnover_rate"
        }
        result.rename(columns=column_mapping, inplace=True)
        result['date'] = pd.to_datetime(result['date'])

        stock_hist = result.apply(lambda row: StockPricedata(**row).model_dump(), axis=1).tolist()

        return stock_hist


    def get_stock_financial_abstract(self,
                                     stock_code: str ,
                                     indicator: Optional[str] = '按报告期')  -> List[Dict[str, Any]]:
        """
        获取中国 A 股上市公司的财务报告概要数据。

        Args:
            stock_code: 股票代码
            indicator: 指标类型，可选值: {'按报告期', '按年度', '按单季度'}

        Returns:
            List[Dict[str, Any]]: 返回字典的列表，每个字典表示一条财务概要记录。每条记录包含以下字段：
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

        result = ak.stock_financial_abstract_ths(symbol=stock_code, indicator=indicator)
        column_mapping = {
            "报告期" : "reporting_period",
            "净利润" : "net_profit",
            "净利润同比增长率" : "net_profit_growth_rate",
            "扣非净利润" : "non_recurring_net_profit",
            "扣非净利润同比增长率" : "non_recurring_net_profit_growth_rate",
            "营业总收入" : "total_operating_revenue",
            "营业总收入同比增长率" : "total_operating_revenue_growth_rate",
            "基本每股收益" : "basic_earnings_per_share",
            "每股净资产" : "net_asset_per_share",
            "每股资本公积金" : "capital_reserve_fund_per_share" ,
            "每股未分配利润" : "undistributed_profit_per_share" ,
            "每股经营现金流" : "operating_cash_flow_per_share" ,
            "销售净利率" : "net_profit_margin" ,
            "销售毛利率" : "gross_profit_margin",
            "净资产收益率" : "return_on_equity_of_roe" ,
            "净资产收益率-摊薄" : "diluted_return_on_equity_of_roe" ,
            "营业周期" : "operating_cycle" ,
            "存货周转率" : "inventory_turnover_ratio" ,
            "存货周转天数" : "days_inventory_outstanding" ,
            "应收账款周转天数" : "days_sales_outstanding" ,
            "流动比率" : "current_ratio" ,
            "速动比率" : "quick_ratio" ,
            "保守速动比率" : "conservative_quick_ratio" ,
            "产权比率" : "debt_to_equity_ratio" ,
            "资产负债率" : "asset_to_liability_ratio" ,
        }
        result.rename(columns=column_mapping, inplace=True)
        financial_abstracts = result.apply(lambda row: FinancialAbstract(**row).model_dump(), axis=1).tolist()
        
        return financial_abstracts

    def get_stock_margin_detail(self, stock_code: str, start_date: str, end_date: str, freq: str = "D") -> List[Dict[str, Any]]:
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
            List[Dict[str, Any]]: 返回字典的列表，每个字典表示一个交易日的融资融券概要。每条记录包含以下字段：
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
        # 初始化空的 DataFrame 用于存储所有数据
        all_filtered_df = pd.DataFrame()

        # 定义字段映射（中文字段名 -> 英文字段名）
        column_mapping = {
            "信用交易日期": "trading_date",
            "标的证券代码": "target_security_code",
            "标的证券简称": "target_security_name",
            "融资余额": "margin_balance",
            "融资买入额": "margin_buy_amount",
            "融资偿还额": "margin_repayment",
            "融券余量": "short_selling_balance",
            "融券卖出量": "short_selling_volume",
            "融券偿还量": "short_selling_repayment",
        }

        # 将日期范围转换为日期列表
        for date in pd.date_range(start=start_date, end=end_date, freq=freq):
            # 格式化日期为字符串
            data_date = date.strftime('%Y%m%d')

            try:
                # 获取当天的融资融券数据
                stock_margin_detail_sse_df = ak.stock_margin_detail_sse(date=data_date)

                # 检查返回的数据是否为空
                if stock_margin_detail_sse_df is None or stock_margin_detail_sse_df.empty:
                    print(f"No data for date: {data_date}")
                    continue  # 跳过没有数据的日期

                # 过滤证券代码为指定的 stock_code
                filtered_df = stock_margin_detail_sse_df[
                    stock_margin_detail_sse_df['标的证券代码'] == stock_code
                ].copy()

                # 再次检查过滤后的数据是否为空
                if filtered_df is None or filtered_df.empty:
                    print(f"No data for stock code {stock_code} on date: {data_date}")
                    continue  # 跳过没有匹配数据的日期

                # 翻译字段名为英文
                filtered_df.rename(columns=column_mapping, inplace=True)

                # 将当天数据添加到总数据中
                all_filtered_df = pd.concat([all_filtered_df, filtered_df], ignore_index=True)

            except Exception as e:
                print(f"Error fetching data for date {data_date}: {e}")
                continue  # 跳过发生错误的日期

        # 将 DataFrame 转换为字典列表
        result = all_filtered_df.to_dict(orient="records")

        return result

    def get_stock_fhps_detail(self, stock_code: str) -> List[Dict[str, Any]]:
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

        result = ak.stock_fhps_detail_em(symbol=stock_code)
        column_mapping = {
            "报告期": "reporting_period",
            "业绩披露日期": "earnings_disclosure_date",
            "送转股份-送转总比例": "total_share_conversion_ratio",
            "送转股份-送股比例": "bonus_share_ratio",
            "送转股份-转股比例": "capitalization_ratio",
            "现金分红-现金分红比例": "cash_dividend_payout_ratio",
            "现金分红-现金分红比例描述": "cash_dividend_payout_ratio_description",
            "现金分红-股息率": "dividend_yield",
            "每股收益": "earnings_per_share",
            "每股净资产": "net_asset_value_per_share",
            "每股公积金": "surplus_reserve_fund_per_share",
            "每股未分配利润": "undistributed_profit_per_share",
            "净利润同比增长": "net_profit_growth_rate",
            "总股本": "total_shares_outstanding",
            "预案公告日": "preliminary_plan_announcement_date",
            "股权登记日": "record_date",
            "除权除息日": "ex_dividend_date",
            "方案进度": "proposal_progress",
            "最新公告日期": "latest_announcement_date",
        }
        result.rename(columns=column_mapping, inplace=True)
        fhps_detail = result.apply(lambda row: FhpsDetail(**row).model_dump(), axis=1).tolist()

        return fhps_detail


if __name__ == "__main__":
    # 示例用法
    # 创建 StockUtils 实例
    stockutils = StocksCommonMetrics()
    # 获取股票名称及股票代码
    stock_codes = stockutils.get_stock_code(name="华泰证券")

    if stock_codes:
        stock_code = []
        for item in stock_codes:

            # 获取股票代码
            stock_code= item['stock_code']
            print(f"处理股票代码：{stock_code}")

            # 获取股价历史数据
            historical_stockprice_data = stockutils.get_historical_stockprice_data(stock_code=stock_code, start_date="20230101", end_date="20231001")
            print(historical_stockprice_data)
            
            # 获取财务概要数据
            stock_financial_abstract = stockutils.get_stock_financial_abstract(stock_code=stock_code, indicator='按报告期')
            print(stock_financial_abstract)

            # 获取融资融券明细数据
            stock_margin_detail = stockutils.get_stock_margin_detail(stock_code=stock_code, start_date="20230102", end_date="20230110")
            print(stock_margin_detail)
    else:
        print("No stock codes found.")
