cmake_minimum_required(VERSION 3.20.0)
project(csp-adapter-zeromq VERSION "0.0.0")
set(CMAKE_CXX_STANDARD 20)

include(CheckCCompilerFlag)
include(CheckLinkerFlag)


# option() should use new make behavior wrt variable clobbering
cmake_policy (SET CMP0077 NEW)

# Allow dep roots from env vars
cmake_policy (SET CMP0074 NEW)

# Set CMP0094 to NEW - find the first version that matches constraints,
# instead of the latest version installed
cmake_policy(SET CMP0094 NEW)

###################################################################################################################################################
# Environment #
###############
if(${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    set(WIN32 ON)
    set(MACOS OFF)
    set(LINUX OFF)
elseif(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
    set(WIN32 OFF)
    set(MACOS ON)
    set(LINUX OFF)
else()
    set(WIN32 OFF)
    set(MACOS OFF)
    set(LINUX ON)
endif()

###################################################################################################################################################
# Paths #
#########
# Custom CMake modules
if(NOT DEFINED CSPZMQ_CMAKE_MODULE_PATH)
    set(CSPZMQ_CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cpp/cmake/modules/")
endif()
list(PREPEND CMAKE_MODULE_PATH "${CSPZMQ_CMAKE_MODULE_PATH}")

###################################################################################################################################################
# Build Configuration #
#######################
find_package(Color)

# Build options
option(CMAKE_BUILD_TYPE "Release/Debug build" RELEASE)
option(CSPZMQ_BUILD_GPROF "Hook into gprof for profiling" OFF)
option(CSPZMQ_MANYLINUX "Build for python's manylinux setup" OFF)
option(CSPZMQ_USE_CCACHE "Build with ccache caching" OFF)
option(CSPZMQ_USE_LD_CLASSIC_MAC "On macOS, link with ld_classic" OFF)

# Normalize build type for downstream comparisons
string(TOLOWER "${CMAKE_BUILD_TYPE}" CMAKE_BUILD_TYPE_LOWER)

# Python library config
set(BUILD_SHARED_LIBS TRUE)
set(CMAKE_MACOSX_RPATH TRUE)
set(CMAKE_SKIP_RPATH FALSE)
set(CMAKE_SKIP_BUILD_RPATH FALSE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
set(CMAKE_INSTALL_NAME_DIR "@rpath")
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Normalize flags
string(REGEX REPLACE "[ ]*-O[^ ]+[ ]*" " " CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
string(REGEX REPLACE "[ ]*-Wl,-O2 -Wl,[^ ]+[ ]*" " " CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS}")
string(REGEX REPLACE "[ ]*-Wl,-O2 -Wl,[^ ]+[ ]*" " " CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS}")

# CCache setup
if(CSPZMQ_USE_CCACHE)
    set(CMAKE_C_COMPILE_LAUNCHER ccache)
    set(CMAKE_CXX_COMPILER_LAUNCHER ccache)
endif()

if(NOT DEFINED CSPZMQ_PYTHON_VERSION)
    set(CSPZMQ_PYTHON_VERSION 3.12)
endif()

if(MACOS)
    # fix for threads on osx
    # assume built-in pthreads on MacOS
    set(CMAKE_THREAD_LIBS_INIT "-lpthread")
    set(CMAKE_HAVE_THREADS_LIBRARY 1)
    set(CMAKE_USE_WIN32_THREADS_INIT 0)
    set(CMAKE_USE_PTHREADS_INIT 1)
    set(THREADS_PREFER_PTHREAD_FLAG ON)

    # don't link against build python
    # https://blog.tim-smith.us/2015/09/python-extension-modules-os-x/
    set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -undefined dynamic_lookup")
endif()


###################################################################################################################################################
# RPath #
#########
if(MACOS)
    set(CMAKE_INSTALL_RPATH "@loader_path/")
elseif(LINUX)
    set(CMAKE_INSTALL_RPATH "\$ORIGIN")
endif()


###################################################################################################################################################
# Flags #
# Optimization Flags
if(WIN32)
    if(CMAKE_BUILD_TYPE_LOWER STREQUAL debug)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /DEBUG /Z7 /Zi")
        add_definitions(-DCSPZMQ_DEBUG)
    else()
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /O2")
        add_definitions(-DNDEBUG)
    endif()

    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /EHsc /MP /bigobj")
    foreach(warning 4244 4251 4267 4275 4290 4786 4305 4996)
        SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /wd${warning}")
    endforeach(warning)
    add_compile_definitions(WIN32 _WIN32)
else()
    if (COVERAGE)
        # TODO windows
        add_compile_options(--coverage)
        set(CMAKE_CXX_FLAGS "-O0 ${CMAKE_CXX_FLAGS}")
        link_libraries(gcov)
    endif ()
    if (GPROF_BUILD)
        set(CMAKE_CXX_FLAGS "-pg ${CMAKE_CXX_FLAGS}")
        set(CMAKE_EXE_LINKER_FLAGS "-pg ${CMAKE_EXE_LINKER_FLAGS}")
        set(CMAKE_SHARED_LINKER_FLAGS "-pg ${CMAKE_SHARED_LINKER_FLAGS}")
    endif ()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fvisibility=hidden")
    if(CMAKE_BUILD_TYPE_LOWER STREQUAL debug)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} \
        -O0 \
        -g3 \
        ")
        add_definitions(-DCSPZMQ_DEBUG)
    else()
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} \
        -O3 \
        -g0 \
        -Wall \
        -Wno-deprecated-declarations \
        -Wno-deprecated \
        ")
        add_definitions(-DNDEBUG)
        if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
            set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} \
            -Wno-maybe-uninitialized \
            ")
        endif()
    endif()
endif()

###################################################################################################################################################
# Messages #
############
# message("\n${Green}Building TT version v${CSPZMQ_VERSION_MAJOR}.${CSPZMQ_VERSION_MINOR}.${CSPZMQ_VERSION_PATCH} [${CSPZMQ_VERSION_COMMIT_SHA}]")
message("\n${Green}Building C++ binding${ColorReset}")
message("\n${Green}Building Python ${Red}${CSPZMQ_PYTHON_VERSION}${Green} binding${ColorReset}")
if(CMAKE_BUILD_TYPE_LOWER STREQUAL debug)
    message("\n${Red}Building DEBUG${ColorReset}")
else()
    message("\n${Green}Building RELEASE${ColorReset}")
endif()
message("\n${Green}CMake Search Path: ${CMAKE_MODULE_PATH}${ColorReset}")


###################################################################################################################################################
# Dependencies #
################
find_package(DepsBase REQUIRED)

# PYTHON
if(CSPZMQ_MANYLINUX)
    # Manylinux docker images have no shared libraries
    # The instead use a statically built python.
    # Cmake's default FindPython can't find the python headers
    # without also finding (or failing to find) the python libraries
    # so we use a custom FindPythonHeaders that is the same as the
    # default, but ignores when the python libraries can't be found.
    message("${Red}Manylinux build has no python shared libraries${ColorReset}")
    find_package(Python ${CSPZMQ_PYTHON_VERSION} EXACT REQUIRED COMPONENTS Interpreter)
    find_package(PythonHeaders ${CSPZMQ_PYTHON_VERSION} EXACT REQUIRED)

    # Run with exact version so its cached for pybind
    find_package(PythonInterp ${CSPZMQ_PYTHON_VERSION} EXACT REQUIRED)
else()
    message("${Cyan}Use python shared libraries${ColorReset}")
    find_package(Python ${CSPZMQ_PYTHON_VERSION} EXACT REQUIRED COMPONENTS Interpreter Development)

    # Run with exact version so its cached for pybind
    find_package(PythonInterp ${CSPZMQ_PYTHON_VERSION} EXACT REQUIRED)
    find_package(PythonLibs ${CSPZMQ_PYTHON_VERSION} EXACT REQUIRED)

    link_directories(${Python_LIBRARY_DIRS})
endif()

message("${Cyan}Using Python ${Python_VERSION}\nPython_INCLUDE_DIRS: ${Python_INCLUDE_DIRS}\nPython_LIBRARIES: ${Python_LIBRARIES}\nPython_EXECUTABLE: ${Python_EXECUTABLE} ${ColorReset}")
include_directories(${Python_INCLUDE_DIRS})

# CSP
find_package(CSP REQUIRED)
message("${Cyan}Found CSP:\n\tincludes in: ${CSP_INCLUDE_DIR}\n\tlibraries in: ${CSP_LIBS_DIR}${ColorReset}")
include_directories(${CSP_INCLUDE_DIR})

###################################################################################################################################################
# Asset names #
################
# prefix is _ by default
set(CMAKE_SHARED_LIBRARY_PREFIX _)

if(NOT WIN32)
    # shared suffix is .so for both linux and mac
    set(CMAKE_SHARED_LIBRARY_SUFFIX .so)

    # static suffix is _static.a # TODO decide if we want this
    set(CMAKE_STATIC_LIBRARY_SUFFIX _static.a)
else()
    # shared suffix is .pyd for windows
    set(CMAKE_SHARED_LIBRARY_SUFFIX .pyd)
endif()


###################################################################################################################################################
# Build assets #
################
include_directories("${CMAKE_SOURCE_DIR}/cpp")
# for autogen
include_directories("${CMAKE_BINARY_DIR}/cpp")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

if(WIN32)
    # On windows, force dlls into lib folder
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
    set(CSPZMQ_RUNTIME_INSTALL_SUBDIR lib/)
else()
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
    set(CSPZMQ_RUNTIME_INSTALL_SUBDIR bin/)
endif()

add_subdirectory(cpp/csp_adapter_zeromq)