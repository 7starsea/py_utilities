#include "read_json_parameters.h"
#include <iostream>
#include <limits>

template<>
bool ReadJsonParametersHelper<StockInfo>(const rapidjson::Value::ConstObject & obj, StockInfo & pConfig){
    bool flag = true;

    strncpy(pConfig.stock_id, obj["stock_id"].GetString(), sizeof(pConfig.stock_id)-1);

    pConfig.sett_price = (double)std::numeric_limits<double>::max();
    if(obj.HasMember( "sett_price" )){
        if(obj["sett_price"].IsNumber()){
            pConfig.sett_price = (double)( obj["sett_price"].GetDouble() );
        }else{
            flag = false;
			std::cerr<<">>> Failed to resolve key: sett_price with type: double in DataStruct: StockInfo."<<std::endl;
        }
    }else{
        
    }

    pConfig.long_vol = (int)std::numeric_limits<int>::max();
    if(obj.HasMember( "long_vol" )){
        if(obj["long_vol"].IsInt()){
            pConfig.long_vol = (int)( obj["long_vol"].GetInt() );
        }else{
            flag = false;
			std::cerr<<">>> Failed to resolve key: long_vol with type: int in DataStruct: StockInfo."<<std::endl;
        }
    }else{
        
    }

    pConfig.tod_long_vol = (int)std::numeric_limits<int>::max();
    if(obj.HasMember( "tod_long_vol" )){
        if(obj["tod_long_vol"].IsInt()){
            pConfig.tod_long_vol = (int)( obj["tod_long_vol"].GetInt() );
        }else{
            flag = false;
			std::cerr<<">>> Failed to resolve key: tod_long_vol with type: int in DataStruct: StockInfo."<<std::endl;
        }
    }else{
        
    }

    pConfig.yd_long_vol = (int)std::numeric_limits<int>::max();
    if(obj.HasMember( "yd_long_vol" )){
        if(obj["yd_long_vol"].IsInt()){
            pConfig.yd_long_vol = (int)( obj["yd_long_vol"].GetInt() );
        }else{
            flag = false;
			std::cerr<<">>> Failed to resolve key: yd_long_vol with type: int in DataStruct: StockInfo."<<std::endl;
        }
    }else{
        
    }
	return flag;
}

