#include "read_json_parameters.h"
#include <iostream>
#include <limits>

template<>
bool ReadJsonParametersHelper<StockInfo>(const rapidjson::Value::ConstObject & obj, StockInfo & data){
    bool flag = true;

    if(obj["stock_id"].GetStringLength() <= sizeof(data.stock_id)-1){
        strncpy(data.stock_id, obj["stock_id"].GetString(), sizeof(data.stock_id)-1);
    }else{
        std::cerr<<">>> String is too bigger for char stock_id[] with py_key stock_id."<<std::endl;
        flag = false;
    }

    data.sett_price = (double)std::numeric_limits<double>::max();
    if(obj.HasMember( "sett_price" )){
        if(obj["sett_price"].IsNumber()){
            data.sett_price = (double)(obj["sett_price"].GetDouble());
        }else{
            std::cerr<<">>> Failed to resolve key: sett_price with type: double in DataStruct: StockInfo."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: sett_price in DataStruct: StockInfo."<<std::endl;
        flag = false;
    }

    data.long_vol = (int)std::numeric_limits<int>::max();
    if(obj.HasMember( "long_vol" )){
        if(obj["long_vol"].IsInt()){
            data.long_vol = (int)(obj["long_vol"].GetInt());
        }else{
            std::cerr<<">>> Failed to resolve key: long_vol with type: int in DataStruct: StockInfo."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: long_vol in DataStruct: StockInfo."<<std::endl;
        flag = false;
    }

    data.tod_long_vol = (int)std::numeric_limits<int>::max();
    if(obj.HasMember( "tod_long_vol" )){
        if(obj["tod_long_vol"].IsInt()){
            data.tod_long_vol = (int)(obj["tod_long_vol"].GetInt());
        }else{
            std::cerr<<">>> Failed to resolve key: tod_long_vol with type: int in DataStruct: StockInfo."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: tod_long_vol in DataStruct: StockInfo."<<std::endl;
        flag = false;
    }

    data.yd_long_vol = (int)std::numeric_limits<int>::max();
    if(obj.HasMember( "yd_long_vol" )){
        if(obj["yd_long_vol"].IsInt()){
            data.yd_long_vol = (int)(obj["yd_long_vol"].GetInt());
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
bool ReadJsonParametersHelper<QwAdapterMarketDataLV5Field>(const rapidjson::Value::ConstObject & obj, QwAdapterMarketDataLV5Field & data){
    bool flag = true;

    if(obj["instrument_id"].GetStringLength() <= sizeof(data.instrument_id)-1){
        strncpy(data.instrument_id, obj["instrument_id"].GetString(), sizeof(data.instrument_id)-1);
    }else{
        std::cerr<<">>> String is too bigger for char instrument_id[] with py_key instrument_id."<<std::endl;
        flag = false;
    }

    
    if(obj.HasMember( "update_time" )){
        if(obj["update_time"].IsString()){
            
    if(obj["update_time"].GetStringLength() <= sizeof(data.update_time)-1){
        strncpy(data.update_time, obj["update_time"].GetString(), sizeof(data.update_time)-1);
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
    if(obj.HasMember( "stock_update_time" )){
        if(obj["stock_update_time"].IsInt64()){
            data.stock_update_time = (long long)(obj["stock_update_time"].GetInt64());
        }else{
            std::cerr<<">>> Failed to resolve key: stock_update_time with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: stock_update_time in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }

    data.market_status = (int)std::numeric_limits<int>::max();
    if(obj.HasMember( "market_status" )){
        if(obj["market_status"].IsInt()){
            data.market_status = (int)(obj["market_status"].GetInt());
        }else{
            std::cerr<<">>> Failed to resolve key: market_status with type: int in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: market_status in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }

    data.update_mil_sec = (int)std::numeric_limits<int>::max();
    if(obj.HasMember( "update_mil_sec" )){
        if(obj["update_mil_sec"].IsInt()){
            data.update_mil_sec = (int)(obj["update_mil_sec"].GetInt());
        }else{
            std::cerr<<">>> Failed to resolve key: update_mil_sec with type: int in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: update_mil_sec in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }

    data.last_price = (double)std::numeric_limits<double>::max();
    if(obj.HasMember( "last_price" )){
        if(obj["last_price"].IsNumber()){
            data.last_price = (double)(obj["last_price"].GetDouble());
        }else{
            std::cerr<<">>> Failed to resolve key: last_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: last_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }

    
    if(obj.HasMember( "bid_price" )){
        if(obj["bid_price"].IsArray()){
            
            const rapidjson::Value & arr = obj["bid_price"];
            if(5 != (int) arr.Size()){
                std::cerr<<">>> array_size of bid_price is invalid in DataStruct QwAdapterMarketDataLV5Field"<<std::endl;
                flag = false;
            }else{
                for (int i = 0; i < 5; ++i){
                    data.bid_price[i] = (double)(arr[i].GetDouble());
                }
            } 

        }else{
            std::cerr<<">>> Failed to resolve key: bid_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: bid_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }

    
    if(obj.HasMember( "ask_price" )){
        if(obj["ask_price"].IsArray()){
            
            const rapidjson::Value & arr = obj["ask_price"];
            if(5 != (int) arr.Size()){
                std::cerr<<">>> array_size of ask_price is invalid in DataStruct QwAdapterMarketDataLV5Field"<<std::endl;
                flag = false;
            }else{
                for (int i = 0; i < 5; ++i){
                    data.ask_price[i] = (double)(arr[i].GetDouble());
                }
            } 

        }else{
            std::cerr<<">>> Failed to resolve key: ask_price with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: ask_price in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }

    
    if(obj.HasMember( "bid_vol" )){
        if(obj["bid_vol"].IsArray()){
            
            const rapidjson::Value & arr = obj["bid_vol"];
            if(5 != (int) arr.Size()){
                std::cerr<<">>> array_size of bid_vol is invalid in DataStruct QwAdapterMarketDataLV5Field"<<std::endl;
                flag = false;
            }else{
                for (int i = 0; i < 5; ++i){
                    data.bid_vol[i] = (long long)(arr[i].GetInt64());
                }
            } 

        }else{
            std::cerr<<">>> Failed to resolve key: bid_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: bid_vol in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }

    
    if(obj.HasMember( "ask_vol" )){
        if(obj["ask_vol"].IsArray()){
            
            const rapidjson::Value & arr = obj["ask_vol"];
            if(5 != (int) arr.Size()){
                std::cerr<<">>> array_size of ask_vol is invalid in DataStruct QwAdapterMarketDataLV5Field"<<std::endl;
                flag = false;
            }else{
                for (int i = 0; i < 5; ++i){
                    data.ask_vol[i] = (long long)(arr[i].GetInt64());
                }
            } 

        }else{
            std::cerr<<">>> Failed to resolve key: ask_vol with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: ask_vol in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }

    data.trade_volume = (long long)std::numeric_limits<long long>::max();
    if(obj.HasMember( "trade_volume" )){
        if(obj["trade_volume"].IsInt64()){
            data.trade_volume = (long long)(obj["trade_volume"].GetInt64());
        }else{
            std::cerr<<">>> Failed to resolve key: trade_volume with type: long long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: trade_volume in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }

    
    if(obj.HasMember( "last_trade_volume" )){
        if(obj["last_trade_volume"].IsInt64()){
            data.last_trade_volume = (long)(obj["last_trade_volume"].GetInt64());
        }else{
            std::cerr<<">>> Failed to resolve key: last_trade_volume with type: long in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: last_trade_volume in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }

    data.turn_over = (double)std::numeric_limits<double>::max();
    if(obj.HasMember( "turn_over" )){
        if(obj["turn_over"].IsNumber()){
            data.turn_over = (double)(obj["turn_over"].GetDouble());
        }else{
            std::cerr<<">>> Failed to resolve key: turn_over with type: double in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
            flag = false;
        }
    }else{
        std::cerr<<">>> Failed to find key: turn_over in DataStruct: QwAdapterMarketDataLV5Field."<<std::endl;
        flag = false;
    }

    data.open_interset = (int)std::numeric_limits<int>::max();
    if(obj.HasMember( "open_interset" )){
        if(obj["open_interset"].IsInt()){
            data.open_interset = (int)(obj["open_interset"].GetInt());
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

