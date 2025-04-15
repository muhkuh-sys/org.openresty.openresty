cmake_minimum_required(VERSION 3.7)

PROJECT("openssl")

INCLUDE(ExternalProject)

SET(VERSION_EXTERNAL "3.5.0")


#----------------------------------------------------------------------------
#
# Extract the sources.
#

ExternalProject_Add(TARGET_openssl
                    PREFIX ${CMAKE_CURRENT_BINARY_DIR}/openssl
                    URL ${CMAKE_CURRENT_SOURCE_DIR}/openssl-${VERSION_EXTERNAL}.tar.gz
                    URL_HASH SHA1=01ba9f9cc97125eab08bbe7206607e404244cf3c
                    CONFIGURE_COMMAND true
                    BUILD_COMMAND true
                    INSTALL_COMMAND true
)
