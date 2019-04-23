#ifndef CSVWriter_AUTO_GENERATED_AT_20190423T083950_H
#define CSVWriter_AUTO_GENERATED_AT_20190423T083950_H
#include <vector>
#include <string>
#include <fstream>
#include <string>
#include "struct.h"

template<typename DataStruct>
std::string CSVWriteRtnHead(){ return ""; }
template<typename DataStruct>
void Internal_CSVWriteHead(std::ostream &ofs){}
template<typename DataStruct>
void Internal_CSVWriteContent(const DataStruct &, std::ostream &){}
template<typename DataStruct>
void CSVWriter(const std::vector<DataStruct> &, std::ostream &){}
template<typename DataStruct>
bool CSVWriter(const std::vector<DataStruct> &, const std::string &){return false;}


/*
 * @brief csv_writer_for datastruct:StockInfo
 */
template<>
std::string CSVWriteRtnHead<StockInfo>();
template<>
void Internal_CSVWriteHead<StockInfo>(std::ostream &ofs);
template<>
void Internal_CSVWriteContent<StockInfo>(const StockInfo &, std::ostream &);
template<>
void CSVWriter<StockInfo>(const std::vector<StockInfo> &, std::ostream &);
template<>
bool CSVWriter<StockInfo>(const std::vector<StockInfo> &, const std::string &);


/*
 * @brief csv_writer_for datastruct:QwAdapterMarketDataLV5Field
 */
template<>
std::string CSVWriteRtnHead<QwAdapterMarketDataLV5Field>();
template<>
void Internal_CSVWriteHead<QwAdapterMarketDataLV5Field>(std::ostream &ofs);
template<>
void Internal_CSVWriteContent<QwAdapterMarketDataLV5Field>(const QwAdapterMarketDataLV5Field &, std::ostream &);
template<>
void CSVWriter<QwAdapterMarketDataLV5Field>(const std::vector<QwAdapterMarketDataLV5Field> &, std::ostream &);
template<>
bool CSVWriter<QwAdapterMarketDataLV5Field>(const std::vector<QwAdapterMarketDataLV5Field> &, const std::string &);


#endif