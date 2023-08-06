#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "VTK::RenderingLookingGlass" for configuration "Release"
set_property(TARGET VTK::RenderingLookingGlass APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(VTK::RenderingLookingGlass PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/vtkRenderingLookingGlass.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "VTK::IOImage;VTK::IOMovie;VTK::IOOggTheora"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/vtkmodules/vtkRenderingLookingGlass.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS VTK::RenderingLookingGlass )
list(APPEND _IMPORT_CHECK_FILES_FOR_VTK::RenderingLookingGlass "${_IMPORT_PREFIX}/lib/vtkRenderingLookingGlass.lib" "${_IMPORT_PREFIX}/lib/vtkmodules/vtkRenderingLookingGlass.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
