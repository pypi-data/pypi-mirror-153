# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nanopb', 'nanopb.generator', 'nanopb.generator.proto']

package_data = \
{'': ['*'], 'nanopb.generator.proto': ['google/protobuf/*']}

install_requires = \
['protobuf>=3.19']

extras_require = \
{':extra == "grpcio-tools"': ['grpcio-tools>=1.46.0']}

entry_points = \
{'console_scripts': ['nanopb_generator = '
                     'nanopb.generator.nanopb_generator:main_cli',
                     'protoc-gen-nanopb = '
                     'nanopb.generator.nanopb_generator:main_plugin']}

setup_kwargs = {
    'name': 'nanopb',
    'version': '0.4.7.dev1329',
    'description': 'Nanopb is a small code-size Protocol Buffers implementation in ansi C. It is especially suitable for use in microcontrollers, but fits any memory restricted system.',
    'long_description': 'Nanopb - Protocol Buffers for Embedded Systems\n==============================================\n\n![Latest change](https://github.com/nanopb/nanopb/actions/workflows/trigger_on_code_change.yml/badge.svg)\n![Weekly build](https://github.com/nanopb/nanopb/actions/workflows/trigger_on_schedule.yml/badge.svg)\n\nNanopb is a small code-size Protocol Buffers implementation in ansi C. It is\nespecially suitable for use in microcontrollers, but fits any memory\nrestricted system.\n\n* **Homepage:** https://jpa.kapsi.fi/nanopb/\n* **Git repository:** https://github.com/nanopb/nanopb/\n* **Documentation:** https://jpa.kapsi.fi/nanopb/docs/\n* **Forum:** https://groups.google.com/forum/#!forum/nanopb\n* **Stable version downloads:** https://jpa.kapsi.fi/nanopb/download/\n* **Pre-release binary packages:** https://github.com/nanopb/nanopb/actions/workflows/binary_packages.yml\n\n\nUsing the nanopb library\n------------------------\nTo use the nanopb library, you need to do two things:\n\n1. Compile your .proto files for nanopb, using `protoc`.\n2. Include *pb_encode.c*, *pb_decode.c* and *pb_common.c* in your project.\n\nThe easiest way to get started is to study the project in "examples/simple".\nIt contains a Makefile, which should work directly under most Linux systems.\nHowever, for any other kind of build system, see the manual steps in\nREADME.txt in that folder.\n\n\nGenerating the headers\n----------------------\nProtocol Buffers messages are defined in a `.proto` file, which follows a standard\nformat that is compatible with all Protocol Buffers libraries. To use it with nanopb,\nyou need to generate `.pb.c` and `.pb.h` files from it:\n\n    python generator/nanopb_generator.py myprotocol.proto  # For source checkout\n    generator-bin/nanopb_generator myprotocol.proto        # For binary package\n\n(Note: For instructions for nanopb-0.3.9.x and older, see the documentation\nof that particular version [here](https://github.com/nanopb/nanopb/blob/maintenance_0.3/README.md))\n\nThe binary packages for Windows, Linux and Mac OS X should contain all necessary\ndependencies, including Python, python-protobuf library and protoc. If you are\nusing a git checkout or a plain source distribution, you will need to install\nPython separately. Once you have Python, you can install the other dependencies\nwith `pip install --upgrade protobuf grpcio-tools`.\n\nYou can further customize the header generation by creating an `.options` file.\nSee [documentation](https://jpa.kapsi.fi/nanopb/docs/concepts.html#modifying-generator-behaviour) for details.\n\n\nRunning the tests\n-----------------\nIf you want to perform further development of the nanopb core, or to verify\nits functionality using your compiler and platform, you\'ll want to run the\ntest suite. The build rules for the test suite are implemented using Scons,\nso you need to have that installed (ex: `sudo apt install scons` or `pip install scons`).\nTo run the tests:\n\n    cd tests\n    scons\n\nThis will show the progress of various test cases. If the output does not\nend in an error, the test cases were successful.\n\nNote: Mac OS X by default aliases \'clang\' as \'gcc\', while not actually\nsupporting the same command line options as gcc does. To run tests on\nMac OS X, use: `scons CC=clang CXX=clang`. Same way can be used to run\ntests with different compilers on any platform.\n\nFor embedded platforms, there is currently support for running the tests\non STM32 discovery board and [simavr](https://github.com/buserror/simavr)\nAVR simulator. Use `scons PLATFORM=STM32` and `scons PLATFORM=AVR` to run\nthese tests.\n\n\nBuild systems and integration\n-----------------------------\nNanopb C code itself is designed to be portable and easy to build\non any platform. Often the bigger hurdle is running the generator which\ntakes in the `.proto` files and outputs `.pb.c` definitions.\n\nThere exist build rules for several systems:\n\n* **Makefiles**: `extra/nanopb.mk`, see `examples/simple`\n* **CMake**: `extra/FindNanopb.cmake`, see `examples/cmake`\n* **SCons**: `tests/site_scons` (generator only)\n* **Bazel**: `BUILD` in source root\n* **Conan**: `conanfile.py` in source root\n* **PlatformIO**: https://platformio.org/lib/show/431/Nanopb\n* **PyPI/pip**: https://pypi.org/project/nanopb/\n* **vcpkg**: https://vcpkg.info/port/nanopb\n\nAnd also integration to platform interfaces:\n\n* **Arduino**: http://platformio.org/lib/show/1385/nanopb-arduino\n\n',
    'author': 'Petteri Aimonen',
    'author_email': 'jpa@npb.mail.kapsi.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://jpa.kapsi.fi/nanopb/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7',
}


setup(**setup_kwargs)
