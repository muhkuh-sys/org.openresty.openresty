cmake_minimum_required(VERSION 3.7)

PROJECT("luajit")

INCLUDE(ExternalProject)

SET(VERSION_EXTERNAL "2.1.0")


#----------------------------------------------------------------------------
#
# Extract the sources.
#

ExternalProject_Add(TARGET_luajit
                    PREFIX ${CMAKE_CURRENT_BINARY_DIR}/luajit
                    URL ${CMAKE_CURRENT_SOURCE_DIR}/LuaJIT-riscv_GITa05dc6fe84c3.zip
                    URL_HASH SHA1=0ddc3d04bfa8a2d9f4d96c1a0af75da913cd5551
                    PATCH_COMMAND "${PYTHON_INTERPRETER}" ${CMAKE_HOME_DIRECTORY}/cmake/tools/apply_patches.py --working-folder ${CMAKE_CURRENT_BINARY_DIR}/luajit/src/TARGET_luajit --patch-folder ${CMAKE_CURRENT_SOURCE_DIR}/patches --strip 1
                    CONFIGURE_COMMAND true
#                    BUILD_COMMAND make HOST_CC=gcc CROSS=riscv64-linux-gnu- TARGET_CFLAGS="-march=rv64imafdc_zicsr_zifencei -mabi=lp64d -mriscv-attribute"
#                    BUILD_COMMAND make HOST_CC=gcc CROSS=riscv64-linux-gnu-
#                    BUILD_IN_SOURCE TRUE
                    BUILD_COMMAND true
#                    INSTALL_COMMAND make install DESTDIR=${CMAKE_CURRENT_BINARY_DIR}/install
                    INSTALL_COMMAND true
)
