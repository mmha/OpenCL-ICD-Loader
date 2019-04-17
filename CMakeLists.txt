cmake_minimum_required(VERSION 3.1.3)
project(OPENCL_ICD_LOADER VERSION 1.2 LANGUAGES C)

option(BUILD_SHARED_LIBS "Build shared libraries" ON)
set(OPENCL_INCLUDE_DIRS inc CACHE PATH
"Change this to point to a directory \
containing OpenCL header directory 'CL' \
OR copy OpenCL headers to ./inc/CL/")

include(CTest)
find_package(Threads REQUIRED)

add_library(OpenCL icd.c icd_dispatch.c)
target_compile_definitions(OpenCL PUBLIC CL_TARGET_OPENCL_VERSION=220)
target_include_directories(OpenCL PUBLIC ${OPENCL_INCLUDE_DIRS})
target_link_libraries(OpenCL PUBLIC Threads::Threads ${CMAKE_DL_LIBS})
set_target_properties (OpenCL PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR})

if(WIN32)
    target_sources(OpenCL PRIVATE icd_windows.c icd_windows_hkr.c OpenCL.def OpenCL.rc)
    target_link_libraries(OpenCL PUBLIC cfgmgr32.lib)
    if(ENV{DXSDK_DIR})
        target_include_directories(OpenCL PUBLIC $ENV{DXSDK_DIR}/Include)
    endif()
else()
    target_sources(OpenCL PRIVATE icd_linux.c icd_exports.map)
endif()

if(${CMAKE_SYSTEM_NAME} STREQUAL "Linux")
    target_link_options(OpenCL PRIVATE
        -Wl,--version-script
        -Wl,${CMAKE_CURRENT_SOURCE_DIR}/icd_exports.map)
endif()

if(BUILD_TESTING)
    add_subdirectory(test)
endif()

install(TARGETS OpenCL
    RUNTIME DESTINATION bin
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib)