cmake_minimum_required(VERSION 3.10)
project(sqlite3)

add_library(sqlite3 src/sqlite3.c include/sqlite3.h)
set_property(TARGET sqlite3 PROPERTY POSITION_INDEPENDENT_CODE ON)
if (NOT WIN32)
    target_link_libraries(sqlite3 dl)
endif()
# no deprecate warnings
set_target_properties(sqlite3 PROPERTIES COMPILE_FLAGS "-Wno-deprecated -Wno-language-extension-token")
