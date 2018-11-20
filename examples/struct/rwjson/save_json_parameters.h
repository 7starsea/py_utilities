#ifndef SAVE_JSONFILE_USING_RAPIDJSON_20181120T172822
#define SAVE_JSONFILE_USING_RAPIDJSON_20181120T172822
#include "save_parameters_json_base.hpp"
#include "struct.h"

template<>
void SaveJsonParametersHelper<StockInfo>(rapidjson::PrettyWriter<rapidjson::FileWriteStream>  & writer, const StockInfo &);

template<>
void SaveJsonParametersHelper<QwAdapterMarketDataLV5Field>(rapidjson::PrettyWriter<rapidjson::FileWriteStream>  & writer, const QwAdapterMarketDataLV5Field &);


#endif