cmake_minimum_required ( VERSION 3.22 )

project ( HyprScripts++
    VERSION 0.1.0
    LANGUAGES CXX
    DESCRIPTION "Hyprland Scripts written in C++"
)

add_executable ( main )

# find_package(fmt)

target_compile_features ( main PRIVATE
    cxx_std_26
)

# target_compile_options (main PRIVATE
#     -stdlib=libc++
# )

target_compile_options( main PRIVATE

    -Werror

    $<$<CXX_COMPILER_ID:Clang>:
        -Wall
        -Wextra
        -Wpedantic
        -Weverything
        -Wno-c++98-compat
        -Wno-c++98-compat-pedantic

        -Wno-error=padded
        -Wno-error=switch-default
        -Wno-error=unsafe-buffer-usage

        -fsafe-buffer-usage-suggestions
    >

    $<$<CXX_COMPILER_ID:GCC,GNU>:
        -Wall
        -Wextra
        -Wpedantic
    >

)

target_link_options ( main PRIVATE
    -static
    -s
)

target_sources ( main PRIVATE
    src/lib_nullix/config.cpp
    src/lib_nullix/wallpaperManager.cpp
    src/lib_nullix/volumeManager.cpp
    # src/scripts/wallselect.cpp
    src/main.cpp
)

target_include_directories ( main PUBLIC
    include/
)

# target_link_libraries( main PRIVATE fmt::fmt-header-only)
