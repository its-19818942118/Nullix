#include <cstdlib>
#include <expected>
#include <filesystem>
#include <format>
#include <print>
#include "lib_nullix/config.hpp"

namespace fs = std::filesystem;
using namespace nullix;
int main(){

    // nullix wallpaper options
    std::string nullixWallpaperDir = "wallpaper.directory";
    std::string nullixWallpaperBackend = "wallpaper.backend";

    // boolean to decide if to use defaultDir or not
    [[maybe_unused]] bool defaultDir = true;

    // loading nullix.conf
    std::expected<Config, Config::errMsg> cfg = Config::load();

    // setting default values for wallpaper options
    std::string HOME = getenv("HOME");
    std::string defaultWallpaperBackend = "swww";
    std::string defaultWallpaperDir = HOME + "/.config/nullix/wallpapers";

    // initializing wallpaper options with default values
    std::string wallpaperDir = defaultWallpaperDir;
    std::string backend = defaultWallpaperBackend;

    // checkinf if nullix.conf loaded successfully or not
    if (cfg) {

        // checking if user provided custom values for wallpaper options
        if (!cfg->getStr(nullixWallpaperDir).empty()) {
            wallpaperDir = cfg->getStr(nullixWallpaperDir);
            defaultDir = false;
        }
        if (!cfg->getStr(nullixWallpaperBackend).empty()) {
            backend = cfg->getStr(nullixWallpaperBackend);
        }
    }
    else {
        std::string errorMsg = std::format("Config error:{}", cfg.error().msg);
        Config::hyprNotify(3, 5000, "0", errorMsg);
    }

    // checking default wallpaper directory and creating if directory don't exist
    if (defaultDir &&( !fs::exists(wallpaperDir) || !fs::is_directory(wallpaperDir))) {
        std::println("Creating: {}", wallpaperDir);
        fs::create_directories(wallpaperDir);
        cfg->hyprNotify(1, 3000, "#44ee44",
            std::format("{} created! Add wallpapers.", wallpaperDir));
        return 0;
    }

    // executing wallpaper command
    const std::string command = "waypaper --folder " + wallpaperDir + " --backend " + backend;
    std::print("{}" , command);
    std::system(command.c_str());
}


