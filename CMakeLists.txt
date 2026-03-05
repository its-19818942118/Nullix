# cmake_minimum_required ( VERSION 3.22 )

# project ( HyprScripts++
#     VERSION 0.1.0
#     LANGUAGES CXX
#     DESCRIPTION "Hyprland Scripts written in C++"
# )

# add_executable ( main )

# # find_package(fmt)

# target_compile_features ( main PRIVATE
#     cxx_std_26
# )

# # target_compile_options (main PRIVATE
# #     -stdlib=libc++
# # )

# target_compile_options( main PRIVATE

#     -Werror

#     $<$<CXX_COMPILER_ID:Clang>:
#         -Wall
#         -Wextra
#         -Wpedantic
#         -Weverything
#         -Wno-c++98-compat
#         -Wno-c++98-compat-pedantic

#         -Wno-error=padded
#         -Wno-error=switch-default
#         -Wno-error=unsafe-buffer-usage

#         -fsafe-buffer-usage-suggestions
#     >

#     $<$<CXX_COMPILER_ID:GCC,GNU>:
#         -Wall
#         -Wextra
#         -Wpedantic
#     >

# )

# target_link_options ( main PRIVATE
#     -static
#     -s
# )

# target_sources ( main PRIVATE
#     src/lib_nullix/config.cpp
#     src/lib_nullix/wallpaperManager.cpp
#     src/lib_nullix/volumeManager.cpp
#     # src/scripts/wallselect.cpp
#     # src/main.cpp
#     # src/shell.cpp
# )

# target_include_directories ( main PUBLIC
#     include/
# )

# # target_link_libraries( main PRIVATE fmt::fmt-header-only)

cmake_minimum_required ( VERSION 4.2.1 )

set(CMAKE_COLOR_DIAGNOSTICS ON)

project( lib_ullix_
    VERSION 0.0.1
    LANGUAGES CXX
    DESCRIPTION ""
)

add_executable ( a.out )

target_compile_options( a.out PRIVATE
    -g
    -Werror
    -Weverything
    -Wno-c++98-compat
    -Wno-switch-default
    -Wno-c++98-compat-pedantic
    -Wno-covered-switch-default
    -ferror-limit=999999
    -fdiagnostics-color
    -Wno-error=padded
    -Wno-unsafe-buffer-usage
)

target_sources( a.out PUBLIC
    src/main.cpp
)

target_sources( a.out PUBLIC
    src/main.cpp
    lib/nullix/source/host/host.cpp
    lib/nullix/source/config/config.cpp
    lib/nullix/source/wallpaperManager/wallpaperManager.cpp
    lib/nullix/source/diagnostics/error.cpp
    lib/uniqx/source/system/process/ProcPd.cpp
    lib/uniqx/source/system/process/ProcPipe.cpp
    lib/uniqx/source/system/process/SubProcess.cpp
    lib/uniqx/source/system/process/ProcStream.cpp
    lib/uniqx/source/system/process/ProcResult.cpp
    lib/uniqx/source/system/file_tree/FileTree.cpp
    lib/uniqx/source/system/file_tree/PathProxy.cpp
)

target_include_directories(a.out PRIVATE
    lib/uniqx/include/system/file_tree/
    lib/uniqx/include/system/process/
    lib/uniqx/include/system/
    lib/nullix/include/
    lib/uniqx/include/
    lib/nullix/
    lib/uniqx/
    lib/
    lib/
    lib/uniqx/
    lib/nullix/
    lib/uniqx/include/
    lib/nullix/include/
    lib/uniqx/include/system/
    lib/uniqx/include/system/process/
    lib/uniqx/include/system/file_tree/
)
target_compile_features (a.out PRIVATE
    cxx_std_26
)

target_link_options(a.out PRIVATE -lstdc++exp)
target_link_libraries(a.out PRIVATE -lstdc++exp)
