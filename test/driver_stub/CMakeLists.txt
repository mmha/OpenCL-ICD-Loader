add_library(OpenCLDriverStub cl.c cl_ext.c cl_gl.c icd.c)

if("${CMAKE_SYSTEM_NAME}" STREQUAL "Windows")
    target_sources(OpenCLDriverStub PRIVATE driver_stub.def)
endif()

target_link_libraries(OpenCLDriverStub PRIVATE IcdLog)
