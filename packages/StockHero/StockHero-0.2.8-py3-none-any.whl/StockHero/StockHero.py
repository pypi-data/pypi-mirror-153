# -*- coding: utf-8 -*-
"""
Created on Thursday Jun 05 2022

@author: RobWen
Version: 0.2.8
"""
import pandas as pd
import requests
from pandas import json_normalize
from bs4 import BeautifulSoup
import numpy as np

    ##############
    ###        ###
    ###  Data  ###
    ###        ###
    ##############

class Ticker:
    
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = self.__get_data()
        self.__laenge()
        self.headers_standard = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"}
    
    def __repr__(self):
        return(self.ticker)
        
    def __str__(self):
        return(self.ticker)
        #return(self.ticker or '') # by None
       
    @property
    def financials(self):
        return self.__morningstar_financials()
    
    @property
    def marginofsales(self):
        return self.__morningstar_margins_of_sales()
    
    @property
    def profitability(self):
        return self.__morningstar_profitability()
    
    @property
    def growth_rev(self):
        return self.__morningstar_growth_revenue()
    
    @property
    def growth_op_inc(self):
        return self.__morningstar_growth_operating_income()
    
    @property
    def growth_net_inc(self):
        return self.__morningstar_growth_net_income()
    
    @property
    def growth_eps(self):
        return self.__morningstar_growth_eps()
    
    @property
    def cf_ratios(self):
        return self.__morningstar_cashflow_ratios()
    
    @property
    def bs(self):
        return self.__morningstar_finhealth_bs()
    
    @property
    def li_fin(self):
        return self.__morningstar_finhealth_health()
    
    @property
    def efficiency(self):
        return self.__morningstar_effiency_ratios()
    
    @property
    def morningstar_quote(self):
        return self.__morningstar_quote_df()
    
    @property
    def nasdaq_summ(self):
        return self.__nasdaq_summary_df()
    
    @property
    def nasdaq_div_hist(self):
        return self.__nasdaq_dividend_history_df()
    
    @property
    def nasdaq_hist_quotes_stock(self):
        return self.__nasdaq_historical_data_stock_df()
    
    @property
    def nasdaq_hist_quotes_etf(self):
        return self.__nasdaq_historical_data_etf_df()
    
    @property
    def nasdaq_hist_nocp(self):
        return self.__nasdaq_historical_nocp_df()
    
    @property
    def nasdaq_fin_income_statement_y(self):
        return self.__nasdaq_financials_income_statement_y_df()
    
    @property
    def nasdaq_fin_balance_sheet_y(self):
        return self.__nasdaq_financials_balance_sheet_y_df()
    
    @property
    def nasdaq_fin_cash_flow_y(self):
        return self.__nasdaq_financials_cash_flow_y_df()
    
    @property
    def nasdaq_fin_fin_ratios_y(self):
        return self.__nasdaq_financials_financials_ratios_y_df()
    
    @property
    def nasdaq_fin_income_statement_q(self):
        return self.__nasdaq_financials_income_statement_q_df()
    
    @property
    def nasdaq_fin_balance_sheet_q(self):
        return self.__nasdaq_financials_balance_sheet_q_df()
    
    @property
    def nasdaq_fin_cash_flow_q(self):
        return self.__nasdaq_financials_cash_flow_q_df()
    
    @property
    def nasdaq_fin_fin_ratios_q(self):
        return self.__nasdaq_financials_financials_ratios_q_df()
    
    @property
    def nasdaq_earn_date_eps(self):
        return self.__nasdaq_earnings_date_eps_df()
    
    @property
    def nasdaq_earn_date_surprise(self):
        return self.__nasdaq_earnings_date_surprise_df()
    
    @property
    def nasdaq_yearly_earn_forecast(self):
        return self.__nasdaq_earnings_date_yearly_earnings_forecast_df()
    
    @property
    def nasdaq_quarterly_earn_forecast(self):
        return self.__nasdaq_earnings_date_quarterly_earnings_forecast_df()
    
    @property
    def nasdaq_pe_peg_forecast(self):
        return self.__forecast_pe_peg_df()
    
    @property
    def yahoo_statistics(self):
        return self.__yahoo_statistics_df()
    
    @property
    def yahoo_statistics_p(self):
        return self.__yahoo_statistics_df_p()
    
    @property
    def gurufocus_pe_ratio_av(self):
        return self.__gurufocus_pe_ratio_av_v()
    
    @property
    def gurufocus_debt_to_ebitda(self):
        return self.__gurufocus_debt_to_ebitda()
    
    
    #####################
    ###               ###
    ###  Morningstar  ###
    ###               ###
    #####################
    
    def __get_data(self):
        
        headers = {'Referer': f'http://financials.morningstar.com/ratios/r.html?t={self.ticker}'}
        r = requests.get(f"http://financials.morningstar.com/finan/ajax/exportKR2CSV.html?&t={self.ticker}", headers=headers)
        csvdatei = r.content
        
        my_decoded_str = csvdatei.decode()
        my_decoded_str = my_decoded_str.split()
        
        return my_decoded_str
    
    def __laenge(self):
        if len(self.data) == 304:
            self.length = 0
        elif len(self.data) == 305:
            self.length = 1
        elif len(self.data) == 306:
            self.length = 2
        elif len(self.data) == 307:
            self.length = 3
        elif len(self.data) == 308:
            self.length = 4
        else:
            self.length = 5
    
    ### Morningstar Quote                                       ###
    ### e.g. https://www.morningstar.com/stocks/xnas/nvda/quote ###
    ### Rückgabe None implementiert und getestet                ###
    ### Ungültige Werte = NaN implementiert                     ###
    def __morningstar_quote_df(self):
        
        if Ticker.__stock_exchange(self) != None:
            if Ticker.__stock_exchange(self).split(':')[0] == 'NAS':
                url = f'https://www.morningstar.com/stocks/xnas/{self.ticker}/quote'
            elif Ticker.__stock_exchange(self).split(':')[0] == 'NYSE':
                url = f'https://www.morningstar.com/stocks/xnys/{self.ticker}/quote'
        else:
            return None
        
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        string = page.find_all(text=True)[-4].replace('"','').strip().split(',')
        
        for n,i in enumerate(string):
            if string[n] == 'Qual' or string[n] == 'Quant':
                parameter = n
                break
            else:
                parameter = None
            
        if parameter == None:
            df_morningstar_quote = None
        else:
            morningstar_performance_id = string[parameter+1]
            
            url = f'https://api-global.morningstar.com/sal-service/v1/stock/header/v2/data/{morningstar_performance_id}/securityInfo?showStarRating=&languageId=en&locale=en&clientId=MDC&benchmarkId=category&component=sal-components-quote&version=3.49.0'
            
            headers = {
                'ApiKey': 'lstzFDEOhfFNMLikKa0am9mgEKLBl49T',
            }
            
            r = requests.get(url, headers=headers)
            dictionary = r.json()
            
            priceEarnings = dictionary["priceEarnings"]
            priceBook = dictionary["priceBook"]
            priceSale = dictionary["priceSale"]
            forwardPE = dictionary["forwardPE"]
            forwardDivYield = dictionary["forwardDivYield"]
            
            url = f'https://api-global.morningstar.com/sal-service/v1/stock/keyStats/{morningstar_performance_id}?languageId=en&locale=en&clientId=MDC&benchmarkId=category&component=sal-components-quote&version=3.49.0'
            
            headers = {
                'ApiKey': 'lstzFDEOhfFNMLikKa0am9mgEKLBl49T',
            }
            
            r = requests.get(url, headers=headers)
            json = r.json()
            
            revenue3YearGrowth = json['revenue3YearGrowth']['stockValue']
            netIncome3YearGrowth = json['netIncome3YearGrowth']['stockValue']
            operatingMarginTTM = json['operatingMarginTTM']['stockValue']
            netMarginTTM = json['netMarginTTM']['stockValue']
            roaTTM = json['roaTTM']['stockValue']
            roeTTM = json['roeTTM']['stockValue']
            freeCashFlowTTM = json['freeCashFlow']['cashFlowTTM']
            
            try:
                priceEarnings = '{:.2f}'.format(float(priceEarnings))
                priceBook = '{:.2f}'.format(float(priceBook))
                priceSale = '{:.2f}'.format(float(priceSale))
                forwardPE = '{:.2f}'.format(float(forwardPE))
                forwardDivYield = float(forwardDivYield) * 100 # in %
                revenue3YearGrowth = '{:.2f}'.format(float(revenue3YearGrowth))
                netIncome3YearGrowth = '{:.2f}'.format(float(netIncome3YearGrowth))
                operatingMarginTTM = '{:.2f}'.format(float(operatingMarginTTM))
                netMarginTTM = '{:.2f}'.format(float(netMarginTTM))
                roaTTM = '{:.2f}'.format(float(roaTTM))
                roeTTM = '{:.2f}'.format(float(roeTTM))
                freeCashFlowTTM = '{:,.2f}'.format(float(freeCashFlowTTM)) # locale='en_US'
            except(TypeError):
                pass
            
            df_morningstar_quote = pd.DataFrame([priceEarnings, priceBook, priceSale, forwardPE, forwardDivYield
                               , revenue3YearGrowth, netIncome3YearGrowth, operatingMarginTTM, netMarginTTM, roaTTM, roeTTM
                               , freeCashFlowTTM]
                              , index =['Price/Earnings', 'Price/Book', 'Price/Sales', 'Consensus Forward P/E', 'Forward Div Yield %'
                                        , 'Rev 3-Yr Growth', 'Net Income 3-Yr Growth'
                                        , 'Operating Margin % TTM', 'Net Margin % TTM', 'ROA % TTM'
                                        , 'ROE % TTM', 'Current Free Cash Flow']
                              , columns =[self.ticker + ' Ratio'])
            
            df_morningstar_quote = df_morningstar_quote.fillna(value=np.nan) # None mit NaN ersetzen für df
        
        # Rückgabe
        self.__df_morningstar_quote = df_morningstar_quote
        
        return self.__df_morningstar_quote
    
    ### Morningstar Financials                                      ###
    ### e.g. http://financials.morningstar.com/ratios/r.html?t=NVDA ###
    ### Rückgabe None implementiert und getestet                    ###
    ### Ungültige Werte = NaN implementiert                         ###
    def __morningstar_financials(self):
                
        data = self.data
        length = self.length
            
        if len(data) == 0:
            self.df_morningstar_financials = None
        else:
            self.df_morningstar_financials = pd.DataFrame([Ticker.__data_list(data[12+length]), Ticker.__data_list(data[15+length])
                                            , Ticker.__data_list(data[19+length]), Ticker.__data_list(data[22+length])
                                            , Ticker.__data_list(data[26+length]), Ticker.__data_list(data[30+length])
                                            , Ticker.__data_list(data[32+length]), Ticker.__data_list(data[36+length])
                                            , Ticker.__data_list(data[38+length]), Ticker.__data_list(data[44+length])
                                            , Ticker.__data_list(data[49+length]), Ticker.__data_list(data[53+length])
                                            , Ticker.__data_list(data[58+length]), Ticker.__data_list(data[65+length])
                                            , Ticker.__data_list(data[69+length])]
                          , index =[Ticker.__index(data[10+length] + ' ' + data[11+length] + ' ' + data[12+length])
                                    , Ticker.__index(data[13+length] + ' ' + data[14+length] + ' ' + data[15+length])
                                    , Ticker.__index(data[16+length] + ' ' + data[17+length] + ' ' + data[18+length]+ ' ' + data[19+length])
                                    , Ticker.__index(data[20+length] + ' ' + data[21+length] + ' ' + data[22+length])
                                    , Ticker.__index(data[23+length] + ' ' + data[24+length] + ' ' + data[25+length]+ ' ' + data[26+length])
                                    , Ticker.__index(data[27+length] + ' ' + data[28+length] + ' ' + data[29+length]+ ' ' + data[30+length])
                                    , Ticker.__index(data[31+length] + ' ' + data[32+length])
                                    , Ticker.__index(data[33+length] + ' ' + data[34+length] + ' ' + data[35+length]+ ' ' + data[36+length])
                                    , Ticker.__index(data[37+length] + ' ' + data[38+length])
                                    , Ticker.__index(data[39+length] + ' ' + data[40+length] + ' ' + data[41+length]+ ' ' + data[42+length]+ ' ' + data[43+length]+ ' ' + data[44+length])
                                    , Ticker.__index(data[45+length] + ' ' + data[46+length] + ' ' + data[47+length]+ ' ' + data[48+length]+ ' ' + data[49+length])
                                    , Ticker.__index(data[50+length] + ' ' + data[51+length] + ' ' + data[52+length]+ ' ' + data[53+length])
                                    , Ticker.__index(data[54+length] + ' ' + data[55+length] + ' ' + data[56+length]+ ' ' + data[57+length]+ ' ' + data[58+length])
                                    , Ticker.__index(data[59+length] + ' ' + data[60+length] + ' ' + data[61+length]+ ' ' + data[62+length]+ ' ' + data[53+length]+ ' ' + data[64+length]+ ' ' + data[65+length])
                                    , Ticker.__index(data[66+length] + ' ' + data[67+length] + ' ' + data[68+length]+ ' ' + data[69+length])]
                          , columns = Ticker.__data_list(data[8+length] + data[9+length]))
        
        # There is a bug somewhere =D
        if self.df_morningstar_financials.iloc[-1,-1] == None:
            self.df_morningstar_financials.iloc[-1,-1] = np.nan
    
        return self.df_morningstar_financials
    
    ### Morningstar Margins % of Sales ###
    ### e.g. http://financials.morningstar.com/ratios/r.html?t=NVDA ###
    ### Rückgabe None implementiert und getestet ###
    ### Ungültige Werte = NaN implementiert ###
    def __morningstar_margins_of_sales(self):
        
        data = self.data
        length = self.length
        
        if len(data) == 0:
            self.morningstar_margins_of_sales = None
        else:
            self.morningstar_margins_of_sales = pd.DataFrame([Ticker.__data_list(data[78+length]), Ticker.__data_list(data[79+length])
                                                  , Ticker.__data_list(data[81+length]), Ticker.__data_list(data[82+length])
                                                  , Ticker.__data_list(data[83+length]), Ticker.__data_list(data[84+length])
                                                  , Ticker.__data_list(data[86+length]), Ticker.__data_list(data[91+length])
                                                  , Ticker.__data_list(data[93+length])]
                              , index =['Revenue', 'COGS', 'Gross Margin', 'SG&A'
                                        , 'R&D', 'Other', 'Operating Margin', 'Net Int Inc & Other', 'EBT Margin']
                              , columns = Ticker.__data_list(data[77+length]))
        
        return self.morningstar_margins_of_sales
    
    ### Morningstar Profitability                                   ###
    ### e.g. http://financials.morningstar.com/ratios/r.html?t=NVDA ###
    ### Rückgabe None implementiert und getestet                    ###
    ### Ungültige Werte = NaN implementiert                         ###
    def __morningstar_profitability(self):
        
        data = self.data
        length = self.length
    
        if len(data) == 0:
            self.morningstar_profitability = None
        else:
            self.morningstar_profitability = pd.DataFrame([Ticker.__data_list(data[97+length]), Ticker.__data_list(data[100+length])
                                               , Ticker.__data_list(data[103+length]), Ticker.__data_list(data[107+length])
                                               , Ticker.__data_list(data[110+length]), Ticker.__data_list(data[114+length])
                                               , Ticker.__data_list(data[119+length]), Ticker.__data_list(data[121+length])]
                          , index =['Tax Rate %', 'Net Margin %', 'Asset Turnover (Average)', 'Return on Assets %'
                                    , 'Financial Leverage (Average)', 'Return on Equity %', 'Return on Invested Capital %'
                                    ,'Interest Coverage']
                          , columns = Ticker.__data_list(data[94+length]))
    
        return self.morningstar_profitability
    
    ### Morningstar Growth - Revenue %                              ###
    ### e.g. http://financials.morningstar.com/ratios/r.html?t=NVDA ###
    ### Rückgabe None implementiert und getestet                    ###
    ### Ungültige Werte = NaN implementiert                         ###
    def __morningstar_growth_revenue(self):
        
        data = self.data
        length = self.length
        
        if len(data) == 0:
            self.morningstar_growth_revenue = None
        else:
            self.morningstar_growth_revenue = pd.DataFrame([Ticker.__data_list(data[132+length]), Ticker.__data_list(data[134+length])
                                                , Ticker.__data_list(data[136+length]), Ticker.__data_list(data[138+length])]
                          , index =['Year over Year', '3-Year Average', '5-Year Average', '10-Year Average']
                          , columns = Ticker.__data_list(data[125+length] + data[126+length] + ' ' + data[127+length]))
    
        return self.morningstar_growth_revenue
    
    ### Morningstar Growth - Operating Income %                     ###
    ### e.g. http://financials.morningstar.com/ratios/r.html?t=NVDA ###
    ### Rückgabe None implementiert und getestet                    ###
    ### Ungültige Werte = NaN implementiert                         ###
    def __morningstar_growth_operating_income(self):
        
        data = self.data
        length = self.length
        
        if len(data) == 0:
            self.morningstar_growth_operating_income = None
        else:
            self.morningstar_growth_operating_income = pd.DataFrame([Ticker.__data_list(data[144+length]), Ticker.__data_list(data[146+length])
                                                         , Ticker.__data_list(data[148+length]), Ticker.__data_list(data[150+length])]
                            , index =['Year over Year', '3-Year Average', '5-Year Average', '10-Year Average']
                            , columns = Ticker.__data_list(data[125+length] + data[126+length] + ' ' + data[127+length]))
    
        return self.morningstar_growth_operating_income
    
    ### Morningstar Growth - Net Income %                           ###
    ### e.g. http://financials.morningstar.com/ratios/r.html?t=NVDA ###
    ### Rückgabe None implementiert und getestet                    ###
    ### Ungültige Werte = NaN implementiert                         ###
    def __morningstar_growth_net_income(self):
        
        data = self.data
        length = self.length
        
        if len(data) == 0:
            self.morningstar_growth_net_income = None
        else:
            try: 
                self.morningstar_growth_net_income = pd.DataFrame([Ticker.__data_list(data[156+length]), Ticker.__data_list(data[158+length])
                                                       , Ticker.__data_list(data[160+length]), Ticker.__data_list(data[162+length])]
                              , index =['Year over Year', '3-Year Average', '5-Year Average', '10-Year Average']
                              , columns = Ticker.__data_list(data[125+length] + data[126+length] + ' ' + data[127+length]))
            except(ValueError):
                Ticker.__data_list(data[156+length]).append(None)
                self.morningstar_growth_net_income = pd.DataFrame([Ticker.__data_list(data[156+length]), Ticker.__data_list(data[158+length])
                                                       , Ticker.__data_list(data[160+length]), Ticker.__data_list(data[162+length])]
                              , index =['Year over Year', '3-Year Average', '5-Year Average', '10-Year Average']
                              , columns = Ticker.__data_list(data[125+length] + data[126+length] + ' ' + data[127+length]))
    
        return self.morningstar_growth_net_income
    
    ### Morningstar Growth - EPS %                                  ###
    ### e.g. http://financials.morningstar.com/ratios/r.html?t=NVDA ###
    ### Rückgabe None implementiert und getestet                    ###
    ### Ungültige Werte = NaN implementiert                         ###
    def __morningstar_growth_eps(self):
        
        data = self.data
        length = self.length
    
        if len(data) == 0:
            self.morningstar_growth_eps = None
        else:
            self.morningstar_growth_eps = pd.DataFrame([Ticker.__data_list(data[167+length]), Ticker.__data_list(data[169+length])
                                            , Ticker.__data_list(data[171+length]), Ticker.__data_list(data[173+length])]
                          , index =['Year over Year', '3-Year Average', '5-Year Average', '10-Year Average']
                          , columns = Ticker.__data_list(data[125+length] + data[126+length] + ' ' + data[127+length]))
    
        return self.morningstar_growth_eps
        
    ### Morningstar Cash Flow - Cash Flow Ratios                    ###
    ### e.g. http://financials.morningstar.com/ratios/r.html?t=NVDA ###
    ### Rückgabe None implementiert und getestet                    ###
    ### Ungültige Werte = NaN implementiert                         ###
    def __morningstar_cashflow_ratios(self):
        
        data = self.data
        length = self.length
        
        if len(data) == 0:
            self.morningstar_cashflow_ratios = None
        else:
            self.morningstar_cashflow_ratios = pd.DataFrame([Ticker.__data_list(data[187+length]), Ticker.__data_list(data[193+length])
                                                 , Ticker.__data_list(data[204+length]), Ticker.__data_list(data[204+length])
                                                 , Ticker.__data_list(data[208+length])]
                          , index =['Operating Cash Flow Growth % YOY', 'Free Cash Flow Growth % YOY', 'Cap Ex as a % of Sales'
                                    , 'Free Cash Flow/Sales %', 'Free Cash Flow/Net Income']
                          , columns =Ticker.__data_list(data[181+length]))
    
        return self.morningstar_cashflow_ratios
    
    ### Morningstar Cash Flow - Balance Sheet Items (in %)          ###
    ### e.g. http://financials.morningstar.com/ratios/r.html?t=NVDA ###
    ### Rückgabe None implementiert und getestet                    ###
    ### Ungültige Werte = NaN implementiert                         ###
    def __morningstar_finhealth_bs(self):
        
        data = self.data
        length = self.length
        
        if len(data) == 0:
            self.morningstar_finhealth_bs = None
        else:
            self.morningstar_finhealth_bs = pd.DataFrame([Ticker.__data_list(data[223+length]), Ticker.__data_list(data[225+length])
                                              , Ticker.__data_list(data[226+length]), Ticker.__data_list(data[229+length])
                                              , Ticker.__data_list(data[232+length]), Ticker.__data_list(data[234+length])
                                              , Ticker.__data_list(data[235+length]), Ticker.__data_list(data[238+length])
                                              , Ticker.__data_list(data[240+length]), Ticker.__data_list(data[242+length])
                                              , Ticker.__data_list(data[244+length]), Ticker.__data_list(data[246+length])
                                              , Ticker.__data_list(data[248+length]), Ticker.__data_list(data[251+length])
                                              , Ticker.__data_list(data[254+length]), Ticker.__data_list(data[256+length])
                                              , Ticker.__data_list(data[259+length]), Ticker.__data_list(data[261+length])
                                              , Ticker.__data_list(data[264+length]), Ticker.__data_list(data[268+length])]
                              , index =['Cash & Short-Term Investments', 'Accounts Receivable', 'Inventory', 'Other Current Assets'
                                        , 'Total Current Assets', 'Net PP&E', 'Intangibles', 'Other Long-Term Assets', 'Total Assets'
                                        , 'Accounts Payable', 'Short-Term Debt', 'Taxes Payable', 'Accrued Liabilities'
                                        , 'Other Short-Term Liabilities', 'Total Current Liabilities', 'Long-Term Debt', 'Other Long-Term Liabilities'
                                        ,'Total Liabilities', "Total Stockholder's Equity", 'Total Liabilities & Equity']
                              , columns = Ticker.__data_list(data[218+length] + ' ' + data[219+length]))
    
        return self.morningstar_finhealth_bs
        
    ### Morningstar Cash Flow - Liquidity/Financial Health          ###
    ### e.g. http://financials.morningstar.com/ratios/r.html?t=NVDA ###
    ### Rückgabe None implementiert und getestet                    ###
    ### Ungültige Werte = NaN implementiert                         ###
    def __morningstar_finhealth_health(self):
        
        data = self.data
        length = self.length
        
        if len(data) == 0:
            self.morningstar_finhealth_health = None
        else:
            self.morningstar_finhealth_health = pd.DataFrame([Ticker.__data_list(data[273+length]), Ticker.__data_list(data[275+length])
                                                  , Ticker.__data_list(data[277+length]), Ticker.__data_list(data[278+length])]
                              , index =['Current Ratio', 'Quick Ratio', 'Financial Leverage', 'Debt/Equity']
                              , columns = Ticker.__data_list(data[270+length] + ' ' + data[271+length]))
        
        return self.morningstar_finhealth_health
    
    ### Morningstar Cash Flow - Efficiency                          ###
    ### e.g. http://financials.morningstar.com/ratios/r.html?t=NVDA ###
    ### Rückgabe None implementiert und getestet                    ###
    ### Ungültige Werte = NaN implementiert                         ###
    def __morningstar_effiency_ratios(self):
        
        data = self.data
        length = self.length
        
        if len(data) == 0:
            self.morningstar_effiency_ratios = None
        else:
            self.morningstar_effiency_ratios = pd.DataFrame([Ticker.__data_list(data[287+length]), Ticker.__data_list(data[289+length])
                                                 , Ticker.__data_list(data[291+length]), Ticker.__data_list(data[294+length])
                                                 , Ticker.__data_list(data[296+length]), Ticker.__data_list(data[298+length])
                                                 , Ticker.__data_list(data[301+length]), Ticker.__data_list(data[303+length])]
                          , index =['Days Sales Outstanding', 'Days Inventory', 'Payables Period', 'Cash Conversion Cycle'
                                    , 'Receivables Turnover', 'Inventory Turnover', 'Fixed Assets Turnover', 'Asset Turnover']
                          , columns = Ticker.__data_list(data[284+length]))
    
        return self.morningstar_effiency_ratios
    
    def __data_list(string):
        if '"' in string:
            substrings = []
            for s_quote_mark in string.split('"'):
                if len(s_quote_mark)>0: 
                    if s_quote_mark[0]=="," or s_quote_mark[-1]=="," or s_quote_mark==string:
                        for s_comma in s_quote_mark.split(','):
                            if len(s_comma)>0:
                                substrings.append(s_comma)
                            #else:
                            #    substrings.append(None)
                    else:
                        substrings.append(s_quote_mark)
        else: 
            substrings = string.split(',')
    
            for n, i in enumerate(substrings):
	            if len(substrings[n]) == 0:
		            substrings[n] = np.nan
        
        del substrings[0]
    
        return substrings
    
    def __index(string):
        string = string.split(',')
        return string[0]
    
    ################
    ###          ###
    ###  NASDAQ  ###
    ###          ###
    ################
    
    ### Nasdaq Summary                                          ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda ###
    ### Rückgabe None implementiert und getestet                ###
    def __nasdaq_summary_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/summary?assetclass=stocks", headers=self.headers_standard)
        try:
            json = r.json()
            
            if json['data'] != None:
                
                json_data_1 = json['data']['summaryData']['Exchange']
                json_data_2 = json['data']['summaryData']['Sector']
                json_data_3 = json['data']['summaryData']['Industry']
                json_data_4 = json['data']['summaryData']['OneYrTarget']
                json_data_5 = json['data']['summaryData']['TodayHighLow']
                json_data_6 = json['data']['summaryData']['ShareVolume']
                json_data_7 = json['data']['summaryData']['AverageVolume']
                json_data_8 = json['data']['summaryData']['PreviousClose']
                json_data_9 = json['data']['summaryData']['FiftTwoWeekHighLow']
                json_data_10 = json['data']['summaryData']['MarketCap']
                json_data_11 = json['data']['summaryData']['PERatio']
                json_data_12 = json['data']['summaryData']['ForwardPE1Yr']
                json_data_13 = json['data']['summaryData']['EarningsPerShare']
                json_data_14 = json['data']['summaryData']['AnnualizedDividend']
                json_data_15 = json['data']['summaryData']['ExDividendDate']
                json_data_16 = json['data']['summaryData']['DividendPaymentDate']
                json_data_17 = json['data']['summaryData']['Yield']
                json_data_18 = json['data']['summaryData']['Beta']
                                        
                array_value = np.array([
                                   json_normalize(json_data_1).iloc[0,1], json_normalize(json_data_2).iloc[0,1]
                                 , json_normalize(json_data_3).iloc[0,1], json_normalize(json_data_4).iloc[0,1]
                                 , json_normalize(json_data_5).iloc[0,1], json_normalize(json_data_6).iloc[0,1]
                                 , json_normalize(json_data_7).iloc[0,1], json_normalize(json_data_8).iloc[0,1]
                                 , json_normalize(json_data_9).iloc[0,1], json_normalize(json_data_10).iloc[0,1]
                                 , json_normalize(json_data_11).iloc[0,1], json_normalize(json_data_12).iloc[0,1]
                                 , json_normalize(json_data_13).iloc[0,1], json_normalize(json_data_14).iloc[0,1]
                                 , json_normalize(json_data_15).iloc[0,1], json_normalize(json_data_16).iloc[0,1]
                                 , json_normalize(json_data_17).iloc[0,1], json_normalize(json_data_18).iloc[0,1]
                                   ])
                
                array_index = np.array([
                                   json_normalize(json_data_1).iloc[0,0], json_normalize(json_data_2).iloc[0,0]
                                 , json_normalize(json_data_3).iloc[0,0], json_normalize(json_data_4).iloc[0,0]
                                 , json_normalize(json_data_5).iloc[0,0], json_normalize(json_data_6).iloc[0,0]
                                 , json_normalize(json_data_7).iloc[0,0], json_normalize(json_data_8).iloc[0,0]
                                 , json_normalize(json_data_9).iloc[0,0], json_normalize(json_data_10).iloc[0,0]
                                 , json_normalize(json_data_11).iloc[0,0], json_normalize(json_data_12).iloc[0,0]
                                 , json_normalize(json_data_13).iloc[0,0], json_normalize(json_data_14).iloc[0,0]
                                 , json_normalize(json_data_15).iloc[0,0], json_normalize(json_data_16).iloc[0,0]
                                 , json_normalize(json_data_17).iloc[0,0], json_normalize(json_data_18).iloc[0,0]
                                   ])
                
                self.nasdaq_summary_df = pd.DataFrame(array_value , index=array_index, columns = [self.ticker + ' Key Data'])
            
            else:
                self.nasdaq_summary_df = None
        except:
            self.nasdaq_summary_df = None
        
        return self.nasdaq_summary_df
    
    ### Nasdaq Dividend History                                                  ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/dividend-history ###
    ### Rückgabe None implementiert und getestet                                 ###
    def __nasdaq_dividend_history_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/dividends?assetclass=stocks", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['dividends']['rows']
            df = json_normalize(json_data)
            #print(df)
            json_headers = json['data']['dividends']['headers']
            df_headers = json_normalize(json_headers)
            self.nasdaq_dividend_history_df = df.rename(columns=df_headers.loc[0])
        except:
            self.nasdaq_dividend_history_df = None
        
        return self.nasdaq_dividend_history_df
        
    ### Nasdaq Historical NOCP                                                  ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/historical-nocp ###
    ### Rückgabe None implementiert und getestet                                ###
    def __nasdaq_historical_nocp_df(self):    
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/historical-nocp?timeframe=y1", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['nocp']['nocpTable']
            df = json_normalize(json_data)
            json_headers = json['data']['headers']
            df_headers = json_normalize(json_headers)
            self.nasdaq_historical_nocp_df = df.rename(columns=df_headers.loc[0])
        except:
            self.nasdaq_historical_nocp_df = None
        
        return self.nasdaq_historical_nocp_df
    
    ### Nasdaq Financials Annual Income Statement                          ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_income_statement_y_df(self): 
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=1", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_1 = json['data']['incomeStatementTable']['rows']
            df = json_normalize(json_1)
            json_headers_1 = json['data']['incomeStatementTable']['headers']
            df_headers_1 = json_normalize(json_headers_1)
            self.nasdaq_financials_income_statement_df = df.rename(columns=df_headers_1.loc[0])
        except:
            self.nasdaq_financials_income_statement_df = None
        
        return self.nasdaq_financials_income_statement_df
    
    ### Nasdaq Financials Annual Balance Statement                         ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_balance_sheet_y_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=1", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_2 = json['data']['balanceSheetTable']['rows']
            df = json_normalize(json_2)
            json_headers_2 = json['data']['balanceSheetTable']['headers']
            df_headers_2 = json_normalize(json_headers_2)
            self.nasdaq_financials_balance_sheet_df = df.rename(columns=df_headers_2.loc[0])
        except:
            self.nasdaq_financials_balance_sheet_df = None
        
        return self.nasdaq_financials_balance_sheet_df
    
    ### Nasdaq Financials Annual Cash Flow                                 ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_cash_flow_y_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=1", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_3 = json['data']['cashFlowTable']['rows']
            df = json_normalize(json_3)
            json_headers_3 = json['data']['cashFlowTable']['headers']
            df_headers_3 = json_normalize(json_headers_3)
            self.nasdaq_financials_cash_flow_df = df.rename(columns=df_headers_3.loc[0])
        except:
            self.nasdaq_financials_cash_flow_df = None
        
        return self.nasdaq_financials_cash_flow_df
    
    ### Nasdaq Financials Annual Financial Ratios                          ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_financials_ratios_y_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=1", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_4 = json['data']['financialRatiosTable']['rows']
            df = json_normalize(json_4)
            json_headers_4 = json['data']['financialRatiosTable']['headers']
            df_headers_4 = json_normalize(json_headers_4)
            self.nasdaq_financials_financials_ratios_df = df.rename(columns=df_headers_4.loc[0])
        except:
            self.nasdaq_financials_financials_ratios_df = None
        
        return self.nasdaq_financials_financials_ratios_df

    ### Nasdaq Financials Quarterly Income Statement                       ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_income_statement_q_df(self): 
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=2", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_1 = json['data']['incomeStatementTable']['rows']
            df = json_normalize(json_1)
            json_headers_1 = json['data']['incomeStatementTable']['headers']
            df_headers_1 = json_normalize(json_headers_1)
            self.nasdaq_financials_income_statement_df = df.rename(columns=df_headers_1.loc[0])
        except:
            self.nasdaq_financials_income_statement_df = None
        
        return self.nasdaq_financials_income_statement_df
    
    ### Nasdaq Financials Quarterly Balance Statement                      ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_balance_sheet_q_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=2", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_2 = json['data']['balanceSheetTable']['rows']
            df = json_normalize(json_2)
            json_headers_2 = json['data']['balanceSheetTable']['headers']
            df_headers_2 = json_normalize(json_headers_2)
            self.nasdaq_financials_balance_sheet_df = df.rename(columns=df_headers_2.loc[0])
        except:
            self.nasdaq_financials_balance_sheet_df = None
        
        return self.nasdaq_financials_balance_sheet_df
    
    ### Nasdaq Financials Quarterly Cash Flow                              ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_cash_flow_q_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=2", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_3 = json['data']['cashFlowTable']['rows']
            df = json_normalize(json_3)
            json_headers_3 = json['data']['cashFlowTable']['headers']
            df_headers_3 = json_normalize(json_headers_3)
            self.nasdaq_financials_cash_flow_df = df.rename(columns=df_headers_3.loc[0])
        except:
            self.nasdaq_financials_cash_flow_df = None
        
        return self.nasdaq_financials_cash_flow_df
    
    ### Nasdaq Financials Quarterly Financial Ratios                       ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/financials ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_financials_financials_ratios_q_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/financials?frequency=2", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_4 = json['data']['financialRatiosTable']['rows']
            df = json_normalize(json_4)
            json_headers_4 = json['data']['financialRatiosTable']['headers']
            df_headers_4 = json_normalize(json_headers_4)
            self.nasdaq_financials_financials_ratios_df = df.rename(columns=df_headers_4.loc[0])
        except:
            self.nasdaq_financials_financials_ratios_df = None
        
        return self.nasdaq_financials_financials_ratios_df

    ### Nasdaq Earnings Date Earnings Per Share                          ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/earnings ###
    ### Rückgabe None implementiert und getestet                         ###
    def __nasdaq_earnings_date_eps_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/eps", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['earningsPerShare']
            self.nasdaq_earnings_date_eps_df = json_normalize(json_data)
        except:
            self.nasdaq_earnings_date_eps_df = None
        
        return self.nasdaq_earnings_date_eps_df


    ### Nasdaq Earnings Date Quarterly Earnings Surprise Amount          ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/earnings ###
    ### Rückgabe None implementiert und getestet                         ###
    def __nasdaq_earnings_date_surprise_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/company/{self.ticker}/earnings-surprise", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['earningsSurpriseTable']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['earningsSurpriseTable']['headers']
            df_headers = json_normalize(json_headers)
            self.nasdaq_earnings_date_surprise_df = df.rename(columns=df_headers.loc[0])
        except:
            self.nasdaq_earnings_date_surprise_df = None
        
        return self.nasdaq_earnings_date_surprise_df
    
    ### Nasdaq Earnings Date Yearly Earnings Forecast                    ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/earnings ###
    ### Rückgabe None implementiert und getestet                         ###
    def __nasdaq_earnings_date_yearly_earnings_forecast_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/analyst/{self.ticker}/earnings-forecast", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['yearlyForecast']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['yearlyForecast']['headers']
            df_headers = json_normalize(json_headers)
            self.nasdaq_earnings_date_yearly_earnings_forecast_df = df.rename(columns=df_headers.loc[0])
        except:
            self.nasdaq_earnings_date_yearly_earnings_forecast_df = None
        
        return self.nasdaq_earnings_date_yearly_earnings_forecast_df

    ### Nasdaq Earnings Date Quarterly Earnings                          ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/earnings ###
    ### Rückgabe None implementiert und getestet                         ### 
    def __nasdaq_earnings_date_quarterly_earnings_forecast_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/analyst/{self.ticker}/earnings-forecast", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['quarterlyForecast']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['quarterlyForecast']['headers']
            df_headers = json_normalize(json_headers)
            self.nasdaq_earnings_date_quarterly_earnings_forecast_df = df.rename(columns=df_headers.loc[0])
        except:
            self.nasdaq_earnings_date_quarterly_earnings_forecast_df = None
        
        return self.nasdaq_earnings_date_quarterly_earnings_forecast_df
    
    ### Nasdaq Price/Earnings & PEG Ratios Forecast PEG Ratio                             ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/price-earnings-peg-ratios ###
    ### Rückgabe None implementiert und getestet                                          ###
    def __forecast_pe_peg_df(self):
        r = requests.get(f"https://api.nasdaq.com/api/analyst/{self.ticker}/peg-ratio", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_data_forecast_pe = json['data']['per']['peRatioChart']
            json_data_forecast_gr = json['data']['gr']['peGrowthChart']
            json_data_forecast_peg = json['data']['pegr']
            
            df_forecast_pe = json_normalize(json_data_forecast_pe)                  # Dataframe
            df_forecast_gr = json_normalize(json_data_forecast_gr)                  # Dataframe
            df_forecast_peg = json_normalize(json_data_forecast_peg)                # Dataframe
            
            df_forecast_gr_array = df_forecast_gr['z'] + ' ' + df_forecast_gr['x']  # Series

            arrays = [
                np.array(["Price/Earnings Ratio","Price/Earnings Ratio","Price/Earnings Ratio","Price/Earnings Ratio"
                          , "Forecast P/E Growth Rates", "Forecast P/E Growth Rates", "Forecast P/E Growth Rates"
                          , "Forecast P/E Growth Rates", "PEG Ratio"]),
                np.array(df_forecast_pe.iloc[0:,0].tolist() + df_forecast_gr_array.tolist() + df_forecast_peg.iloc[0:,0].tolist())]
            
            array_table = df_forecast_pe.iloc[0:,1].tolist() + df_forecast_gr.iloc[0:,2].tolist() + df_forecast_peg.iloc[0:,-1].tolist()
            
            s = pd.DataFrame(array_table , index=arrays, columns = [self.ticker + ' Price/Earnings & PEG Ratios'])
            
            self.__forecast_pe_peg_df = s
        except:
            self.__forecast_pe_peg_df = None
        
        return self.__forecast_pe_peg_df
    
    ### Nasdaq Historical Data Stocks                                      ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/historical ###
    ### Rückgabe None implementiert und getestet                           ###
    def __nasdaq_historical_data_stock_df(self):
        from datetime import datetime
        datum = datetime.today().strftime('%Y-%m-%d')
        
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/historical?assetclass=stocks&fromdate=2011-09-26&limit=9999&todate={datum}", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['tradesTable']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['tradesTable']['headers']
            df_headers = json_normalize(json_headers)
            self.nasdaq_historical_data_stock_df = df.rename(columns=df_headers.loc[0])
        except:
            self.nasdaq_historical_data_stock_df = None
        
        return self.nasdaq_historical_data_stock_df
    
    ### Historical Data ETF                                                ###
    ### e.g. https://www.nasdaq.com/market-activity/stocks/nvda/historical ###
    ### Nasdaq Rückgabe None implementiert und getestet                    ###
    def __nasdaq_historical_data_etf_df(self):
        from datetime import datetime
        datum = datetime.today().strftime('%Y-%m-%d')
        
        r = requests.get(f"https://api.nasdaq.com/api/quote/{self.ticker}/historical?assetclass=etf&fromdate=2011-09-26&limit=9999&todate={datum}", headers=self.headers_standard)
        try:
            json = r.json()
            
            json_data = json['data']['tradesTable']['rows']
            df = json_normalize(json_data)
            json_headers = json['data']['tradesTable']['headers']
            df_headers = json_normalize(json_headers)
            self.nasdaq_historical_data_etf_df = df.rename(columns=df_headers.loc[0])
        except:
            self.nasdaq_historical_data_etf_df = None
        
        return self.nasdaq_historical_data_etf_df
    
    #######################
    ###                 ###
    ###  Yahoo Finance  ###
    ###                 ###
    #######################
    
    ### Yahoo Finance Statistics                                 ###
    ### e.g. https://finance.yahoo.com/quote/NVDA/key-statistics ###
    ### Rückgabe None implementiert und getestet                 ###
    ### Ungültige Werte = NaN implementiert                      ###   
    def __yahoo_statistics_df(self):
        url = f'https://finance.yahoo.com/quote/{self.ticker}/key-statistics'
        
        with requests.session():
            page = requests.get(url, headers = self.headers_standard)
            page = BeautifulSoup(page.content, 'html.parser')
            table = page.find_all('td', {'class':'Fw(500) Ta(end) Pstart(10px) Miw(60px)'})
                  
            if len(table) == 0:
                self.yahoo_statistics_df = None
            else:
                headlines = page.find_all('h3', {'class':'Mt(20px)'})
                
                valuation_measures = []; n = 9; v = page.find_all('h2', {'class':'Pt(20px)'})[0].text
                valuation_measures += n * [v]
                
                stock_price_history = []; n = 7; v = headlines[0].text
                stock_price_history += n * [v]
                
                share_statistics = []; n = 12; v = headlines[1].text
                share_statistics += n * [v]
                
                dividends_splits = []; n = 10; v = headlines[2].text
                dividends_splits += n * [v]
                
                fiscal_year = []; n = 2; v = headlines[3].text
                fiscal_year += n * [v]
                
                profitability = []; n = 2; v = headlines[4].text
                profitability += n * [v]
                
                management_effectiveness = []; n = 2; v = headlines[5].text
                management_effectiveness += n * [v]
                
                income_statement = []; n = 8; v = headlines[6].text
                income_statement += n * [v]
                
                balance_sheet = []; n = 6; v = headlines[7].text
                balance_sheet += n * [v]
                
                cash_flow_statement = []; n = 2; v = headlines[8].text
                cash_flow_statement += n * [v]
                
                outer_text = page.find_all('td', {'class':'Pos(st) Start(0) Bgc($lv2BgColor) fi-row:h_Bgc($hoverBgColor) Pend(10px) Miw(140px)'})
                inner_text = page.find_all('td', {'class':'Pos(st) Start(0) Bgc($lv2BgColor) fi-row:h_Bgc($hoverBgColor) Pend(10px)'})
                
                if len(outer_text) == 10 or len(inner_text) == 50:
                
                    arrays = [
                        np.array(valuation_measures + stock_price_history + share_statistics + dividends_splits + fiscal_year
                                 + profitability + management_effectiveness + income_statement + balance_sheet + cash_flow_statement)
                                ,
                        
                        np.array([outer_text[0].text[:-2], inner_text[0].text[:-2], inner_text[1].text[:-1], inner_text[2].text[:-2]
                                  , inner_text[3].text[:-2], inner_text[4].text, inner_text[5].text, inner_text[6].text[:-2]
                                  , inner_text[7].text[:-2], outer_text[1].text.strip(), inner_text[8].text[:-2], inner_text[9].text[:-2]
                                  , inner_text[10].text[:-2], inner_text[11].text[:-2], inner_text[12].text[:-2], inner_text[13].text[:-2]
                                  , outer_text[2].text[:-2], inner_text[14].text[:-2], inner_text[15].text[:-2], inner_text[16].text[:-2]
                                  , inner_text[17].text[:-2], inner_text[18].text[:-2], inner_text[19].text[:-2], inner_text[20].text[:-2]
                                  , inner_text[21].text[:-2], inner_text[22].text[:-2], inner_text[23].text[:-2], inner_text[24].text[:-2]
                                  , outer_text[3].text[:-2], inner_text[25].text[:-2], inner_text[26].text[:-2], inner_text[27].text[:-2]
                                  , inner_text[28].text[:-2], inner_text[29].text[:-2], inner_text[30].text[:-2], inner_text[31].text[:-2]
                                  , inner_text[32].text[:-2], inner_text[33].text[:-2], outer_text[4].text[:-1], inner_text[34].text
                                  , outer_text[5].text[:-1], inner_text[35].text, outer_text[6].text, inner_text[36].text
                                  , outer_text[7].text, inner_text[37].text, inner_text[38].text, inner_text[39].text
                                  , inner_text[40].text.strip(), inner_text[41].text, inner_text[42].text, inner_text[43].text
                                  , outer_text[8].text, inner_text[44].text, inner_text[45].text, inner_text[46].text
                                  , inner_text[47].text, inner_text[48].text, outer_text[9].text, inner_text[49].text
                                  ]),]
                    
                    array_table = []
                
                    for i in range (0,60):
                        array_table.append(table[i].text.strip())
                        
                    s = pd.DataFrame(array_table , index=arrays, columns = [self.ticker + ' Yahoo Statistics'])
                    s = s.loc[:,self.ticker + ' Yahoo Statistics'].replace(['N/A'],np.nan)
                    
                    self.yahoo_statistics_df = s.to_frame(name= self.ticker + ' Yahoo Statistics')
                
                else:
                    self.yahoo_statistics_df = None
        
        return self.yahoo_statistics_df
    
    ### Yahoo Finance Statistics - PreProcessing                 ###
    ### e.g. https://finance.yahoo.com/quote/NVDA/key-statistics ###
    def __yahoo_statistics_df_p(self):
             
        def m_b_t(string):
            
            if type(string) != float:
                if string[-1] == 'B':
                    string = float(string[:-1])*10**9
                elif string[-1] == 'M':
                    string = float(string[:-1])*10**6
                elif string[-1] == 'T':
                    string = float(string[:-1])*10**12
                else:
                    string = float(string[:-1])
            else:
                pass
            
            return string
        
        s = self.yahoo_statistics
        
        if type(s) != None:
        
            # Market Cap
            s.iloc[0,0] = m_b_t(s.iloc[0,0])
            # Enterprise Value
            s.iloc[1,0] = m_b_t(s.iloc[1,0])
            # Trailing P/E
            s.iloc[2,0] = float(s.iloc[2,0])
            # Forward P/E
            s.iloc[3,0] = float(s.iloc[3,0])
            # PEG Ratio (5 yr expected)
            s.iloc[4,0] = float(s.iloc[4,0])
            # Price/Sales (ttm)
            s.iloc[5,0] = float(s.iloc[5,0])
            # Price/Book (mrq)
            s.iloc[6,0] = float(s.iloc[6,0])
            # Enterprise Value/Revenue
            s.iloc[7,0] = float(s.iloc[7,0])
            # Enterprise Value/EBITDA
            s.iloc[8,0] = float(s.iloc[8,0])
            # Beta (5Y Monthly)
            s.iloc[9,0] = float(s.iloc[9,0])
            # 52-Week Change
            s.iloc[10,0] = m_b_t(s.iloc[10,0])
            # S&P500 52-Week Change
            s.iloc[11,0] = m_b_t(s.iloc[11,0])
            # 52 Week High
            s.iloc[12,0] = float(s.iloc[12,0])
            # 52 Week Low
            s.iloc[13,0] = float(s.iloc[13,0])
            # 50-Day Moving Average
            s.iloc[14,0] = float(s.iloc[14,0])
            # 200-Day Moving Average
            s.iloc[15,0] = float(s.iloc[15,0])
            # Avg Vol (3 month)
            s.iloc[16,0] = m_b_t(s.iloc[16,0])
            # Avg Vol (10 day)
            s.iloc[17,0] = m_b_t(s.iloc[17,0])
            # Shares Outstanding
            s.iloc[18,0] = m_b_t(s.iloc[18,0])
            # Implied Shares Outstanding
            s.iloc[19,0] = m_b_t(s.iloc[19,0])
            # Float
            s.iloc[20,0] = m_b_t(s.iloc[20,0])
            # % Held by Insiders
            s.iloc[21,0] = m_b_t(s.iloc[21,0])
            # % Held by Institutions
            s.iloc[22,0] = m_b_t(s.iloc[22,0])
            # Shares Short (Oct 14, 2021)
            s.iloc[23,0] = m_b_t(s.iloc[23,0])
            # Short Ratio (Oct 14, 2021)
            s.iloc[24,0] = float(s.iloc[24,0])
            # Short % of Float (Oct 14, 2021)
            s.iloc[25,0] = m_b_t(s.iloc[25,0])
            # Short % of Shares Outstanding (Oct 14, 2021)
            s.iloc[26,0] = m_b_t(s.iloc[26,0])
            # Shares Short (prior month Sep 14, 2021)
            s.iloc[27,0] = m_b_t(s.iloc[27,0])
            # Forward Annual Dividend Rate
            s.iloc[28,0] = float(s.iloc[28,0])
            # Forward Annual Dividend Yield
            s.iloc[29,0] = m_b_t(s.iloc[29,0])
            # Trailing Annual Dividend Rate
            s.iloc[30,0] = float(s.iloc[30,0])
            # Trailing Annual Dividend Yield
            s.iloc[31,0] = m_b_t(s.iloc[31,0])
            # 5 Year Average Dividend Yield
            s.iloc[32,0] = float(s.iloc[32,0])
            # Payout Ratio
            s.iloc[33,0] = m_b_t(s.iloc[33,0])
            # Dividend Date
            # s.iloc[34,0] = float(s.iloc[34,0])
            # Ex-Dividend Date
            #s.iloc[35,0] = float(s.iloc[35,0])
            # Last Split Factor
            #s.iloc[36,0] = float(s.iloc[36,0])
            # Last Split Date
            #s.iloc[37,0] = float(s.iloc[37,0])
            # Fiscal Year Ends
            #s.iloc[38,0] = float(s.iloc[38,0])
            # Most Recent Quarter (mrq)
            #s.iloc[39,0] = float(s.iloc[39,0])
            # Profit Margin
            s.iloc[40,0] = m_b_t(s.iloc[40,0])
            # Operating Margin (ttm)
            s.iloc[41,0] = m_b_t(s.iloc[41,0])
            # Return on Assets (ttm)
            s.iloc[42,0] = m_b_t(s.iloc[42,0])
            # Return on Equity (ttm)
            s.iloc[43,0] = m_b_t(s.iloc[43,0])
            # Revenue (ttm)
            s.iloc[44,0] = m_b_t(s.iloc[44,0])
            # Revenue Per Share (ttm)
            s.iloc[45,0] = float(s.iloc[45,0])
            # Quarterly Revenue Growth (yoy)
            s.iloc[46,0] = m_b_t(s.iloc[46,0])
            # Gross Profit (ttm)
            s.iloc[47,0] = m_b_t(s.iloc[47,0])
            # EBITDA
            s.iloc[48,0] = m_b_t(s.iloc[48,0])
            # Net Income Avi to Common (ttm)
            s.iloc[49,0] = m_b_t(s.iloc[49,0])
            # Diluted EPS (ttm)
            s.iloc[50,0] = float(s.iloc[50,0])
            # Quarterly Earnings Growth (yoy)
            s.iloc[51,0] = m_b_t(s.iloc[51,0])
            # Total Cash (mrq)
            s.iloc[52,0] = m_b_t(s.iloc[52,0])
            # Total Cash Per Share (mrq)
            s.iloc[53,0] = float(s.iloc[53,0])
            # Total Debt (mrq)
            s.iloc[54,0] = m_b_t(s.iloc[54,0])
            # Total Debt/Equity (mrq)
            s.iloc[55,0] = float(s.iloc[55,0])
            # Current Ratio (mrq)
            s.iloc[56,0] = float(s.iloc[56,0])
            # Book Value Per Share (mrq)
            s.iloc[57,0] = float(s.iloc[57,0])
            # Operating Cash Flow (ttm)
            s.iloc[58,0] = m_b_t(s.iloc[58,0])
            # Levered Free Cash Flow (ttm)
            s.iloc[59,0] = m_b_t(s.iloc[59,0])
            
            s = s.rename(columns = {self.ticker + ' Yahoo Statistics' : self.ticker + ' Yahoo Statistics PreProcessing'})
        
        else:
            s = None
        
        return s
    
    #####################
    ###               ###
    ###  Gurufocus    ###
    ###               ###
    #####################
    
    def __stock_exchange(self):
        r = requests.get(f'https://www.gurufocus.com/stock/{self.ticker}/summary')
        stock_exchange = BeautifulSoup(r.content, 'html.parser')
        
        try:
            stock_exchange = stock_exchange.find('div', {'class':'el-col el-col-24'}).text.split()[0]
        except:
            return None
        
        return stock_exchange
    
    def __gurufocus_pe_ratio_av_v(self):
        if Ticker.__stock_exchange(self) != None:
            r = requests.get(f'https://www.gurufocus.com/term/pettm/{Ticker.__stock_exchange(self)}/PE-Ratio-TTM/')
            page = BeautifulSoup(r.content, 'html.parser')
        
            table = page.find('div', {'class':'history_bar value'})
            try:
                table = table.find('strong').text.split()
                self.__PE_Ratio_Average = float(table[3])
                return self.__PE_Ratio_Average
            except:
                return None
        else:
            return None
        
    def __gurufocus_debt_to_ebitda(self):
        
        if Ticker.__stock_exchange(self) != None:
          
            url = f'https://www.gurufocus.com/term/debt2ebitda/{Ticker.__stock_exchange(self)}/Debt-to-EBITDA'
            page = requests.get(url)
            page = BeautifulSoup(page.content, 'html.parser')

            table = page.find('div', {'class':'history_bar value'})

            try:
                table = table.find('strong')
                table = table.text.split()
                debt_to_EBITDA = table[7]
                try:
                    self.__debt_to_EBITDA = float(debt_to_EBITDA)
                except:
                    return '#'
                return self.__debt_to_EBITDA
            except (AttributeError):
                return '#'

###############################################################################
###############################################################################

    #########################
    ###                   ###
    ###  Stock exchanges  ###
    ###     indicies      ###
    ###                   ###
    #########################
        
class StockExchange:

    def __init__(self, stockexchange):
        self.stockexchange = stockexchange
        self.__headers_standard = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"}
        
    def __repr__(self):
        return(self.stockexchange)
        
    def __str__(self):
        return(self.stockexchange)
    
    @property
    def nasdaq(self):
        return self.__df_nasdaq()
    
    @property
    def cnn_fear_and_greed(self):
        return self.__cnn_fear_and_greed_df()
    
    @property
    def dax(self):
        return self.__boersenag_dax_df()
    
    @property
    def mdax(self):
        return self.__boersenag_mdax_df()
    
    @property
    def sdax(self):
        return self.__boersenag_sdax_df()
    
    @property
    def tecdax(self):
        return self.__boersenag_tecdax_df()
    
    @property
    def nisax(self):
        return self.__boersenag_nisax_df()
    
    @property
    def haspax(self):
        return self.__boersenag_haspax_df()
    
    @property
    def eurostoxx(self):
        return self.__boersenag_eurostoxx_df()
    
    @property
    def gcx(self):
        return self.__boersenag_gcx_df()
    
    @property
    def gevx(self):
        return self.__boersenag_gevx_df()
    
    @property
    def gergenx(self):
        return self.__boersenag_gergenx_df()
    
    @property
    def dow_jones(self):
        return self.__boersenag_dow_jones_df()
    
    @property
    def nasdaq_100(self):
        return self.__boersenag_nasdaq_100_df()
    
    #####################
    ###               ###
    ###    NASDAQ     ###
    ###               ###
    #####################
    
    ### NASDQ Stock Screener                                   ###
    ### https://www.nasdaq.com/market-activity/stocks/screener ###
    def __df_nasdaq(self):
        r = requests.get("https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true", headers=self.__headers_standard)
        
        json = r.json()
               
        json_data = json['data']['rows']
        df = json_normalize(json_data)
        json_headers = json['data']['headers']
        df_headers = json_normalize(json_headers)
        df_nasdaq_stockexchange = df.rename(columns=df_headers.loc[0])
        
        return df_nasdaq_stockexchange
    
    #####################
    ###               ###
    ###      CNN      ###
    ###               ###
    #####################
    
    ### CNN Fear and Greed Index                   ###
    ### https://money.cnn.com/data/fear-and-greed/ ###
    def __cnn_fear_and_greed_df(self):
        r = requests.get('https://money.cnn.com/data/fear-and-greed/')
        page = BeautifulSoup(r.content, 'html.parser')
        
        table = page.find('div', {'id':'needleChart'})
        try:
            array_index =   [   
                                table.text.split(' (')[0].split(':')[0]
                             ,  table.text.split(' (')[1].split(')')[1].split(':')[0]
                             ,  table.text.split(' (')[2].split(')')[1].split(':')[0]
                             ,  table.text.split(' (')[3].split(')')[1].split(':')[0]
                             ,  table.text.split(' (')[4].split(')')[1].split(':')[0]
                            ]
            
            array_value =   [
                             [table.text.split(' (')[0].split(':')[1].strip() ,table.text.split(' (')[1].split(')')[0]]
                            ,[table.text.split(' (')[1].split(':')[1].strip() ,table.text.split(' (')[2].split(')')[0]]
                            ,[table.text.split(' (')[2].split(':')[1].strip() ,table.text.split(' (')[3].split(')')[0]]
                            ,[table.text.split(' (')[3].split(':')[1].strip() ,table.text.split(' (')[4].split(')')[0]]
                            ,[table.text.split(' (')[4].split(':')[1].strip() ,table.text.split(' (')[5].split(')')[0]]
                            ]
            
            df_cnn_fear_and_greed = pd.DataFrame(array_value, index = array_index, columns = ['Fear & Greed Index', ''])
            
            return df_cnn_fear_and_greed
        except:
            return None
        
    ##########################
    ###                    ###
    ###      Börsen        ###
    ###  Hamburg-Hannover  ###
    ###                    ###
    ##########################
    
    ### DAX Performance-Index                           ###
    ### 40 Werte                                        ###
    ### https://www.boersenag.de/Index/DE0008469008/DAX ###

    def __boersenag_dax_df(self):
        url = 'https://www.boersenag.de/Index/DE0008469008/DAX'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        number = page.find('div', {'class':'pager'}).text.split()[-2]               # String
        
        url = f'https://www.boersenag.de/Index/DE0008469008/DAX?p=1&pager=780&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        table = page.find('table', {'class':'table table-striped table-prices'})
        
        try:
            page = page.find_all('a')
            columns = table.find_all('th')
            
            data = []
            
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
            
            index_array = list(range(1,int(number)+1))
            
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
            
            __df_boersenag_dax = pd.DataFrame(
                                data,
                                index = index_array,
                                columns = columns_array
                                )
            
            return __df_boersenag_dax
        except:
            return None
        
    ### MDAX Performance-Index                            ###
    ### 50 Werte                                          ###
    ### https://www.boersenag.de/Index/DE0008467416/MDAX  ###
    
    def __boersenag_mdax_df(self):
        url = 'https://www.boersenag.de/Index/DE0008467416/MDAX'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        number = page.find('div', {'class':'pager'}).text.split()[-2]                           # String
    
        url = f'https://www.boersenag.de/Index/DE0008467416/MDAX?p=1&pager=811&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        table = page.find('table', {'class':'table table-striped table-prices'})
        
        try:
            page = page.find_all('a')
            columns = table.find_all('th')
        
            data = []
        
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
        
            index_array = list(range(1,int(number)+1))
        
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
        
            __df_boersenag_mdax = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
    
            return __df_boersenag_mdax
        except:
            return None
        
    ### SDAX Performance-Index                            ###
    ### 70 Werte                                          ###
    ### https://www.boersenag.de/Index/DE0009653386/SDAX  ###
    
    def __boersenag_sdax_df(self):
        url = 'https://www.boersenag.de/Index/DE0009653386/SDAX'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        number = page.find('div', {'class':'pager'}).text.split()[-2]
    
        url = f'https://www.boersenag.de/Index/DE0009653386/SDAX?p=1&pager=842&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        table = page.find('table', {'class':'table table-striped table-prices'})
        try:
            page = page.find_all('a')
            columns = table.find_all('th')
        
            data = []
        
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
        
            index_array = list(range(1,int(number)+1))
        
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
        
            __df_boersenag_sdax = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )

            return __df_boersenag_sdax
        except:
            return None
    
    ### TecDAX Performance-Index                            ###
    ### 30 Werte                                            ###
    ### https://www.boersenag.de/Index/DE0007203275/TecDAX  ###
    
    def __boersenag_tecdax_df(self):
        url = 'https://www.boersenag.de/Index/DE0007203275/TecDAX'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        number = page.find('div', {'class':'pager'}).text.split()[-2]
    
        url = f'https://www.boersenag.de/Index/DE0007203275/TecDAX?p=1&pager=815&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        table = page.find('table', {'class':'table table-striped table-prices'})
        try:
            page = page.find_all('a')
            columns = table.find_all('th')
        
            data = []
        
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
        
            index_array = list(range(1,int(number)+1))
        
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
        
            __df_boersenag_tecdax = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
    
            return __df_boersenag_tecdax
        except:
            return None
    
    ### NISAX 20 Index (Net Return) (EUR)                   ###
    ### 20 Werte                                            ###
    ### https://www.boersenag.de/Index/DE000A2BL7T2/Nisax20 ###
    
    def __boersenag_nisax_df(self):
        url = 'https://www.boersenag.de/Index/DE000A2BL7T2/Nisax20'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        number = page.find('div', {'class':'pager'}).text.split()[-2]
        
        url = f'https://www.boersenag.de/Index/DE000A2BL7T2/Nisax20?p=1&pager=4891&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
            
            page = page.find_all('a')
            columns = table.find_all('th')
            
            data = []
            
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
            
            index_array = list(range(1,int(number)+1))
            
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
            
            __df_boersenag_nisax = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
        
            return __df_boersenag_nisax
        except:
            return None
    
    ### Haspax Index (Performance) (EUR)                   ###
    ### 22 Werte (01.12.2021)                              ###
    ### https://www.boersenag.de/Index/DE0008468810/Haspax ###
    
    def __boersenag_haspax_df(self):
        url = 'https://www.boersenag.de/Index/DE0008468810/Haspax'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        number = page.find('div', {'class':'pager'}).text.split()[-2]
    
        url = f'https://www.boersenag.de/Index/DE0008468810/Haspax?p=1&pager=1093&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
        
            page = page.find_all('a')
            columns = table.find_all('th')
        
            data = []
        
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
        
            index_array = list(range(1,int(number)+1))
        
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
        
            __df_boersenag_haspax = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
    
            return __df_boersenag_haspax
        except:
            return None
        
    ### EURO STOXX 50 Index (Price) (EUR)                       ###
    ### 50 Werte                                                ###
    ### https://www.boersenag.de/Index/EU0009658145/EuroStoxx50 ###
    
    def __boersenag_eurostoxx_df(self):
        url = 'https://www.boersenag.de/Index/EU0009658145/EuroStoxx50'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        number = page.find('div', {'class':'pager'}).text.split()[-2]
    
        url = f'https://www.boersenag.de/Index/EU0009658145/EuroStoxx50?p=1&pager=1293&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
        
            page = page.find_all('a')
            columns = table.find_all('th')
        
            data = []
        
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
        
            index_array = list(range(1,int(number)+1))
        
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
        
            __df_boersenag_eurostoxx = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )

            return __df_boersenag_eurostoxx
        except:
            return None
    
    ### GCX Global Challenges Performance-Index         ###
    ### 50 Werte                                        ###
    ### https://www.boersenag.de/Index/DE000A0MEN25/GCX ###
    
    def __boersenag_gcx_df(self):
        url = 'https://www.boersenag.de/Index/DE000A0MEN25/GCX'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        number = page.find('div', {'class':'pager'}).text.split()[-2]
    
        url = f'https://www.boersenag.de/Index/DE000A0MEN25/GCX?p=1&pager=818&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
    
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
        
            page = page.find_all('a')
            columns = table.find_all('th')
        
            data = []
        
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
        
            index_array = list(range(1,int(number)+1))
        
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
        
            __df_boersenag_gcx = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )

            return __df_boersenag_gcx
        except:
            return None

    ### Global Ethical Values Index (Total Return) (EUR)  ###
    ### 609 Werte (variable)                              ###
    ### https://www.boersenag.de/Index/DE000SL0EBW8/GEVX  ###
    
    def __boersenag_gevx_df(self):
        url = 'https://www.boersenag.de/Index/DE000SL0EBW8/GEVX'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        number_gesamt = page.find('div', {'class':'pager'}).text.split()[-2]           # String
        
        data = []
        
        try:
        
            for seite in range(1, int(int(number_gesamt)/100)+2):
             
                number = '100'
                
                url = f'https://www.boersenag.de/Index/DE000SL0EBW8/GEVX?p={seite}&pager=5345&limit={number}'
                page = requests.get(url)
                page = BeautifulSoup(page.content, 'html.parser')
                
                table = page.find('table', {'class':'table table-striped table-prices'})
                
                page = page.find_all('a')
                columns = table.find_all('th')
                
                if seite > int(int(number_gesamt)/100):
                    number = str(int(number_gesamt) % 100)
                
                for i in range(int(number)):
                    data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
                
            
            index_array = list(range(1,int(number_gesamt)+1))
            
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
            
            __df_boersenag_gevx = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
                
            return __df_boersenag_gevx
        except:
            return None

    ### German Gender Index (Total Return) (EUR)                       ###
    ### 50 Werte                                                       ###
    ### https://www.boersenag.de/Index/DE000SLA0QF8/GermanGenderIndex  ###
    
    def __boersenag_gergenx_df(self):
        url = 'https://www.boersenag.de/Index/DE000SLA0QF8/GermanGenderIndex'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        number = page.find('div', {'class':'pager'}).text.split()[-2]
        
        url = f'https://www.boersenag.de/Index/DE000SLA0QF8/GermanGenderIndex?p=1&pager=1308&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
            
            page = page.find_all('a')
            columns = table.find_all('th')
            
            data = []
            
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
            
            index_array = list(range(1,int(number)+1))
            
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
            
            __df_boersenag_gergenx = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
        
            return __df_boersenag_gergenx
        except:
            return None


    ### Dow Jones Industrial Average Index (Price) (USD)       ###
    ### 30 Werte (fix) - Fehler hier nur 29 Werte (01.12.2021) ###
    ### https://www.boersenag.de/Index/US2605661048/DowJones   ###
    
    def __boersenag_dow_jones_df(self):
        url = 'https://www.boersenag.de/Index/US2605661048/DowJones'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        number = page.find('div', {'class':'pager'}).text.split()[-2]

        url = f'https://www.boersenag.de/Index/US2605661048/DowJones?p=1&pager=1323&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
            
            page = page.find_all('a')
            columns = table.find_all('th')
            
            data = []
            
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
            
            index_array = list(range(1,int(number)+1))
            
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
            
            __df_boersenag_dow_jones = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )
    
            return __df_boersenag_dow_jones
        except:
            return None

    ### Nasdaq-100 Index                                        ###
    ### 100 Werte (fix) - Fehler hier nur 86 Werte (01.12.2021) ###
    ### https://www.boersenag.de/Index/US6311011026/Nasdaq      ###
    
    def __boersenag_nasdaq_100_df(self):
        url = 'https://www.boersenag.de/Index/US6311011026/Nasdaq'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        number = page.find('div', {'class':'pager'}).text.split()[-2]
        
        url = f'https://www.boersenag.de/Index/US6311011026/Nasdaq?p=1&pager=1338&limit={number}'
        page = requests.get(url)
        page = BeautifulSoup(page.content, 'html.parser')
        
        try:
            table = page.find('table', {'class':'table table-striped table-prices'})
            
            page = page.find_all('a')
            columns = table.find_all('th')
            
            data = []
            
            for i in range(int(number)):
                data.append([page[i].prettify().split('\n')[2].strip().replace('amp;',''), page[i].prettify().split('\n')[-2].strip()])
            
            index_array = list(range(1,int(number)+1))
            
            columns_array = [
                            columns[0].prettify().split()[1], 
                            columns[0].prettify().split()[3]
                            ]
            
            __df_boersenag_nasdaq_100 = pd.DataFrame(
                            data,
                            index = index_array,
                            columns = columns_array
                            )

            return __df_boersenag_nasdaq_100
        except:
            return None

###############################################################################
###############################################################################


    ############################
    ###                      ###
    ###  Valuation Summary   ###
    ###  under construction  ###
    ###                      ###
    ############################
    
# Basis
class StockValuation:

    def __init__(self, ticker):
        self.ticker = ticker
        
    def __repr__(self):
        return(self.ticker)
        
    def __str__(self):
        return(self.ticker)
    
    @property
    def valuation(self):
        return self.__df_valuation()
    
    def __df_valuation(self):
        
        arrays = [
            np.array([  "Fundamental"
                      , "Valuation Ratio"
                      , "Valuation Ratio"
                      , "Valuation Ratio"
                      , "Profitability"
                      , "Price"
                      , "Dividends"
                      , "Income Statement"
                      , "Income Statement"
                      , "Balance Sheet"
                      , "Cashflow Statement"
                      , "Technical Indicator"
                      ]),
            
            np.array([  "5-Year EBITDA Growth Rate"
                      , "Debt-to-EBITDA"
                      , "PE-Ratio (TTM)"
                      , "PE-Ratio (Forward)"
                      , "FCF Margin %"
                      , "Beta"
                      , "3-Year Dividend Growth Rate"
                      , "EBIT"
                      , "EBITDA"
                      , "Long-Term Debt"
                      , "Free Cash Flow"
                      , "50-Day SMA"
                      ])]
        
        # Yahoo Finanance # Morningstar # NASDAQ
        array_table = [
                        # Fundamental / 5-Year EBITDA Growth Rate
                        [np.nan
                       , np.nan
                       , np.nan]                              
                       # Valuation Ratio / Debt-to-EBITDA
                       , [self.debt_to_ebitda_yahoo()
                       , np.nan
                       , np.nan]
                       # Valuation Ratio / PE-Ratio (TTM)
                       , [Ticker(self.ticker).yahoo_statistics_p.iloc[2,0]
                       , np.nan
                       , np.nan]
                       # Valuation Ratio / PE-Ratio (Forward)
                       , [Ticker(self.ticker).yahoo_statistics_p.iloc[3,0]
                       , np.nan
                       , np.nan]
                       # Profitability / FCF Margin %
                       , [np.nan
                       , np.nan
                       , np.nan]
                       # Price / Beta
                       , [np.nan
                       , np.nan
                       , np.nan]
                       # Dividends / 3-Year Dividend Growth Rate
                       , [np.nan
                       , np.nan
                       , np.nan]
                       # Income Statement / EBIT
                       , [np.nan
                       , np.nan
                       , np.nan]
                       # Income Statement / EBITDA
                       , [Ticker(self.ticker).yahoo_statistics_p.iloc[48,0]
                       , np.nan
                       , np.nan]
                       # Balance Sheet / Long-Term Debt
                       , [np.nan
                       , np.nan
                       , np.nan]
                       # Cashflow Statement / Free Cash Flow
                       , [np.nan
                       , np.nan
                       , np.nan]
                       # Technical Indicator / 50-Day SMA
                       , [np.nan
                       , np.nan
                       , np.nan]
                       ]
            
        self.valuation_df = pd.DataFrame(array_table , index=arrays, columns = ['Yahoo Finance', 'Morningstar', 'NASDAQ'])
        
        return self.valuation_df
    
    def debt_to_ebitda_yahoo(self):
        
        ebitda = Ticker(self.ticker).yahoo_statistics_p.iloc[48,0]
        debt = Ticker(self.ticker).yahoo_statistics_p.iloc[54,0]
        
        debt_to_ebitda_yahoo_float = debt/ebitda
        
        return debt_to_ebitda_yahoo_float
    
    
    
    
    
    
    
    
    
    
    
    