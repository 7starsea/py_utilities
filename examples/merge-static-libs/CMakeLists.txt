cmake_minimum_required(VERSION 3.6.0 FATAL_ERROR)

project(tests-merge-static-libs)

add_library(boo boo.cpp)
add_library(bar bar.cpp)

INCLUDE(libutils.cmake)
MERGE_STATIC_LIBS(boobar bar boo)


add_executable(test_merged main.cpp)
target_link_libraries(test_merged boobar)



