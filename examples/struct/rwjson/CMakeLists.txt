CMAKE_MINIMUM_REQUIRED(VERSION 3.4)

file(GLOB headers ${CMAKE_CURRENT_SOURCE_DIR} *.h)
file(GLOB sources ${CMAKE_CURRENT_SOURCE_DIR} *.cpp)

add_library(rwjson ${headers} ${sources})
