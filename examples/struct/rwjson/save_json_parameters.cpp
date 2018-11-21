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
    writer.Double(data.sett_price);
    writer.String("long_vol");
    writer.Int(data.long_vol);
    writer.String("tod_long_vol");
    writer.Int(data.tod_long_vol);
    writer.String("yd_long_vol");
    writer.Int(data.yd_long_vol);
    writer.EndObject();
}

template<>
void SaveJsonParametersHelper<QwAdapterMarketDataLV5Field>(rapidjson::PrettyWriter<rapidjson::FileWriteStream>  & writer, const QwAdapterMarketDataLV5Field & data){
    char unsigned_char_helper[2]; unsigned_char_helper[0]=0; unsigned_char_helper[1]=0;
    (void)unsigned_char_helper;
    writer.String(data.instrument_id);
    writer.StartObject();
    writer.String("instrument_id");
    writer.String(data.instrument_id);
    writer.String("update_time");
    writer.String(data.update_time);
    writer.String("stock_update_time");
    writer.Int64(data.stock_update_time);
    writer.String("market_status");
    writer.Int(data.market_status);
    writer.String("update_mil_sec");
    writer.Int(data.update_mil_sec);
    writer.String("last_price");
    writer.Double(data.last_price);
    writer.String("bid_price");
    writer.StartArray();
        writer.Double(data.bid_price[0]);
        writer.Double(data.bid_price[1]);
        writer.Double(data.bid_price[2]);
        writer.Double(data.bid_price[3]);
        writer.Double(data.bid_price[4]);
    writer.EndArray();
    writer.String("ask_price");
    writer.StartArray();
        writer.Double(data.ask_price[0]);
        writer.Double(data.ask_price[1]);
        writer.Double(data.ask_price[2]);
        writer.Double(data.ask_price[3]);
        writer.Double(data.ask_price[4]);
    writer.EndArray();
    writer.String("bid_vol");
    writer.StartArray();
        writer.Int64(data.bid_vol[0]);
        writer.Int64(data.bid_vol[1]);
        writer.Int64(data.bid_vol[2]);
        writer.Int64(data.bid_vol[3]);
        writer.Int64(data.bid_vol[4]);
    writer.EndArray();
    writer.String("ask_vol");
    writer.StartArray();
        writer.Int64(data.ask_vol[0]);
        writer.Int64(data.ask_vol[1]);
        writer.Int64(data.ask_vol[2]);
        writer.Int64(data.ask_vol[3]);
        writer.Int64(data.ask_vol[4]);
    writer.EndArray();
    writer.String("trade_volume");
    writer.Int64(data.trade_volume);
    writer.String("last_trade_volume");
    writer.Int64(data.last_trade_volume);
    writer.String("turn_over");
    writer.Double(data.turn_over);
    writer.String("open_interset");
    writer.Int(data.open_interset);
    writer.EndObject();
}

