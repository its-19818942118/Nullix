#include "lib_nullix/wallpaperManager.hpp"
#include <format>
#include <string_view>

using namespace nullix;
using namespace std::string_view_literals;

auto WallpaperManager::getWallpaperSettings() const -> std::string{
    std::string settings{""};
    for (auto & entry : this->cfg.getOrder()) {
        if (entry.key == "wallpaper.directory" ||
            entry.key == "wallpaper.backend") {
                settings += std::format("[{}] = {}\n", entry.key , entry.value);
        }
    }
    return settings;
}

auto WallpaperManager::getWallpaperBackend() const -> std::string{
    std::string w_backend{""};
    w_backend = this->cfg.getStr("wallpaper.backend"sv);
    return w_backend;
}

auto WallpaperManager::getWallpaperDirectory() const -> std::string{
    std::string w_backend{""};
    w_backend = this->cfg.getStr("wallpaper.directory"sv);
    return w_backend;
}

auto WallpaperManager::setWallpaperBackend(std::string_view value) -> void{
    this->cfg.set("wallpaper.backend"sv, value);
}

auto WallpaperManager::setWallpaperDirectory(std::string_view value) -> void{
    this->cfg.set("wallpaper.directory"sv, value);
}

