#include "config.hpp"
#include <string_view>


namespace nullix {
    class WallpaperManager{

        public:
            WallpaperManager(Config& c): cfg(c){}

            auto getWallpaperSettings() const -> std::string;
            auto getWallpaperDirectory() const -> std::string;
            auto getWallpaperBackend() const -> std::string;

            auto setWallpaperDirectory(std::string_view value) -> void;
            auto setWallpaperBackend(std::string_view value) -> void;

        private:
            Config cfg;
    };
}
