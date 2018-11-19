//Configuration:StockInfo,QwAdapterMarketDataLV5Field

typedef char QwInstrumentIdType[31];

struct StockInfo{
    char stock_id[31];
    double sett_price;
    int long_vol;
    int tod_long_vol;
    int yd_long_vol;

    /// used for CPPJsonGenerator
    const char * key_id(){
        return stock_id;
        }
};

//5档行情
struct QwAdapterMarketDataLV5Field{
    //合约名
    QwInstrumentIdType instrument_id;
    //更新时间
    QwInstrumentIdType update_time;
	//更新时间
	long long stock_update_time;
    //合约状态
    int market_status;
    //更新秒数
    int update_mil_sec;
    //最新的成交价
    double last_price;
    //买价 1
    double bid_price[5];
    //卖价 1
    double ask_price[5];
    //买量 1
	long long bid_vol[5];
    //卖量 1
	long long ask_vol[5];
    //成交量
	long long trade_volume;
    //最新成交量
    long last_trade_volume;
    //成交金额
	double turn_over;
    //持仓量
    int open_interset;
};

