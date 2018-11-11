#ifndef READ_JSON_PARAMETERS_BASE_JSON_HPP
#define READ_JSON_PARAMETERS_BASE_JSON_HPP


#include <vector>
#include <map>
#include <cstdio>

#include "rapidjson/document.h"
#include "rapidjson/filereadstream.h"

template<typename DataStruct>
bool ReadJsonParametersHelper(const rapidjson::Value::ConstObject &, DataStruct &){return false;}

bool ReadJsonDocument(const char * fileName, rapidjson::Document & d);

/**
inline bool ReadJsonDocument(const char * fileName, rapidjson::Document & d){
#if	defined(_WIN32) || defined(_WIN64) || defined(__WIN32__) || defined(__TOS_WIN__) || defined(__WINDOWS__) 
	FILE* fp = fopen(fileName, "rb"); // non-Windows use "r"
#else
	FILE* fp = fopen(fileName, "r"); // non-Windows use "r"
#endif
    bool flag = false;
	if (fp != NULL){
		char readBuffer[65536];
		rapidjson::FileReadStream is(fp, readBuffer, sizeof(readBuffer));

		d.ParseStream(is);
		fclose(fp);
        flag = !d.HasParseError() && d.IsObject();
	}
    return flag;
}
*/

template<typename DataStruct>
bool ReadJsonParameters2Struct(const char * fileName, DataStruct & data ){
    rapidjson::Document d;
	if (ReadJsonDocument(fileName, d)){
        std::memset(&data, 0, sizeof(DataStruct));
        
        const rapidjson::Document & dd = d;
        return ReadJsonParametersHelper<DataStruct>(dd.GetObject(), data);
	}
    return false;
}

template<typename DataStruct>
bool ReadJsonParameters2Vector(const char * fileName, std::vector<DataStruct> & vecConfig ){
	bool flag = true;
    rapidjson::Document d;
    if( ReadJsonDocument(fileName, d) ){
        DataStruct data;
        
        for (rapidjson::Value::ConstMemberIterator itr = d.MemberBegin(); itr != d.MemberEnd(); ++itr){
            if (itr->value.IsObject()){
                const rapidjson::Value::ConstObject & obj = itr->value.GetObject();

                memset(&data, 0, sizeof(DataStruct));;
                if( !ReadJsonParametersHelper<DataStruct>(obj, data) ){
                    flag = false;
                }
                vecConfig.push_back(data);
            }
        }

    }else{
        flag = false;
    }
    
    return flag;
};


template<typename DataStruct>
bool ReadJsonParameters2Map(const char * fileName, std::map<std::string, DataStruct> & vecConfig ){
	bool flag = true;
    rapidjson::Document d;
    if( ReadJsonDocument(fileName, d) ){
        DataStruct data;
        
        for (rapidjson::Value::ConstMemberIterator itr = d.MemberBegin(); itr != d.MemberEnd(); ++itr){
            if (itr->value.IsObject()){
                const rapidjson::Value::ConstObject & obj = itr->value.GetObject();

                memset(&data, 0, sizeof(DataStruct));;
                if( !ReadJsonParametersHelper<DataStruct>(obj, data) ){
                    flag = false;
                }
                vecConfig.emplace(itr->name.GetString(), data);
            }
        }
    }else{
        flag = false;
    }
    
    return flag;
};


#endif
