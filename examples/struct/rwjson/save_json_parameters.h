#ifndef SAVE_JSONFILE_USING_RAPIDJSON_20181111T113124
#define SAVE_JSONFILE_USING_RAPIDJSON_20181111T113124
#include "save_parameters_json_base.hpp"
#include "struct.h"

template<>
void SaveJsonParametersHelper<StockInfo>(rapidjson::PrettyWriter<rapidjson::FileWriteStream>  & writer, const StockInfo &);


#endif