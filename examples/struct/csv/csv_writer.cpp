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
void Internal_CSVWriteHead<StockInfo>(std::ofstream &ofs)
{
	ofs << CSVWriteRtnHead<StockInfo>();
}
template<>
void Internal_CSVWriteContent<StockInfo>( const StockInfo & data, std::ofstream &ofs)
{
	ofs<<data.stock_id<<CSV_SPLITTER_SYMBOL
		<<data.sett_price<<CSV_SPLITTER_SYMBOL
		<<data.long_vol<<CSV_SPLITTER_SYMBOL
		<<data.tod_long_vol<<CSV_SPLITTER_SYMBOL
		<<data.yd_long_vol<<"\n";
}

template<>
void CSVWriter<StockInfo>(const std::vector<StockInfo> & vec_data, std::ofstream & ofs){
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


