#ifndef READ_CSV_PARAMETERS_BASE_CSV_HPP
#define READ_CSV_PARAMETERS_BASE_CSV_HPP

#include <vector>
#include <cstring>
#include "csv.hpp"



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


#endif
