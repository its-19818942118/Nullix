#include "lib/config.hpp"
#include <expected>
#include <fmt/base.h>
#include <fmt/format.h>

int main() {
    auto cfgResult = Config::load();

    if (!cfgResult.has_value()) {
        fmt::println("Config error: {}", cfgResult.error().msg);
        return 1;
    }

    Config& cfg = *cfgResult;
    cfg.printValues();
    fmt::println( "\n");

    cfg.set("theme.active", "nord");
    cfg.set("brightness.step", "100");

    cfg.save();


    return 0;
}

