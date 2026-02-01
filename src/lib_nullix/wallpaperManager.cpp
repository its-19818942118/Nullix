#include "lib_nullix/wallpaperManager.hpp"
#include <string_view>

using namespace nullix;
using namespace std::string_view_literals;

auto WallpaperManager::getWallpaperSettings() const -> std::string{
    std::string settings{""};

    // using get function from config class for better performance

    settings += "[wallpaper.directory] = ";
    settings += cfg.getStr("wallpaper.directory"sv) + "\n";
    settings += "[wallpaper.backend] = ";
    settings += cfg.getStr("wallpaper.backend"sv) + "\n";

    return settings;
}

auto WallpaperManager::getWallpaperBackend() const -> std::string{
    std::string w_backend{""};
    w_backend = cfg.getStr("wallpaper.backend"sv);
    return w_backend;
}

auto WallpaperManager::getWallpaperDirectory() const -> std::string{
    std::string w_backend{""};
    w_backend = cfg.getStr("wallpaper.directory"sv);
    return w_backend;
}

auto WallpaperManager::setWallpaperBackend(std::string_view value) -> void{
    cfg.setOption("wallpaper.backend"sv, value);
    cfg.save();
}

auto WallpaperManager::setWallpaperDirectory(std::string_view value) -> void{
    cfg.setOption("wallpaper.directory"sv, value);
    cfg.save();
}

