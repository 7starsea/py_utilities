cmake_minimum_required(VERSION 3.6)
project(csv_parser)


if (MSVC)
	# Make Visual Studio report accurate C++ version
	# See: https://devblogs.microsoft.com/cppblog/msvc-now-correctly-reports-__cplusplus/
	set(CMAKE_CXX_FLAGS "/EHsc /Zc:__cplusplus")

	if(CMAKE_BUILD_TYPE MATCHES Debug)
		# /Wall emits warnings about the C++ standard library
		set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
	endif(CMAKE_BUILD_TYPE MATCHES Debug)

else()
	set(CMAKE_CXX_FLAGS "-pthread")
	set(CMAKE_CXX_FLAGS_RELEASE "-O3")
	set(CMAKE_CXX_FLAGS_DEBUG "-Og -g -lgcov --coverage")
endif(MSVC)

message("CSV for C++ ${CMAKE_BUILD_TYPE} Build with ${CMAKE_CXX_COMPILER}")

set(SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR}/)


set(SOURCES
	${SOURCE_DIR}/csv_reader.cpp
	${SOURCE_DIR}/csv_row.cpp
	${SOURCE_DIR}/data_type.cpp
	${SOURCE_DIR}/giant_string_buffer.cpp
)


## Main Library
add_library(csv_parser STATIC ${SOURCES})
set_target_properties(csv_parser PROPERTIES LINKER_LANGUAGE CXX)


