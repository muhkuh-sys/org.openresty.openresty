cmake_minimum_required(VERSION 3.7.0)

PROJECT("net.zlib-zlib")

INCLUDE(ExternalProject)

SET(VERSION_EXTERNAL "1.3")

#----------------------------------------------------------------------------
#
# Extract the sources.
#

ExternalProject_Add(TARGET_zlib
                    PREFIX ${CMAKE_CURRENT_BINARY_DIR}/zlib
                    URL ${CMAKE_CURRENT_SOURCE_DIR}/zlib-${VERSION_EXTERNAL}.tar.gz
                    URL_HASH SHA1=04d053e4d4064a0fb8f0cbd127f0bfb5fe4eb554
                    CONFIGURE_COMMAND true
                    BUILD_COMMAND true
                    INSTALL_COMMAND true
)
