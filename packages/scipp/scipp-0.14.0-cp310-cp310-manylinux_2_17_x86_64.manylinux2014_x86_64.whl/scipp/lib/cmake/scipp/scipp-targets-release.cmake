#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "scipp::units" for configuration "Release"
set_property(TARGET scipp::units APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(scipp::units PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libscipp-units.so"
  IMPORTED_SONAME_RELEASE "libscipp-units.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS scipp::units )
list(APPEND _IMPORT_CHECK_FILES_FOR_scipp::units "${_IMPORT_PREFIX}/lib64/libscipp-units.so" )

# Import target "scipp::core" for configuration "Release"
set_property(TARGET scipp::core APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(scipp::core PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libscipp-core.so"
  IMPORTED_SONAME_RELEASE "libscipp-core.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS scipp::core )
list(APPEND _IMPORT_CHECK_FILES_FOR_scipp::core "${_IMPORT_PREFIX}/lib64/libscipp-core.so" )

# Import target "scipp::variable" for configuration "Release"
set_property(TARGET scipp::variable APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(scipp::variable PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libscipp-variable.so"
  IMPORTED_SONAME_RELEASE "libscipp-variable.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS scipp::variable )
list(APPEND _IMPORT_CHECK_FILES_FOR_scipp::variable "${_IMPORT_PREFIX}/lib64/libscipp-variable.so" )

# Import target "scipp::dataset" for configuration "Release"
set_property(TARGET scipp::dataset APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(scipp::dataset PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libscipp-dataset.so"
  IMPORTED_SONAME_RELEASE "libscipp-dataset.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS scipp::dataset )
list(APPEND _IMPORT_CHECK_FILES_FOR_scipp::dataset "${_IMPORT_PREFIX}/lib64/libscipp-dataset.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
