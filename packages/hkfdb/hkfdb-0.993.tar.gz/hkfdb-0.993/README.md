# Hong Kong Finance Database

To install the latest version:
```
pip install hkfdb
```

Before you start, please make sure you have done the following:
* **subscribe** the data from our website
* get the personal authToken 
* create an client object from class Database
* have fun!

create client object with authToken and class Database:
```
import hkfdb

authToken = '20210124'
client = hkfdb.Database(authToken)
```

**Major Functions**

Price Data:
* get_hk_stock_ohlc() 
* get_us_stock_ohlc()
* get_hk_fut_ohlc()
* get_hk_deri_daily_market_report()

CCASS Data:
* get_ccass_all_id()
* get_ccass_by_code()
* get_ccass_holding_rank()
* get_ccass_by_id()
* get_ccass_by_id_change()

Index list:
* get_spx_index_const()
* get_hk_index_const()
* get_hk_stock_plate_const()
* get_all_hk_index_name()
* get_all_hk_stock_plate_name()

Earning Calendar:
* get_us_earning_calendar_by_date()
* get_us_earning_calendar_by_code()
* get_hk_earning_calendar_by_code()
* get_hk_earning_calendar_by_date()

Other:
* get_hk_market_cap_hist()
* get_hk_ipo_hist()
* get_north_water()
* get_market_highlight()
* get_hk_buyback_by_date()
* get_hk_buyback_by_code()
* get_basic_hk_stock_info()
