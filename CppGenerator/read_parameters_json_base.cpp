
#include "read_parameters_json_base.hpp"



bool ReadJsonDocument(const char * fileName, rapidjson::Document & d){
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

