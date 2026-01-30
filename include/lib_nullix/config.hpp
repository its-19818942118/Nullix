#pragma once

#include <cstddef>
#include <cstring>
#include <expected>
#include <string>
#include <unordered_map>
#include <vector>
#include <filesystem>

class Config {
    public:
        enum class errType{
            invalidKey,
            invalidValue,
            missingAssignment,
            fileNotOpen,
            syntaxErr,
            envNotSet,
        };
        enum class valueType{
            String,
            Int,
            Bool,
        };

        struct errMsg{
            errType et ;
            std::string msg;
            size_t line;
        };

        struct Line{
            std::string raw;
            std::string key;
            std::string value;
            std::string trailing;
        };

        auto static load() -> std::expected<Config, Config::errMsg>;
        static std::unordered_map<std::string , Config::valueType>& getValidOptionsMap();

        auto static hyprNotify(int icon, int timeoutMs,const std::string& color, const std::string& msg) -> void;
        void save();

        auto getStr(const std::string_view key) const -> std::string ;
        auto getInt(const std::string_view key) const -> int ;
        auto getBool(const std::string_view key) const -> bool;

        auto set(const std::string_view key, const std::string_view value) -> void;
        auto setInt(const std::string_view key, int value) -> void;
        auto setBool(const std::string_view key, bool value) -> void;
        auto has(const std::string& key) const -> bool;

        auto printValues() const -> void;

        private:

        static constexpr const char* baseConfigPath = "/.config/nullix/nullix.conf";
        static std::unordered_map<std::string, Config::valueType> validOptionsMap;
        std::unordered_map<std::string , std::string> values;
        std::vector<Line> order;
        
        auto changeOrder(std::string_view key ,std::string_view newValue ) -> void;
        auto needsQuotes(const std::string_view value) const -> bool;
        auto static  getHOME() -> std::expected<std::string, bool>;
        auto static getNullixConfigPath() -> std::expected<std::filesystem::path, bool>;

};
