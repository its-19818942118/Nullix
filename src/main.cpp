#include "lib/config.hpp"
#include <expected>
#include <fmt/format.h>

int main() {
    auto cfgResult = Config::load();

    if (!cfgResult) {
        fmt::println("Config error: {}", cfgResult.error().msg);
        return 1;
    }

    Config& cfg = *cfgResult;
    cfg.printValues();

    cfg.set("theme.active", "Nord");  // No brackets in key!
    cfg.save();

    fmt::println("Theme set to Nord!");
    return 0;
}

