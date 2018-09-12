cmake_minimum_required(VERSION 2.8)

project(CXSparse C)

option(BUILD_DEMO "Build all CXSparse demos" OFF)

set(CXSPARSE_INSTALL_BIN_DIR "${CMAKE_INSTALL_PREFIX}/bin" CACHE PATH "Installation directory for executables")
set(CXSPARSE_INSTALL_LIB_DIR "${CMAKE_INSTALL_PREFIX}/lib" CACHE PATH "Installation directory for libraries")
set(CXSPARSE_INSTALL_INC_DIR "${CMAKE_INSTALL_PREFIX}/include" CACHE PATH "Installation directory for headers")


set(CXSPARSE_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/Include/cs.h
                     ${CMAKE_CURRENT_SOURCE_DIR}/Include/SuiteSparse_config.h)


include_directories(${CMAKE_CURRENT_SOURCE_DIR}/Include)

file(GLOB CXSPARSE_SRCS "Source/*.c")

set_source_files_properties(${CXSPARSE_SRCS} PROPERTIES LANGUAGE C)
add_definitions("-DNCOMPLEX")

if(BUILD_SHARED_LIBS)
    set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
    add_library(CXSparse SHARED ${CXSPARSE_SRCS} ${CXSPARSE_HEADERS})
else()
    add_library(CXSparse STATIC ${CXSPARSE_SRCS} ${CXSPARSE_HEADERS})
endif()

install(TARGETS CXSparse
        RUNTIME DESTINATION "${CXSPARSE_INSTALL_BIN_DIR}"
        ARCHIVE DESTINATION "${CXSPARSE_INSTALL_LIB_DIR}"
        LIBRARY DESTINATION "${CXSPARSE_INSTALL_LIB_DIR}" )

install(FILES ${CXSPARSE_HEADERS} DESTINATION "${CXSPARSE_INSTALL_INC_DIR}/CXSparse")

if(BUILD_DEMO)
    add_subdirectory(Demo)
endif()
