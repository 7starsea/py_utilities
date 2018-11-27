# Copyright (c) 2009, 2014, Oracle and/or its affiliates. All rights reserved.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA 


# Following macros are exported
# - MERGE_STATIC_LIBS(target [static-lib1 .... static-libN])
# This macro merges several static libraries into a single one 

set(DIR_OF_MERGE_LIB_CMAKE ${CMAKE_CURRENT_LIST_DIR})  
function(INIT_MERGE_LIB_DIR)
    message("DIR_OF_MERGE_LIB_CMAKE is ${DIR_OF_MERGE_LIB_CMAKE}")
endfunction()

MACRO(MERGE_STATIC_LIBS TARGET_OUTPUT)
    ## To produce a library we need at least one source file.
    ## It is created by ADD_CUSTOM_COMMAND below and will
    ## also help to track dependencies.

    set(TMP_FOLDER ${CMAKE_CURRENT_BINARY_DIR}/TMP_FOLDER_${TARGET_OUTPUT})

    SET(SOURCE_FILE ${TMP_FOLDER}/${TARGET_OUTPUT}_depends.c)
    ADD_LIBRARY(${TARGET_OUTPUT} STATIC ${SOURCE_FILE})
        
    set(STATIC_LIBS)
    FOREACH(LIB ${ARGN})
        GET_TARGET_PROPERTY(LIB_TYPE ${LIB} TYPE)
        IF(LIB_TYPE STREQUAL "STATIC_LIBRARY")
            ADD_DEPENDENCIES(${TARGET_OUTPUT} ${LIB})
            set(STATIC_LIBS ${STATIC_LIBS} $<TARGET_FILE:${LIB}>)
            message(STATUS "Add STATIC LIB:" ${LIB})

        ELSE()
            message(FATAL_ERROR "${LIB} IS NOT A STATIC LIB.")
        ENDIF()
    ENDFOREACH()

    ## Make the generated dummy source file depended on all static input
    ## libs. If input lib changes,the source file is touched
    ## which causes the desired effect (relink).
    ADD_CUSTOM_COMMAND(OUTPUT  ${SOURCE_FILE}
		COMMAND ${CMAKE_COMMAND}  -E make_directory ${TMP_FOLDER}
        COMMAND ${CMAKE_COMMAND}  -E touch ${SOURCE_FILE} )
    
    set(TARGET_LOCATION $<TARGET_FILE:${TARGET_OUTPUT}>)
    IF(MSVC)
        FOREACH(LIB ${ARGN})
            SET(LINKER_EXTRA_FLAGS_DEBUG "${LINKER_EXTRA_FLAGS_DEBUG} ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG}/${LIB}d.lib")
            SET(LINKER_EXTRA_FLAGS_RELEASE "${LINKER_EXTRA_FLAGS_RELEASE} ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE}/${LIB}.lib")
        ENDFOREACH()
        # To merge libs, just pass them to lib.exe command line.
        SET_TARGET_PROPERTIES(${TARGET_OUTPUT} PROPERTIES 
            STATIC_LIBRARY_FLAGS "${LINKER_EXTRA_FLAGS_DEBUG}"
            STATIC_LIBRARY_FLAGS "${LINKER_EXTRA_FLAGS_RELEASE}")
        
    ELSEIF(APPLE)
        # Use OSX's libtool to merge archives (ihandles universal 
        # binaries properly)
        ADD_CUSTOM_COMMAND(TARGET ${TARGET_OUTPUT} POST_BUILD
            COMMAND rm ${TARGET_LOCATION}
            COMMAND /usr/bin/libtool -static -o ${TARGET_LOCATION}  ${STATIC_LIBS} )  

    ELSE()
        # Generic Unix, Cygwin or MinGW. In post-build step, call
        # script, that extracts objects from archives with "ar x" 
        # and repacks them with "ar r"

        INIT_MERGE_LIB_DIR()

        ADD_CUSTOM_COMMAND(TARGET ${TARGET_OUTPUT} POST_BUILD
            COMMAND rm ${TARGET_LOCATION}
            COMMAND python ${DIR_OF_MERGE_LIB_CMAKE}/merge_static_libs.py --verbose ${TARGET_LOCATION} ${STATIC_LIBS}
            WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
            )  
    ENDIF()
ENDMACRO()
