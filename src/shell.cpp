#include "lib_nullix/config.hpp"
#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>

auto main ([[maybe_unused]]int argc ,[[maybe_unused]] char** argv) -> int{

    std::unordered_map<std::string , bool> options{
        {"volume",false},
        {"brightness",false},
        {"wallpaper",false},
        {"theme",false},
        {"link",false},
    };

    for (int i = 0 ; i < argc; i++) {
        if (options.contains(argv[i])) {
            options[argv[i]] = true;
        }
    }

    

}
