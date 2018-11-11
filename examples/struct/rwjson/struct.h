//Configuration:StockInfo


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
