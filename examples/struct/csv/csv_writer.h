#ifndef CSVWriter_AUTO_GENERATED_AT_20181111T113134_H
#define CSVWriter_AUTO_GENERATED_AT_20181111T113134_H
#include <vector>
#include <string>
#include <fstream>
#include <string>
#include "struct.h"

template<typename DataStruct>
std::string CSVWriteRtnHead(){ return ""; }
template<typename DataStruct>
void Internal_CSVWriteHead(std::ofstream &ofs){}
template<typename DataStruct>
void Internal_CSVWriteContent(const DataStruct &, std::ofstream &){}
template<typename DataStruct>
void CSVWriter(const std::vector<DataStruct> &, std::ofstream &){}
template<typename DataStruct>
bool CSVWriter(const std::vector<DataStruct> &, const std::string &){return false;}


/*
 * @brief csv_writer_for datastruct:StockInfo
 */
template<>
std::string CSVWriteRtnHead<StockInfo>();
template<>
void Internal_CSVWriteHead<StockInfo>(std::ofstream &ofs);
template<>
void Internal_CSVWriteContent<StockInfo>(const StockInfo &, std::ofstream &);
template<>
void CSVWriter<StockInfo>(const std::vector<StockInfo> &, std::ofstream &);
template<>
bool CSVWriter<StockInfo>(const std::vector<StockInfo> &, const std::string &);


#endif