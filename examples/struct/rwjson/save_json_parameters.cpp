#include "save_json_parameters.h"

template<>
void SaveJsonParametersHelper<StockInfo>(rapidjson::PrettyWriter<rapidjson::FileWriteStream>  & writer, const StockInfo & data){
    char unsigned_char_helper[2]; unsigned_char_helper[0]=0; unsigned_char_helper[1]=0;
    (void)unsigned_char_helper;
    writer.String(data.stock_id);
    writer.StartObject();

    writer.String("stock_id");
    writer.String(data.stock_id);

    writer.String("sett_price");
    writer.Double((double)data.sett_price);

    writer.String("long_vol");
    writer.Int((int)data.long_vol);

    writer.String("tod_long_vol");
    writer.Int((int)data.tod_long_vol);

    writer.String("yd_long_vol");
    writer.Int((int)data.yd_long_vol);
	writer.EndObject();
}

