cmake_minimum_required(VERSION 3.2.3)

PROJECT("pcre")

INCLUDE(ExternalProject)

SET(VERSION_EXTERNAL "8.45")


#----------------------------------------------------------------------------
#
# Extract the sources.
#

ExternalProject_Add(TARGET_pcre
                    PREFIX ${CMAKE_CURRENT_BINARY_DIR}/pcre
                    URL ${CMAKE_CURRENT_SOURCE_DIR}/pcre-${VERSION_EXTERNAL}.tar.bz2
                    URL_HASH SHA1=8463cc88b737e2c3ce7f041922a6ff0c5abbed34
                    CONFIGURE_COMMAND true
                    BUILD_COMMAND true
                    INSTALL_COMMAND true
)
