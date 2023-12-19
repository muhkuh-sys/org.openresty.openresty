cmake_minimum_required(VERSION 3.7)

PROJECT("openssl")

INCLUDE(ExternalProject)

SET(VERSION_EXTERNAL "3.1.4")


#----------------------------------------------------------------------------
#
# Extract the sources.
#

ExternalProject_Add(TARGET_openssl
                    PREFIX ${CMAKE_CURRENT_BINARY_DIR}/openssl
                    URL ${CMAKE_CURRENT_SOURCE_DIR}/openssl-${VERSION_EXTERNAL}.tar.gz
                    URL_HASH SHA1=24c5d4308e0f901326f15c274c8c736117966499
                    CONFIGURE_COMMAND true
                    BUILD_COMMAND true
                    INSTALL_COMMAND true
)
