#include "lib_nullix/config.hpp"
#include "lib_nullix/wallpaperManager.hpp"
#include <expected>
#include <print>
// #include <fmt/base.h>
// #include <fmt/format.h>
using namespace std::string_view_literals;
int main() {
    auto cfgResult = nullix::Config::load();

    if (!cfgResult.has_value()) {
        std::println("Config error: {}", cfgResult.error().msg);
        return 1;
    }

    nullix::Config& cfg = *cfgResult;

    nullix::WallpaperManager wm(cfg);
    std::println("{}", wm.getWallpaperSettings());

    return 0;
}

