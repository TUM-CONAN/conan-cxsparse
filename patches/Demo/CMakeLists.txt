cmake_minimum_required(VERSION 2.8)

add_executable(cs_demo1 cs_demo1.c)
target_link_libraries(cs_demo1 CXSparse)

add_executable(cs_demo2 cs_demo2.c cs_demo.c cs_demo.h)
target_link_libraries(cs_demo2 CXSparse)

add_executable(cs_demo3 cs_demo3.c cs_demo.c cs_demo.h)
target_link_libraries(cs_demo3 CXSparse)

add_executable(cs_di_demo1 cs_di_demo1.c )
target_link_libraries(cs_di_demo1 CXSparse)

add_executable(cs_di_demo2 cs_di_demo2.c cs_demo.c cs_demo.h)
target_link_libraries(cs_di_demo2 CXSparse)

add_executable(cs_di_demo3 cs_di_demo3.c cs_demo.c cs_demo.h)
target_link_libraries(cs_di_demo3 CXSparse)
