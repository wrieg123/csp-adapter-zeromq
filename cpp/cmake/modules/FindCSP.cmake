# Find the Python CSP package
# CSP_INCLUDE_DIR
# CSP_LIBS_DIR
# CSP_FOUND
#
# CSP_AUTOGEN
# CSP_LIBRARY
# CSP_CORE_LIBRARY
# CSP_ENGINE_LIBRARY
# CSP_TYPES_LIBRARY
# CSP_TYPES_STATIC_LIBRARY
# CSP_BASELIB_LIBARY
# CSP_BASELIB_STATIC_LIBRARY
# CSP_BASKETLIB_LIBRARY
# CSP_BASKETLIB_STATIC_LIBRARY
# CSP_TESTLIB_LIBRARY
# CSP_MATH_LIBRARY
# CSP_MATH_STATIC_LIBRARY
# CSP_STATS_LIBRARY
# CSP_STATS_STATIC_LIBRARY
# CSP_NPSTATS_LIBRARY
# CSP_ADAPTER_UTILS_LIBRARY
# CSP_KAFKAADAPTER_LIBRARY
# CSP_KAFKAADAPTER_STATIC_LIBRARY
# CSP_PARQUETADAPTER_LIBRARY
# CSP_PARQUETADAPTER_STATIC_LIBRARY
#
# will be set by this script

cmake_minimum_required(VERSION 3.7.2)


# Find out the base path by interrogating the installed csp
find_package(Python ${CSP_PYTHON_VERSION} EXACT REQUIRED COMPONENTS Interpreter)
execute_process(
  COMMAND "${Python_EXECUTABLE}" -c
          "from __future__ import print_function;import os.path;import csp;print(os.path.dirname(csp.__file__), end='')"
  OUTPUT_VARIABLE __csp_base_path)
# Find out the include path
execute_process(
  COMMAND "${Python_EXECUTABLE}" -c
          "from __future__ import print_function;import csp;print(csp.get_include_path(), end='')"
  OUTPUT_VARIABLE __csp_include_path)

# Find out the lib path
if(NOT WIN32)
  execute_process(
    COMMAND "${Python_EXECUTABLE}" -c
              "from __future__ import print_function;import csp;print(csp.get_lib_path(), end='')"
    OUTPUT_VARIABLE __csp_lib_path)
else()
  execute_process(
    COMMAND "${Python_EXECUTABLE}" -c
              "from __future__ import print_function;import csp;print(csp.get_lib_path().replace('lib','Lib'), end='')"
    OUTPUT_VARIABLE __csp_lib_path)
endif()
# And the version
execute_process(
  COMMAND "${Python_EXECUTABLE}" -c
          "from __future__ import print_function;import csp;print(csp.__version__, end='')"
  OUTPUT_VARIABLE __csp_version)

# Now look for files
find_file(CSP_AUTOGEN csp_autogen.py HINTS "${__csp_base_path}/build" NO_DEFAULT_PATH)
find_path(CSP_INCLUDE_DIR csp/core/System.h HINTS "${__csp_include_path}" "${PYTHON_INCLUDE_PATH}" NO_DEFAULT_PATH)

find_path(CSP_LIBS_DIR _cspimpl.so HINTS "${__csp_lib_path}" NO_DEFAULT_PATH)

if(NOT WIN32)
  find_library(CSP_LIBRARY NAMES _cspimpl.so PATHS "${__csp_lib_path}" NO_DEFAULT_PATH)
else()
  find_library(CSP_LIBRARY NAMES _cspimpl.pyd PATHS "${__csp_lib_path}" NO_DEFAULT_PATH)
endif()
find_library(CSP_ADAPTER_UTILS_LIBRARY NAMES libcsp_adapter_utils_static.a PATHS "${__csp_lib_path}" NO_DEFAULT_PATH)

if(CSP_INCLUDE_DIR AND CSP_LIBS_DIR AND CSP_AUTOGEN)
  set(CSP_FOUND 1 CACHE INTERNAL "CSP found")
endif()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(CSP REQUIRED_VARS CSP_INCLUDE_DIR CSP_LIBS_DIR CSP_AUTOGEN VERSION_VAR __csp_version)