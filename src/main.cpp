#include "lib_nullix/config.hpp"
#include "lib_nullix/wallpaperManager.hpp"
#include <expected>
#include <print>


using namespace std::string_view_literals;
int main([[maybe_unused]]int argc , [[maybe_unused]]char** argv) {


    auto cfgResult = nullix::Config::load();

    if (!cfgResult.has_value()) {
        std::println("Config error: {}", cfgResult.error().msg);
        return 1;
    }

    [[maybe_unused]] nullix::Config& cfg = *cfgResult;
    
    return 0;
}

