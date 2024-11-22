import multiprocessing
import os
import os.path
import platform
import subprocess
import sys
from shutil import which
from skbuild import setup

# CMake Options
CMAKE_OPTIONS = (
    ("CSPZMQ_MANYLINUX", "0"),
    # NOTE:
    # - omit vcpkg, need to test for presence
    # - omit ccache, need to test for presence
    # - omit coverage/gprof, not implemented
)


python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
cmake_args = [f"-DCSPZMQ_PYTHON_VERSION={python_version}", "-DBUILD_SHARED_LIBS=ON"]
if "CXX" in os.environ:
    cmake_args.append(f"-DCMAKE_CXX_COMPILER={os.environ['CXX']}")

if "DEBUG" in os.environ:
    cmake_args.append("-DCMAKE_BUILD_TYPE=Debug")

if platform.system() == "Windows":
    import distutils.msvccompiler as dm

    # https://wiki.python.org/moin/WindowsCompilers#Microsoft_Visual_C.2B-.2B-_14.0_with_Visual_Studio_2015_.28x86.2C_x64.2C_ARM.29
    msvc = {
        "12": "Visual Studio 12 2013",
        "14": "Visual Studio 14 2015",
        "14.0": "Visual Studio 14 2015",
        "14.1": "Visual Studio 15 2017",
        "14.2": "Visual Studio 16 2019",
        "14.3": "Visual Studio 17 2022",
    }.get(str(dm.get_build_version()), "Visual Studio 15 2017")
    cmake_args.extend(
        [
            "-G",
            os.environ.get("CSPZMQ_GENERATOR", msvc),
        ]
    )

for cmake_option, default in CMAKE_OPTIONS:
    if os.environ.get(cmake_option, default).lower() in ("1", "on"):
        cmake_args.append(f"-D{cmake_option}=ON")
    else:
        cmake_args.append(f"-D{cmake_option}=OFF")

if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
    os.environ["CMAKE_BUILD_PARALLEL_LEVEL"] = str(multiprocessing.cpu_count())

if platform.system() == "Darwin":
    os.environ["MACOSX_DEPLOYMENT_TARGET"] = os.environ.get("OSX_DEPLOYMENT_TARGET", "10.15")
    cmake_args.append(f'-DCMAKE_OSX_DEPLOYMENT_TARGET={os.environ.get("OSX_DEPLOYMENT_TARGET", "10.15")}')

if which("ccache") and os.environ.get("CSPZMQ_USE_CCACHE", "") != "0":
    cmake_args.append("-DCSPZMQ_USE_CCACHE=On")

print(f"CMake Args: {cmake_args}")

setup(
    name="csp_zeromq_adapter",
    version="0.0.0",
    packages=["csp_zeromq_adapter"],
    cmake_install_dir="csp_zeromq_adapter",
    cmake_args=cmake_args,
)
