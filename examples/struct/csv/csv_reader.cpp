#include "csv_reader.h"
#include <iostream>
#include <limits>

template<>
bool CSVReaderHelper<StockInfo>(const csv::CSVRow & row, StockInfo & data){
    bool flag = true; int ind = -1;

    
    ind = row.find_column("stock_id");
    if( ind >= 0 ){   
        if(row[ind].is_str()){
            
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
    }else{
        std::cerr<<">>> Failed to find key: stock_id in DataStruct: StockInfo."<<std::endl;
        flag = false;
    }
    

    data.sett_price = (double)std::numeric_limits<double>::max();
    ind = row.find_column("sett_price");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.sett_price = (double)(row["sett_price"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: sett_price with type: double in DataStruct: StockInfo."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: sett_price in DataStruct: StockInfo."<<std::endl;
        flag = false;
    }
    

    data.long_vol = (int)std::numeric_limits<int>::max();
    ind = row.find_column("long_vol");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.long_vol = (int)(row["long_vol"].get<int>());
        }else{
            std::cerr<<">>> Failed to resolve key: long_vol with type: int in DataStruct: StockInfo."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: long_vol in DataStruct: StockInfo."<<std::endl;
        flag = false;
    }
    

    data.tod_long_vol = (int)std::numeric_limits<int>::max();
    ind = row.find_column("tod_long_vol");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.tod_long_vol = (int)(row["tod_long_vol"].get<int>());
        }else{
            std::cerr<<">>> Failed to resolve key: tod_long_vol with type: int in DataStruct: StockInfo."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: tod_long_vol in DataStruct: StockInfo."<<std::endl;
        flag = false;
    }
    

    data.yd_long_vol = (int)std::numeric_limits<int>::max();
    ind = row.find_column("yd_long_vol");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.yd_long_vol = (int)(row["yd_long_vol"].get<int>());
        }else{
            std::cerr<<">>> Failed to resolve key: yd_long_vol with type: int in DataStruct: StockInfo."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: yd_long_vol in DataStruct: StockInfo."<<std::endl;
        flag = false;
    }
    
    return flag;
}

template<>
bool CSVReaderHelper<QwAdapterMarketDataLV5Field>(const csv::CSVRow & row, QwAdapterMarketDataLV5Field & data){
    bool flag = true; int ind = -1;

    
    ind = row.find_column("instrument_id");
    if( ind >= 0 ){   
        if(row[ind].is_str()){
            
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
    }else{
        std::cerr<<">>> Failed to find key: instrument_id in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("update_time");
    if( ind >= 0 ){   
        if(row[ind].is_str()){
            
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
    }else{
        std::cerr<<">>> Failed to find key: update_time in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    data.stock_update_time = (long long)std::numeric_limits<long long>::max();
    ind = row.find_column("stock_update_time");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.stock_update_time = (long long)(row["stock_update_time"].get<long long>());
        }else{
            std::cerr<<">>> Failed to resolve key: stock_update_time with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: stock_update_time in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    data.market_status = (int)std::numeric_limits<int>::max();
    ind = row.find_column("market_status");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.market_status = (int)(row["market_status"].get<int>());
        }else{
            std::cerr<<">>> Failed to resolve key: market_status with type: int in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: market_status in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    data.update_mil_sec = (int)std::numeric_limits<int>::max();
    ind = row.find_column("update_mil_sec");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.update_mil_sec = (int)(row["update_mil_sec"].get<int>());
        }else{
            std::cerr<<">>> Failed to resolve key: update_mil_sec with type: int in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: update_mil_sec in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    data.last_price = (double)std::numeric_limits<double>::max();
    ind = row.find_column("last_price");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.last_price = (double)(row["last_price"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: last_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: last_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("bid_price1");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.bid_price[0] = (double)(row["bid_price1"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: bid_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: bid_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("bid_price2");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.bid_price[1] = (double)(row["bid_price2"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: bid_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: bid_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("bid_price3");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.bid_price[2] = (double)(row["bid_price3"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: bid_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: bid_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("bid_price4");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.bid_price[3] = (double)(row["bid_price4"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: bid_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: bid_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("bid_price5");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.bid_price[4] = (double)(row["bid_price5"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: bid_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: bid_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("ask_price1");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.ask_price[0] = (double)(row["ask_price1"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: ask_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: ask_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("ask_price2");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.ask_price[1] = (double)(row["ask_price2"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: ask_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: ask_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("ask_price3");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.ask_price[2] = (double)(row["ask_price3"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: ask_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: ask_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("ask_price4");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.ask_price[3] = (double)(row["ask_price4"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: ask_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: ask_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("ask_price5");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.ask_price[4] = (double)(row["ask_price5"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: ask_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: ask_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("bid_vol1");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.bid_vol[0] = (long long)(row["bid_vol1"].get<long long>());
        }else{
            std::cerr<<">>> Failed to resolve key: bid_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: bid_vol in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("bid_vol2");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.bid_vol[1] = (long long)(row["bid_vol2"].get<long long>());
        }else{
            std::cerr<<">>> Failed to resolve key: bid_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: bid_vol in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("bid_vol3");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.bid_vol[2] = (long long)(row["bid_vol3"].get<long long>());
        }else{
            std::cerr<<">>> Failed to resolve key: bid_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: bid_vol in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("bid_vol4");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.bid_vol[3] = (long long)(row["bid_vol4"].get<long long>());
        }else{
            std::cerr<<">>> Failed to resolve key: bid_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: bid_vol in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("bid_vol5");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.bid_vol[4] = (long long)(row["bid_vol5"].get<long long>());
        }else{
            std::cerr<<">>> Failed to resolve key: bid_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: bid_vol in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("ask_vol1");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.ask_vol[0] = (long long)(row["ask_vol1"].get<long long>());
        }else{
            std::cerr<<">>> Failed to resolve key: ask_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: ask_vol in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("ask_vol2");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.ask_vol[1] = (long long)(row["ask_vol2"].get<long long>());
        }else{
            std::cerr<<">>> Failed to resolve key: ask_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: ask_vol in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("ask_vol3");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.ask_vol[2] = (long long)(row["ask_vol3"].get<long long>());
        }else{
            std::cerr<<">>> Failed to resolve key: ask_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: ask_vol in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("ask_vol4");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.ask_vol[3] = (long long)(row["ask_vol4"].get<long long>());
        }else{
            std::cerr<<">>> Failed to resolve key: ask_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: ask_vol in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("ask_vol5");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.ask_vol[4] = (long long)(row["ask_vol5"].get<long long>());
        }else{
            std::cerr<<">>> Failed to resolve key: ask_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: ask_vol in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    data.trade_volume = (long long)std::numeric_limits<long long>::max();
    ind = row.find_column("trade_volume");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.trade_volume = (long long)(row["trade_volume"].get<long long>());
        }else{
            std::cerr<<">>> Failed to resolve key: trade_volume with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: trade_volume in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    
    ind = row.find_column("last_trade_volume");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.last_trade_volume = (long)(row["last_trade_volume"].get<long>());
        }else{
            std::cerr<<">>> Failed to resolve key: last_trade_volume with type: long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: last_trade_volume in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    data.turn_over = (double)std::numeric_limits<double>::max();
    ind = row.find_column("turn_over");
    if( ind >= 0 ){   
        if(row[ind].is_num()){
            data.turn_over = (double)(row["turn_over"].get<double>());
        }else{
            std::cerr<<">>> Failed to resolve key: turn_over with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: turn_over in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    

    data.open_interset = (int)std::numeric_limits<int>::max();
    ind = row.find_column("open_interset");
    if( ind >= 0 ){   
        if(row[ind].is_int()){
            data.open_interset = (int)(row["open_interset"].get<int>());
        }else{
            std::cerr<<">>> Failed to resolve key: open_interset with type: int in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: open_interset in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }
    
    return flag;
}

