#ifndef READ_JSONFILE_USING_RAPIDJSON_20181111T113124
#define READ_JSONFILE_USING_RAPIDJSON_20181111T113124

#include "read_parameters_json_base.hpp"
#include "struct.h"

template<>
bool ReadJsonParametersHelper<StockInfo>(const rapidjson::Value::ConstObject & obj, StockInfo & pConfig);


#endif