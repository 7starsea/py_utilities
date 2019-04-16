#include "csv_reader.h"
#include <iostream>
#include <limits>

template<>
bool ReadCsvParametersHelper<StockInfo>(const csv::CSVRow & row, StockInfo & data){
    bool flag = true;

       
    if(row["stock_id"].is_str()){
        
        if(row["stock_id"].get().size() <= sizeof(data.stock_id)-1){
            strncpy(data.stock_id, row["stock_id"].get<std::string>().c_str(), sizeof(data.stock_id)-1);
        }else{
            std::cerr<<">>> String is too bigger for char stock_id[] with py_key stock_id."<<std::endl;
            flag = false;
        }

    }else{
        std::cerr<<">>> Failed to resolve key: stock_id with type: char in DataStruct: StockInfo."<<std::endl;
            flag = false;
    }
    

    data.sett_price = (double)std::numeric_limits<double>::max();   
    if(row["sett_price"].is_num()){
        data.sett_price = (double)(row["sett_price"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: sett_price with type: double in DataStruct: StockInfo."<<std::endl;
            flag = false;
    }
    

    data.long_vol = (int)std::numeric_limits<int>::max();   
    if(row["long_vol"].is_int()){
        data.long_vol = (int)(row["long_vol"].get<int>());
    }else{
        std::cerr<<">>> Failed to resolve key: long_vol with type: int in DataStruct: StockInfo."<<std::endl;
            flag = false;
    }
    

    data.tod_long_vol = (int)std::numeric_limits<int>::max();   
    if(row["tod_long_vol"].is_int()){
        data.tod_long_vol = (int)(row["tod_long_vol"].get<int>());
    }else{
        std::cerr<<">>> Failed to resolve key: tod_long_vol with type: int in DataStruct: StockInfo."<<std::endl;
            flag = false;
    }
    

    data.yd_long_vol = (int)std::numeric_limits<int>::max();   
    if(row["yd_long_vol"].is_int()){
        data.yd_long_vol = (int)(row["yd_long_vol"].get<int>());
    }else{
        std::cerr<<">>> Failed to resolve key: yd_long_vol with type: int in DataStruct: StockInfo."<<std::endl;
            flag = false;
    }
    
    return flag;
}

template<>
bool ReadCsvParametersHelper<QwAdapterMarketDataLV5Field>(const csv::CSVRow & row, QwAdapterMarketDataLV5Field & data){
    bool flag = true;

       
    if(row["instrument_id"].is_str()){
        
        if(row["instrument_id"].get().size() <= sizeof(data.instrument_id)-1){
            strncpy(data.instrument_id, row["instrument_id"].get<std::string>().c_str(), sizeof(data.instrument_id)-1);
        }else{
            std::cerr<<">>> String is too bigger for char instrument_id[] with py_key instrument_id."<<std::endl;
            flag = false;
        }

    }else{
        std::cerr<<">>> Failed to resolve key: instrument_id with type: char in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["update_time"].is_str()){
        
        if(row["update_time"].get().size() <= sizeof(data.update_time)-1){
            strncpy(data.update_time, row["update_time"].get<std::string>().c_str(), sizeof(data.update_time)-1);
        }else{
            std::cerr<<">>> String is too bigger for char update_time[] with py_key update_time."<<std::endl;
            flag = false;
        }

    }else{
        std::cerr<<">>> Failed to resolve key: update_time with type: char in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

    data.stock_update_time = (long long)std::numeric_limits<long long>::max();   
    if(row["stock_update_time"].is_int()){
        data.stock_update_time = (long long)(row["stock_update_time"].get<long long>());
    }else{
        std::cerr<<">>> Failed to resolve key: stock_update_time with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

    data.market_status = (int)std::numeric_limits<int>::max();   
    if(row["market_status"].is_int()){
        data.market_status = (int)(row["market_status"].get<int>());
    }else{
        std::cerr<<">>> Failed to resolve key: market_status with type: int in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

    data.update_mil_sec = (int)std::numeric_limits<int>::max();   
    if(row["update_mil_sec"].is_int()){
        data.update_mil_sec = (int)(row["update_mil_sec"].get<int>());
    }else{
        std::cerr<<">>> Failed to resolve key: update_mil_sec with type: int in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

    data.last_price = (double)std::numeric_limits<double>::max();   
    if(row["last_price"].is_num()){
        data.last_price = (double)(row["last_price"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: last_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["bid_price1"].is_num()){
        data.bid_price[0] = (double)(row["bid_price1"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: bid_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["bid_price2"].is_num()){
        data.bid_price[1] = (double)(row["bid_price2"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: bid_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["bid_price3"].is_num()){
        data.bid_price[2] = (double)(row["bid_price3"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: bid_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["bid_price4"].is_num()){
        data.bid_price[3] = (double)(row["bid_price4"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: bid_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["bid_price5"].is_num()){
        data.bid_price[4] = (double)(row["bid_price5"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: bid_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["ask_price1"].is_num()){
        data.ask_price[0] = (double)(row["ask_price1"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: ask_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["ask_price2"].is_num()){
        data.ask_price[1] = (double)(row["ask_price2"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: ask_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["ask_price3"].is_num()){
        data.ask_price[2] = (double)(row["ask_price3"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: ask_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["ask_price4"].is_num()){
        data.ask_price[3] = (double)(row["ask_price4"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: ask_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["ask_price5"].is_num()){
        data.ask_price[4] = (double)(row["ask_price5"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: ask_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["bid_vol1"].is_int()){
        data.bid_vol[0] = (long long)(row["bid_vol1"].get<long long>());
    }else{
        std::cerr<<">>> Failed to resolve key: bid_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["bid_vol2"].is_int()){
        data.bid_vol[1] = (long long)(row["bid_vol2"].get<long long>());
    }else{
        std::cerr<<">>> Failed to resolve key: bid_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["bid_vol3"].is_int()){
        data.bid_vol[2] = (long long)(row["bid_vol3"].get<long long>());
    }else{
        std::cerr<<">>> Failed to resolve key: bid_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["bid_vol4"].is_int()){
        data.bid_vol[3] = (long long)(row["bid_vol4"].get<long long>());
    }else{
        std::cerr<<">>> Failed to resolve key: bid_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["bid_vol5"].is_int()){
        data.bid_vol[4] = (long long)(row["bid_vol5"].get<long long>());
    }else{
        std::cerr<<">>> Failed to resolve key: bid_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["ask_vol1"].is_int()){
        data.ask_vol[0] = (long long)(row["ask_vol1"].get<long long>());
    }else{
        std::cerr<<">>> Failed to resolve key: ask_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["ask_vol2"].is_int()){
        data.ask_vol[1] = (long long)(row["ask_vol2"].get<long long>());
    }else{
        std::cerr<<">>> Failed to resolve key: ask_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["ask_vol3"].is_int()){
        data.ask_vol[2] = (long long)(row["ask_vol3"].get<long long>());
    }else{
        std::cerr<<">>> Failed to resolve key: ask_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["ask_vol4"].is_int()){
        data.ask_vol[3] = (long long)(row["ask_vol4"].get<long long>());
    }else{
        std::cerr<<">>> Failed to resolve key: ask_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["ask_vol5"].is_int()){
        data.ask_vol[4] = (long long)(row["ask_vol5"].get<long long>());
    }else{
        std::cerr<<">>> Failed to resolve key: ask_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

    data.trade_volume = (long long)std::numeric_limits<long long>::max();   
    if(row["trade_volume"].is_int()){
        data.trade_volume = (long long)(row["trade_volume"].get<long long>());
    }else{
        std::cerr<<">>> Failed to resolve key: trade_volume with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

       
    if(row["last_trade_volume"].is_int()){
        data.last_trade_volume = (long)(row["last_trade_volume"].get<long>());
    }else{
        std::cerr<<">>> Failed to resolve key: last_trade_volume with type: long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

    data.turn_over = (double)std::numeric_limits<double>::max();   
    if(row["turn_over"].is_num()){
        data.turn_over = (double)(row["turn_over"].get<double>());
    }else{
        std::cerr<<">>> Failed to resolve key: turn_over with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    

    data.open_interset = (int)std::numeric_limits<int>::max();   
    if(row["open_interset"].is_int()){
        data.open_interset = (int)(row["open_interset"].get<int>());
    }else{
        std::cerr<<">>> Failed to resolve key: open_interset with type: int in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
    }
    
    return flag;
}

