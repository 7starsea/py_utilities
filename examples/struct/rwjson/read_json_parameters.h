#ifndef READ_JSONFILE_USING_RAPIDJSON_20181121T211650
#define READ_JSONFILE_USING_RAPIDJSON_20181121T211650

#include "read_parameters_json_base.hpp"
#include "struct.h"

template<>
bool ReadJsonParametersHelper<StockInfo>(const rapidjson::Value::ConstObject & obj, StockInfo & data);

template<>
bool ReadJsonParametersHelper<QwAdapterMarketDataLV5Field>(const rapidjson::Value::ConstObject & obj, QwAdapterMarketDataLV5Field & data);


#endif