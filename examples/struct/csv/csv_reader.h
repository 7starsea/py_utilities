#ifndef CSVReader_AUTO_GENERATED_AT_20190417T180506_H
#define CSVReader_AUTO_GENERATED_AT_20190417T180506_H
#include <vector>
#include <string>
#include <fstream>
#include <cstring>
#include "csv_parser/csv.hpp"
#include "struct.h"

template<typename DataStruct>
bool CSVReaderHelper(const csv::CSVRow &, DataStruct &){return false;}

template<typename DataStruct>
bool CSVReader2Vec(const char * fileName, std::vector<DataStruct> & vec_data ){
    bool flag = true;
    csv::CSVReader reader(fileName, csv::DEFAULT_CSV_STRICT);    
    csv::CSVRow row;
    DataStruct data;
    while (reader.read_row(row)) {
        
        std::memset(&data, 0, sizeof(DataStruct));;
        if( CSVReaderHelper<DataStruct>(row, data) ){
            vec_data.push_back(data);
        }else{
             flag = false;
        }
    }
    return flag;
};


template<>
bool CSVReaderHelper<StockInfo>(const csv::CSVRow & row, StockInfo & data);

template<>
bool CSVReaderHelper<QwAdapterMarketDataLV5Field>(const csv::CSVRow & row, QwAdapterMarketDataLV5Field & data);


#endif
