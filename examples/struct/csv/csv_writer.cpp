#include "csv_writer.h"
#define CSV_SPLITTER_SYMBOL    ','

/*
 * @brief csv_writer_for datastruct:StockInfo
 */
template<>
std::string CSVWriteRtnHead<StockInfo>()
{
	std::string header;
	header.append("StockId");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("SettPrice");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("LongVol");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("TodLongVol");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("YdLongVol");	header.push_back('\n');

	return header;
}
template<>
void Internal_CSVWriteHead<StockInfo>(std::ostream &ofs)
{
	ofs << CSVWriteRtnHead<StockInfo>();
}
template<>
void Internal_CSVWriteContent<StockInfo>( const StockInfo & data, std::ostream &ofs)
{
	ofs<<data.stock_id<<CSV_SPLITTER_SYMBOL
		<<data.sett_price<<CSV_SPLITTER_SYMBOL
		<<data.long_vol<<CSV_SPLITTER_SYMBOL
		<<data.tod_long_vol<<CSV_SPLITTER_SYMBOL
		<<data.yd_long_vol<<'\n';
}

template<>
void CSVWriter<StockInfo>(const std::vector<StockInfo> & vec_data, std::ostream & ofs){
    for(auto it = vec_data.begin(); it != vec_data.end(); ++it){
        Internal_CSVWriteContent<StockInfo>(*it, ofs);
    }
}
template<>
bool CSVWriter<StockInfo>(const std::vector<StockInfo> & vec_data, const std::string & csv_file){
    std::ofstream ofs( csv_file.c_str(), std::ios::out | std::ios::trunc);
    if(ofs.is_open()){
        ofs.setf(std::ios_base::fixed);
        Internal_CSVWriteHead<StockInfo>(ofs);
        CSVWriter<StockInfo>(vec_data, ofs);
        return true;
    }
    return false;
}


/*
 * @brief csv_writer_for datastruct:QwAdapterMarketDataLV5Field
 */
template<>
std::string CSVWriteRtnHead<QwAdapterMarketDataLV5Field>()
{
	std::string header;
	header.append("InstrumentId");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("UpdateTime");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("StockUpdateTime");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("MarketStatus");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("UpdateMilSec");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("LastPrice");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("BidPrice1");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("BidPrice2");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("BidPrice3");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("BidPrice4");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("BidPrice5");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("AskPrice1");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("AskPrice2");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("AskPrice3");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("AskPrice4");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("AskPrice5");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("BidVol1");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("BidVol2");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("BidVol3");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("BidVol4");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("BidVol5");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("AskVol1");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("AskVol2");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("AskVol3");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("AskVol4");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("AskVol5");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("TradeVolume");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("LastTradeVolume");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("TurnOver");	header.push_back(CSV_SPLITTER_SYMBOL);
	header.append("OpenInterset");	header.push_back('\n');

	return header;
}
template<>
void Internal_CSVWriteHead<QwAdapterMarketDataLV5Field>(std::ostream &ofs)
{
	ofs << CSVWriteRtnHead<QwAdapterMarketDataLV5Field>();
}
template<>
void Internal_CSVWriteContent<QwAdapterMarketDataLV5Field>( const QwAdapterMarketDataLV5Field & data, std::ostream &ofs)
{
	ofs<<data.instrument_id<<CSV_SPLITTER_SYMBOL
		<<data.update_time<<CSV_SPLITTER_SYMBOL
		<<data.stock_update_time<<CSV_SPLITTER_SYMBOL
		<<data.market_status<<CSV_SPLITTER_SYMBOL
		<<data.update_mil_sec<<CSV_SPLITTER_SYMBOL
		<<data.last_price<<CSV_SPLITTER_SYMBOL
		<<data.bid_price[0]<<CSV_SPLITTER_SYMBOL
		<<data.bid_price[1]<<CSV_SPLITTER_SYMBOL
		<<data.bid_price[2]<<CSV_SPLITTER_SYMBOL
		<<data.bid_price[3]<<CSV_SPLITTER_SYMBOL
		<<data.bid_price[4]<<CSV_SPLITTER_SYMBOL
		<<data.ask_price[0]<<CSV_SPLITTER_SYMBOL
		<<data.ask_price[1]<<CSV_SPLITTER_SYMBOL
		<<data.ask_price[2]<<CSV_SPLITTER_SYMBOL
		<<data.ask_price[3]<<CSV_SPLITTER_SYMBOL
		<<data.ask_price[4]<<CSV_SPLITTER_SYMBOL
		<<data.bid_vol[0]<<CSV_SPLITTER_SYMBOL
		<<data.bid_vol[1]<<CSV_SPLITTER_SYMBOL
		<<data.bid_vol[2]<<CSV_SPLITTER_SYMBOL
		<<data.bid_vol[3]<<CSV_SPLITTER_SYMBOL
		<<data.bid_vol[4]<<CSV_SPLITTER_SYMBOL
		<<data.ask_vol[0]<<CSV_SPLITTER_SYMBOL
		<<data.ask_vol[1]<<CSV_SPLITTER_SYMBOL
		<<data.ask_vol[2]<<CSV_SPLITTER_SYMBOL
		<<data.ask_vol[3]<<CSV_SPLITTER_SYMBOL
		<<data.ask_vol[4]<<CSV_SPLITTER_SYMBOL
		<<data.trade_volume<<CSV_SPLITTER_SYMBOL
		<<data.last_trade_volume<<CSV_SPLITTER_SYMBOL
		<<data.turn_over<<CSV_SPLITTER_SYMBOL
		<<data.open_interset<<'\n';
}

template<>
void CSVWriter<QwAdapterMarketDataLV5Field>(const std::vector<QwAdapterMarketDataLV5Field> & vec_data, std::ostream & ofs){
    for(auto it = vec_data.begin(); it != vec_data.end(); ++it){
        Internal_CSVWriteContent<QwAdapterMarketDataLV5Field>(*it, ofs);
    }
}
template<>
bool CSVWriter<QwAdapterMarketDataLV5Field>(const std::vector<QwAdapterMarketDataLV5Field> & vec_data, const std::string & csv_file){
    std::ofstream ofs( csv_file.c_str(), std::ios::out | std::ios::trunc);
    if(ofs.is_open()){
        ofs.setf(std::ios_base::fixed);
        Internal_CSVWriteHead<QwAdapterMarketDataLV5Field>(ofs);
        CSVWriter<QwAdapterMarketDataLV5Field>(vec_data, ofs);
        return true;
    }
    return false;
}


