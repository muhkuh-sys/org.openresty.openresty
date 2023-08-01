CMAKE_MINIMUM_REQUIRED(VERSION 3.7)

SET(VERSION_EXTERNAL "1.21.4.2")
SET(VERSION_PACKAGE "1")

PROJECT("openresty")

SET(PROJECT_VERSION "${VERSION_EXTERNAL}.${VERSION_PACKAGE}")

INCLUDE(ExternalProject)


# Python is required for the patch script and the hash tool.
IF(CMAKE_VERSION VERSION_LESS 3.12.0)
	FIND_PACKAGE(PythonInterp 3 REQUIRED)
	SET(PYTHON_INTERPRETER "${PYTHON_EXECUTABLE}")
ELSE(CMAKE_VERSION VERSION_LESS 3.12.0)
	FIND_PACKAGE(Python3 REQUIRED COMPONENTS Interpreter)
	SET(PYTHON_INTERPRETER "${Python3_EXECUTABLE}")
ENDIF(CMAKE_VERSION VERSION_LESS 3.12.0)

#----------------------------------------------------------------------------
#
# Build the project.
#

SET(OPENSSL_SRC_DIR "${CMAKE_BINARY_DIR}/external/openssl/openssl/src/TARGET_openssl")
SET(PCRE_SRC_DIR    "${CMAKE_BINARY_DIR}/external/pcre/pcre/src/TARGET_pcre")
SET(ZLIB_SRC_DIR    "${CMAKE_BINARY_DIR}/external/zlib/zlib/src/TARGET_zlib")

MESSAGE("OPENSSL_SRC_DIR = ${OPENSSL_SRC_DIR}")
MESSAGE("PCRE_SRC_DIR    = ${PCRE_SRC_DIR}")
MESSAGE("ZLIB_SRC_DIR    = ${ZLIB_SRC_DIR}")

SET(LUAJIT_OPTION_HOST "")
SET(LUAJIT_OPTION_CROSS "")
SET(NGX_COMPILER_CC "")
SET(NGX_COMPILER_CPP "")
SET(NGINX_PCRE_CONFIG "")
SET(NGINX_OPENSSL_CONFIG "")
SET(PATCHES_FOLDER "${CMAKE_CURRENT_SOURCE_DIR}/patches/none")
SET(DEPENDS_LUAJIT "")
SET(EXTERNAL_LUAJIT "")

IF(${CMAKE_CROSSCOMPILING})
	# Extract the architecture.
	STRING(REGEX MATCH "[^-]+" CONFIGURE_ARCH ${CONFIGURE_HOST})

	# Set the compile options for LuaJIT.
	SET(LUAJIT_OPTION_HOST "HOST_CC=gcc")
	SET(LUAJIT_OPTION_CROSS "CROSS=${CONFIGURE_HOST}-")

	# Set the compiler for nginx.
	SET(NGINX_COMPILER_CC "--with-cc=${CMAKE_C_COMPILER}")
	SET(NGINX_COMPILER_CPP "--with-cpp=${CONFIGURE_HOST}-cpp")

	# Set the configure options for PCRE and openSSL.
	SET(NGINX_PCRE_CONFIG "--with-pcre-conf-opt=--host=${CONFIGURE_HOST}")
	SET(NGINX_OPENSSL_CONFIG "--with-openssl-opt=\"linux-${CONFIGURE_ARCH} --cross-compile-prefix=${CONFIGURE_HOST}-\"")

	# Select the patches.
	SET(PATCHES_FOLDER "${CMAKE_CURRENT_SOURCE_DIR}/patches/${CONFIGURE_HOST}")

	# Use the external LuaJIT on riscv64.
	IF(${CONFIGURE_HOST} STREQUAL "riscv64-linux-gnu")
		SET(DEPENDS_LUAJIT TARGET_luajit)
		SET(EXTERNAL_LUAJIT "--with-luajit=${CMAKE_BINARY_DIR}/external/luajit/install")
	ENDIF(${CONFIGURE_HOST} STREQUAL "riscv64-linux-gnu")
ENDIF(${CMAKE_CROSSCOMPILING})

SET(LUAJIT_COMMAND "make ${LUAJIT_OPTION_HOST} ${LUAJIT_OPTION_CROSS}")
SET(NGINX_COMMAND "./configure --with-pcre=${PCRE_SRC_DIR} --with-zlib=${ZLIB_SRC_DIR} --with-openssl=${OPENSSL_SRC_DIR} ${EXTERNAL_LUAJIT} --user=www --group=www --build=muhkuh ${NGINX_PCRE_CONFIG} ${NGINX_OPENSSL_CONFIG} ${NGINX_COMPILER_CC} ${NGINX_COMPILER_CPP}")

MESSAGE("*** LuaJit build command: ${LUAJIT_COMMAND}")
MESSAGE("*** configure command: ${NGINX_COMMAND}")

SET(CONFIGURE_CMD "cd bundle/LuaJIT-2.1-20230410 && ${LUAJIT_COMMAND} && cd ../.. && ${NGINX_COMMAND}")

ExternalProject_Add(TARGET_openresty
                    PREFIX ${CMAKE_CURRENT_BINARY_DIR}/openresty
                    URL ${CMAKE_CURRENT_SOURCE_DIR}/openresty-${VERSION_EXTERNAL}.tar.gz
                    URL_HASH SHA1=f8320b4d2d09fea46b01ee115465f8c67a36c024
                    DEPENDS TARGET_openssl TARGET_pcre TARGET_zlib ${DEPENDS_LUAJIT}
                    PATCH_COMMAND "${PYTHON_INTERPRETER}" ${CMAKE_HOME_DIRECTORY}/cmake/tools/apply_patches.py --working-folder ${CMAKE_CURRENT_BINARY_DIR}/openresty/src/TARGET_openresty --patch-folder ${PATCHES_FOLDER} --strip 1
                    CONFIGURE_COMMAND /usr/bin/bash -c -- ${CONFIGURE_CMD}
                    BUILD_IN_SOURCE true
                    BUILD_COMMAND make
                    INSTALL_COMMAND make install DESTDIR=${CMAKE_CURRENT_BINARY_DIR}/install
)


#----------------------------------------------------------------------------
#
# Build a package for the selected platform.
#
SET(CPACK_OUTPUT_FILE_PREFIX ${CMAKE_BINARY_DIR}/../repository/org/openresty/openresty/${PROJECT_VERSION})
SET(CPACK_INCLUDE_TOPLEVEL_DIRECTORY FALSE)
SET(CPACK_PACKAGE_FILE_NAME "openresty-${PROJECT_VERSION}-${JONCHKI_PLATFORM}")

SET(CPACK_GENERATOR "TXZ")
INCLUDE(CPack)

# Package a linux build.

CONFIGURE_FILE(installer/install_linux.lua
               ${CMAKE_CURRENT_BINARY_DIR}/package/install.lua
               @ONLY)

INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/package/install.lua
        DESTINATION .)

# The openresty installation is in the path "/usr/local/...".
# Add the complete "usr" folder to the installation.
INSTALL(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/install/usr DESTINATION .)

CONFIGURE_FILE(installer/openresty.xml
               ${CPACK_OUTPUT_FILE_PREFIX}/openresty-${PROJECT_VERSION}-${JONCHKI_PLATFORM}.xml
               @ONLY)


#-----------------------------------------------------------------------------
#
# Create a custom target named "pack".
# It builds the package and creates the hashes.
#
ADD_CUSTOM_TARGET(pack
                  COMMAND ${CMAKE_MAKE_PROGRAM}
                  COMMAND ${CMAKE_MAKE_PROGRAM} package
                  COMMAND "${PYTHON_INTERPRETER}" ${CMAKE_HOME_DIRECTORY}/cmake/tools/generate_hash.py ${CPACK_OUTPUT_FILE_PREFIX}/openresty-${PROJECT_VERSION}-${JONCHKI_PLATFORM}.xml
                  COMMAND "${PYTHON_INTERPRETER}" ${CMAKE_HOME_DIRECTORY}/cmake/tools/generate_hash.py ${CPACK_OUTPUT_FILE_PREFIX}/openresty-${PROJECT_VERSION}-${JONCHKI_PLATFORM}.tar.xz
                  COMMENT "Pack the artifact and generate the hashes...")


#-----------------------------------------------------------------------------
#
# Filter the pom.xml file.
#
SET(POM_ARTIFACT_ID  "openresty")
SET(POM_GROUP_ID     "org.openresty")
SET(POM_VERSION      "${PROJECT_VERSION}")
SET(POM_PACKAGING    "tar.xz")
CONFIGURE_FILE(installer/pom.xml
               ${CPACK_OUTPUT_FILE_PREFIX}/openresty-${PROJECT_VERSION}.pom
               @ONLY)
