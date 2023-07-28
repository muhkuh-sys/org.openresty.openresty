cmake_minimum_required(VERSION 3.7)

PROJECT("external")

#----------------------------------------------------------------------------
#
# Include the projects in the subdirectories.
#

ADD_SUBDIRECTORY(openssl)
ADD_SUBDIRECTORY(pcre)
ADD_SUBDIRECTORY(zlib)

#----------------------------------------------------------------------------
