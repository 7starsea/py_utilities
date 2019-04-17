cmake_minimum_required(VERSION 3.6)
project(examples)


add_subdirectory(csv_parser)

include_directories(${CMAKE_CURRENT_LIST_DIR}/csv_parser/)

add_subdirectory(struct/csv)

add_executable(csv_test ${CMAKE_CURRENT_LIST_DIR}/csv_test.cpp)
target_link_libraries(csv_test csv csv_parser pthread)
