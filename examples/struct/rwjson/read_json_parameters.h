#ifndef READ_JSONFILE_USING_RAPIDJSON_20181120T172822
#define READ_JSONFILE_USING_RAPIDJSON_20181120T172822

#include "read_parameters_json_base.hpp"
#include "struct.h"

template<>
bool ReadJsonParametersHelper<StockInfo>(const rapidjson::Value::ConstObject & obj, StockInfo & data);

template<>
bool ReadJsonParametersHelper<QwAdapterMarketDataLV5Field>(const rapidjson::Value::ConstObject & obj, QwAdapterMarketDataLV5Field & data);


#endif