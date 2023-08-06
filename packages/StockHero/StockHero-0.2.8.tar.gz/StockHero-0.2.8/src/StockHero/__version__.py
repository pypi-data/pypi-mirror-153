#  ______     __                          __        __    __                               
# /      \   |  \                        |  \      |  \  |  \                              
#|  $$$$$$\ _| $$_     ______    _______ | $$   __ | $$  | $$  ______    ______    ______  
#| $$___\$$|   $$ \   /      \  /       \| $$  /  \| $$__| $$ /      \  /      \  /      \ 
# \$$    \  \$$$$$$  |  $$$$$$\|  $$$$$$$| $$_/  $$| $$    $$|  $$$$$$\|  $$$$$$\|  $$$$$$\
# _\$$$$$$\  | $$ __ | $$  | $$| $$      | $$   $$ | $$$$$$$$| $$    $$| $$   \$$| $$  | $$
#|  \__| $$  | $$|  \| $$__/ $$| $$_____ | $$$$$$\ | $$  | $$| $$$$$$$$| $$      | $$__/ $$
# \$$    $$   \$$  $$ \$$    $$ \$$     \| $$  \$$\| $$  | $$ \$$     \| $$       \$$    $$
#  \$$$$$$     \$$$$   \$$$$$$   \$$$$$$$ \$$   \$$ \$$   \$$  \$$$$$$$ \$$        \$$$$$$ 

__title__ = 'StockHero'
__description__ = 'stock market data downloader'
__url__ = 'https://github.com/RobWen/StockHero'
__version__ = '0.2.8'
__author__ = 'Robert Wenzel'
__author_email__ = 'RobWen.StockHero@gmail.com'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2022 Robert Wenzel'
__thanks__ = 'Thanks to my colleagues @Fraunhofer'

'''
Release History

0.2.8 (05.06.2022)
    - minor fixes

0.2.7 (09.12.2021)
    - added some indizies (Dax, MDax, Euro Stoxx 50, Dow Jones, Nasdaq etc.) from Börse Hamburg / Hannover
    - added Debt-to-EBITDA from Gurufocus
    - fixed some bugs

0.2.6 (22.11.2021)
    - added the Fear and Greed Index from CNN
    - added Historical PE-Ratio from Gurufocus
    - optimised NASDAQ summary, looks much nicer now
    - optimised Morningstar Quote, now also NYSE listed stocks work

0.2.5 (29.10.2021)
    - combined nasdaq_pe_forecast / nasdaq_gr_forecast / nvda.nasdaq_peg_forecast (MultiIndex)
    - added yahoo_statistics_p (a bit of PreProcessing)
    - code cleanup
    - np.NaN for any not valid value
    - None for any empty pd.dataframe
    
'''