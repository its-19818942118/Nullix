#pragma once

#include <cstddef>
#include <cstring>
#include <expected>
#include <string>
#include <unordered_map>
#include <vector>


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

        static void hyprNotify(int icon, int timeoutMs,const std::string& color, const std::string& msg);

        static std::expected<Config, Config::errMsg> load();
        static std::unordered_map<std::string , Config::valueType>& getValidOptionsMap();

        bool needsQuotes(const std::string& value) const;
        void save();
        std::string getStr(const std::string& key) ;
        int getInt(const std::string& key) ;
        bool getBool(const std::string&key);
        void set(const std::string& key, const std::string& value);
        void setInt(const std::string& key, int value);
        void setBool(const std::string& key, bool value);
        bool has(const std::string& key) const;
        void printValues();

    private:

        static std::unordered_map<std::string, Config::valueType> validOptionsMap;
        std::unordered_map<std::string , std::string> values;
        std::vector<std::pair<std::string, std::string>> order;

};
