cmake_minimum_required(VERSION 2.6)

project(sep C)

LIST(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules/")
include(GNUInstallDirs)

set(SOURCES
   ${CMAKE_CURRENT_SOURCE_DIR}/src/analyse.c
   ${CMAKE_CURRENT_SOURCE_DIR}/src/convolve.c
   ${CMAKE_CURRENT_SOURCE_DIR}/src/deblend.c
   ${CMAKE_CURRENT_SOURCE_DIR}/src/extract.c
   ${CMAKE_CURRENT_SOURCE_DIR}/src/lutz.c
   ${CMAKE_CURRENT_SOURCE_DIR}/src/aperture.c
   ${CMAKE_CURRENT_SOURCE_DIR}/src/background.c
   ${CMAKE_CURRENT_SOURCE_DIR}/src/util.c
   )

add_library(sep SHARED ${SOURCES})
set_target_properties(sep PROPERTIES OUTPUT_NAME sep)
set_target_properties(sep PROPERTIES VERSION 0.6.0 SOVERSION 0)
set_target_properties(sep PROPERTIES C_VISIBILITY_PRESET hidden)
target_include_directories(sep PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src ${CFITSIO_INCLUDE_DIR})
target_link_directories(sep PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)

if (MSVC)
   add_definitions(-D_USE_MATH_DEFINES)
else ()
   add_compile_options(-Wcast-qual)
   target_link_libraries(sep m)
endif()

install(TARGETS sep LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/sep.h DESTINATION include)
