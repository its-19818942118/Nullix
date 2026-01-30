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

        static std::expected<Config, Config::errMsg> load();
        static std::unordered_map<std::string , Config::valueType>& getValidOptionsMap();

        static void hyprNotify(int icon, int timeoutMs,const std::string& color, const std::string& msg);
        void save();

        std::string getStr(const std::string_view key) ;
        int getInt(const std::string_view key) ;
        bool getBool(const std::string_view key);

        void set(const std::string_view key, const std::string_view value);
        void setInt(const std::string_view key, int value);
        void setBool(const std::string_view key, bool value);
        bool has(const std::string& key) const;

        void printValues();


        private:
        static std::expected<std::string, bool> getHOME();
        static std::expected<std::filesystem::path, bool> getNullixConfigPath();
        static constexpr const char* baseConfigPath = "/.config/nullix/nullix.conf";
        static std::unordered_map<std::string, Config::valueType> validOptionsMap;
        std::unordered_map<std::string , std::string> values;
        std::vector<Line> order;
        void changeOrder(std::string_view key ,std::string_view newValue );
        bool needsQuotes(const std::string_view value) const;

};
