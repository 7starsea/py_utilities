#ifndef SAVE_JSON_PARAMETERS_BASE_JSON_HPP
#define SAVE_JSON_PARAMETERS_BASE_JSON_HPP

#include <map>
#include <vector>
#include <cstdio>
#include "rapidjson/prettywriter.h"
#include "rapidjson/filewritestream.h"

template<typename DataStruct>
void SaveJsonParametersHelper(rapidjson::PrettyWriter<rapidjson::FileWriteStream>  &, const DataStruct&){}


template<typename DataStruct>
bool SaveJSONParameters4Vector(const std::string& fileName, const std::vector<DataStruct> & vecData ){
#if	defined(_WIN32) || defined(_WIN64) || defined(__WIN32__) || defined(__TOS_WIN__) || defined(__WINDOWS__)     
    FILE* fp = fopen(fileName.c_str(), "wb"); // non-Windows use "w"
#else
	FILE* fp = fopen(fileName.c_str(), "w"); // non-Windows use "w"
#endif
	if (fp != NULL){
		char writeBuffer[65536];
		rapidjson::FileWriteStream os(fp, writeBuffer, sizeof(writeBuffer));
		rapidjson::PrettyWriter<rapidjson::FileWriteStream> writer(os);

		writer.StartObject();
		for (auto it = vecData.begin(); it != vecData.end(); ++it){
			SaveJsonParametersHelper<DataStruct>(writer, *it);
		}
		writer.EndObject();
		fclose(fp);
		return true;
	}
	return false;
}


template<typename DataStruct>
bool SaveJSONParameters4Map(const std::string& fileName, const std::map<std::string, DataStruct> & vecData ){
#if	defined(_WIN32) || defined(_WIN64) || defined(__WIN32__) || defined(__TOS_WIN__) || defined(__WINDOWS__)     
    FILE* fp = fopen(fileName.c_str(), "wb"); // non-Windows use "w"
#else
	FILE* fp = fopen(fileName.c_str(), "w"); // non-Windows use "w"
#endif
	if (fp != NULL){
		char writeBuffer[65536];
		rapidjson::FileWriteStream os(fp, writeBuffer, sizeof(writeBuffer));
		rapidjson::PrettyWriter<rapidjson::FileWriteStream> writer(os);

		writer.StartObject();
		for (auto it = vecData.begin(); it != vecData.end(); ++it){
			SaveJsonParametersHelper<DataStruct>(writer, it->second);
		}
		writer.EndObject();
		fclose(fp);
		return true;
	}
	return false;
}


#endif
