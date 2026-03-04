#include <filesystem>
#include <fstream>
#include <cstdlib>
#include <print>
#include <string>

namespace fs = std::filesystem;

int main() {
    const char* home = std::getenv("HOME");
    if (!home) {
        std::println(stderr,"{}\n","HOME not set");
        return 1;
    }
    std::string baseStr = std::getenv("HOME");
    baseStr += "./config/nullix";
    fs::path base = fs::path(home) / ".config" / "nullix";

    if (fs::exists(base)) {
        std::println("{} {}" , "Nullix already initialized at",baseStr);
        return 0;
    }

    // Create directory tree
    fs::create_directories(base / "bin");
    // fs::create_directories(base / "state");
    fs::create_directories(base / "templates");
    fs::create_directories(base / "generated");
    // fs::create_directories(base / "wallpapers");
    fs::create_directories(base / "themes");

    // Create default config
    std::ofstream config(base / "nullix.conf");
    config <<
        "# Nullix configuration\n"
        "\n"
        "wallpaper.dir = " << base << "/wallpapers\n"
        "wallpaper.backend = swww\n"
        "\n"
        "volume.step = 5\n"
        "brightness.step = 5\n"
        "\n";
    config.close();

    std::println("{}\n", "Nullix initialized successfully.");
    return 0;
}
