#ifndef CSVReader_AUTO_GENERATED_AT_20190416T222208_H
#define CSVReader_AUTO_GENERATED_AT_20190416T222208_H
#include <vector>
#include <string>
#include <fstream>
#include <cstring>
#include "csv.hpp"
#include "struct.h"

template<typename DataStruct>
bool ReadCsvParametersHelper(const csv::CSVRow &, DataStruct &){return false;}

template<typename DataStruct>
bool ReadCsvnParameters2Vector(const char * fileName, std::vector<DataStruct> & vec_data ){
    bool flag = true;
    csv::CSVReader reader(fileName, csv::DEFAULT_CSV_STRICT);    
    csv::CSVRow row;
    DataStruct data;
    while (reader.read_row(row)) {
        
        std::memset(&data, 0, sizeof(DataStruct));;
        if( ReadCsvParametersHelper<DataStruct>(row, data) ){
            vec_data.push_back(data);
        }else{
             flag = false;
        }
    }
    return flag;
};


template<>
bool ReadCsvParametersHelper<StockInfo>(const csv::CSVRow & row, StockInfo & data);

template<>
bool ReadCsvParametersHelper<QwAdapterMarketDataLV5Field>(const csv::CSVRow & row, QwAdapterMarketDataLV5Field & data);


#endif