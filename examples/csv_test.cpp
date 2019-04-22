
#include <iostream>
#include "struct/csv/csv_reader.h"
#include "struct/csv/csv_writer.h"
int main(){
    StockInfo info;
    strcpy(info.stock_id, "000001.SZ");
    info.sett_price = 9.0;
    info.long_vol = 100;
    info.tod_long_vol = 200;
    info.yd_long_vol = 300;

    std::vector<StockInfo> vec_info;
    for(int i = 0; i < 10; ++i){
        info.long_vol += 10;
        vec_info.push_back(info);
    }
    CSVWriter<StockInfo>(vec_info, "info.csv");

    vec_info.clear();
    CSVReader2Vec<StockInfo>("info.csv", vec_info);
    for(StockInfo & item: vec_info){
        std::cout<<item.long_vol<<std::endl;
    }
    CSVWriter<StockInfo>(vec_info, "info2.csv");
    return 0;
}
