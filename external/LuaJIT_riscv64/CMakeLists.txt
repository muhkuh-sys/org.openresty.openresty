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
                    URL ${CMAKE_CURRENT_SOURCE_DIR}/LuaJIT-riscv_GIT5938da937b13.zip
                    URL_HASH SHA1=3076c16525c0fbc46e47781539fc3d8e8fba215f
                    PATCH_COMMAND "${PYTHON_INTERPRETER}" ${CMAKE_HOME_DIRECTORY}/cmake/tools/apply_patches.py --working-folder ${CMAKE_CURRENT_BINARY_DIR}/luajit/src/TARGET_luajit --patch-folder ${CMAKE_CURRENT_SOURCE_DIR}/patches --strip 1
                    CONFIGURE_COMMAND true
#                    BUILD_COMMAND make HOST_CC=gcc CROSS=riscv64-linux-gnu- TARGET_CFLAGS="-march=rv64imafdc_zicsr_zifencei -mabi=lp64d -mriscv-attribute"
#                    BUILD_COMMAND make HOST_CC=gcc CROSS=riscv64-linux-gnu-
#                    BUILD_IN_SOURCE TRUE
                    BUILD_COMMAND true
#                    INSTALL_COMMAND make install DESTDIR=${CMAKE_CURRENT_BINARY_DIR}/install
                    INSTALL_COMMAND true
)
