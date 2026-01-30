#include "lib_nullix/config.hpp"
#include <expected>
#include <fmt/base.h>
#include <fmt/format.h>
using namespace std::string_view_literals;
int main() {
    auto cfgResult = Config::load();

    if (!cfgResult.has_value()) {
        fmt::println("Config error: {}", cfgResult.error().msg);
        return 1;
    }

    Config& cfg = *cfgResult;
    cfg.printValues();
    fmt::println( "\n");

    cfg.set("theme.active"sv, "catpuccin"sv);
    cfg.set("brightness.step"sv, "1"sv);

    cfg.save();


    return 0;
}

