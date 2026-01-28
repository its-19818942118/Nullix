#include "config.hpp"
#include <algorithm>
#include <cctype>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <expected>
#include <format>
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
#include <unistd.h>
#include <sys/types.h>



std::unordered_map<std::string, Config::valueType>& Config::getValidOptionsMap() {
    #pragma clang diagnostic push
    #pragma clang diagnostic ignored "-Wexit-time-destructors"
    static std::unordered_map<std::string, Config::valueType> OptionsSet{
        {"wallpaper.directory", Config::valueType::String},
        {"wallpaper.backend",   Config::valueType::String},
        {"volume.step",         Config::valueType::Int},
        {"brightness.step",     Config::valueType::Int},
        {"theme.active",        Config::valueType::String}
    };
    #pragma clang diagnostic pop
    return OptionsSet;
}

void Config::hyprNotify(
    int icon,
    int timeoutMs,
    const std::string& color,
    const std::string& msg
) {
    pid_t pid = fork();

    if (pid == 0) {
        // child
        std::string iconStr = std::to_string(icon);
        std::string timeStr = std::to_string(timeoutMs);

        execlp(
            "hyprctl",
            "hyprctl",
            "notify",
            iconStr.c_str(),
            timeStr.c_str(),
            color.c_str(),
            msg.c_str(),
            nullptr
        );

        // only reached if execvp fails
        _exit(127);
    }

    // parent does nothing
}


std::expected<Config, Config::errMsg> Config::load(){
    Config cfg;
    std::string base = "/.config/nullix/nullix.conf";
    const char* HOME = std::getenv("HOME");
    if (!HOME) {
        std::string errorMsg = std::format("Home not set.");
        // hyprNotify(3, 5000, "0", errorMsg);
        return std::unexpected(errMsg{
            .et = errType::envNotSet,
            .msg = errorMsg,
            .line = 0
        });

    }
    std::string filePath = std::string(HOME) + base ;
    // std::string filePath = getNullixFile();
    std::ifstream file(filePath);

    if (!file.is_open()) {
        std::string errorMsg = std::format("Config not found: {}", filePath);
        // hyprNotify(1, 3000, "0", errorMsg);
        return std::unexpected(errMsg{.et = errType::fileNotOpen, .msg = errorMsg, .line = 0});
    }



    size_t ln = 0;
    std::string line;

    while (std::getline(file, line)) {
        ln++;
        if(line.empty()){
            cfg.order.emplace_back(Line{
                .raw = "",
                .key = "",
                .value = "",
                .trailing = "",
            });
            continue;
        }



        // trim lambda for trimming whitespaces from left and right of line

        auto trim = [](std::string& s){
            s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char ch) {return !std::isspace(ch);}));
            size_t pos = s.rfind(';');
            if (pos != std::string::npos) {
                s.erase(pos + 1);
            }
            else {
                s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char ch) {return !std::isspace(ch);}).base() , s.end());
            }
        };



        size_t lineEnd = line.find(';');
        std::string trailing = "";

        if (lineEnd != std::string::npos) {
            trailing = line.substr(lineEnd);
        }

        trim(line);

        // if comment then skip
        if (line.starts_with('#')) {
            // cfg.order[ln] = {"",""};

            cfg.order.emplace_back(Line{
                .raw = line,
                .key = "comment",
                .value = "",
                .trailing = trailing,
            });
            continue;
        }


        // finding all required tokens for valid syntax
        size_t openBracket = line.find('[');
        size_t closeBracket = line.find(']');
        size_t epos = line.find('=');
        size_t comment = line.find('#');

        // getting all the valid syntax options
        auto validOptions = Config::getValidOptionsMap();

        // checking lots of condition for proper syntax parsing
        if
            (
                (openBracket != std::string::npos) &&
                (closeBracket != std::string::npos) &&
                (openBracket < closeBracket) &&
                (openBracket + 1 != closeBracket) &&
                (lineEnd != std::string::npos && epos != std::string::npos ) &&
                (comment == std::string::npos || comment > lineEnd)
            )
        {

            std::string option = line.substr(openBracket + 1 , closeBracket - openBracket - 1);
            trim(option);
            if (!validOptions.contains(option)) {
                std::string errorMsg = std::format("[Err] in file : {} [invalid key] at line : {}",filePath,ln);
                // hyprNotify(2, 5000, "0", errorMsg);

                return std::unexpected(errMsg{
                    .et = errType::invalidKey,
                    .msg = errorMsg,
                    .line = ln
                });

            }
            else {
                auto value_t = validOptions.at(option);
                switch (value_t) {
                    case Config::valueType::String :{
                        size_t openingQuote = line.find('"' , epos);
                        size_t closingQuote = line.rfind('"');
                        if
                            (
                                openingQuote != std::string::npos &&
                                closingQuote != std::string::npos &&
                                epos < openingQuote &&
                                lineEnd > closingQuote &&
                                openingQuote < closingQuote
                            )
                        {
                            std::string value = line.substr( openingQuote + 1, closingQuote - openingQuote - 1);
                            cfg.values[option] = value;
                            cfg.order.emplace_back(Line{
                                .raw = line,
                                .key = option,
                                .value = value,
                                .trailing = trailing,
                            });

                        }
                        else {
                            std::string errorMsg = std::format("[Err] in file : {} [invalid value] at line : {}",filePath,ln);
                            // hyprNotify(2, 5000, "0", errorMsg);

                            return std::unexpected(errMsg{
                                .et = errType::invalidValue,
                                .msg = errorMsg,
                                .line = ln
                            });
                        }
                        break;
                    }
                    case Config::valueType::Int :{
                        std::string subLine = line.substr(epos + 1 , lineEnd - epos - 1);
                        trim(subLine);
                        if
                        (
                            subLine.find('"') != std::string::npos||
                            subLine.rfind('"') != std::string::npos

                        )
                        {

                            std::string errorMsg = std::format("[Err] in file : {} [invalid value] at line : {}",filePath,ln);
                            // hyprNotify(2, 5000, "0", errorMsg);

                            return std::unexpected(errMsg{
                                .et = errType::invalidValue,
                                .msg = errorMsg,
                                .line = ln
                            });

                        }
                        std::string errorMsg = std::format("[Err] in file : {} [invalid key] at line : {}",filePath,ln);

                        try {
                            std::stoi(subLine);
                        } catch (...) {
                            return std::unexpected(errMsg{.et = errType::invalidValue,.msg = errorMsg,.line = ln});
                        }

                        cfg.values[option] = subLine;
                        cfg.order.emplace_back(Line{
                            .raw = line,
                            .key = option,
                            .value = subLine,
                            .trailing = trailing,
                        });

                        break;
                    }

                    case Config::valueType::Bool :{
                        std::string subLine = line.substr(epos + 1 , lineEnd - epos - 1);
                        trim(subLine);
                        for (char& c : subLine) {
                            c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
                        }
                        if
                        (
                            subLine.find('"') != std::string::npos||
                            subLine.rfind('"') != std::string::npos ||
                            ( subLine != "true" && subLine != "false")

                        )
                        {
                            std::string errorMsg = std::format("[Err] in file : {} [invalid value] at line : {}",filePath,ln);
                            // hyprNotify(2, 5000, "0", errorMsg);

                                return std::unexpected(errMsg{
                                    .et = errType::invalidValue,
                                    .msg = errorMsg,
                                    .line = ln
                                });
                        }

                        cfg.values[option] = subLine;

                        cfg.order.emplace_back(Line{
                            .raw = line,
                            .key = option,
                            .value = subLine,
                            .trailing = trailing,
                        });


                        break;
                    }
                }

            }

        }
        else {
            std::string errorMsg = std::format("[Err] in file : {} [invalid syntax] at line : {}",filePath,ln);
            // hyprNotify(2, 5000, "0", errorMsg);
            return std::unexpected(errMsg{
                .et = errType::syntaxErr,
                .msg = errorMsg,
                .line = ln
            });
        }



    }
    // std::string msg = std::format("nullix.conf validated successfully. ");
    // hyprNotify(5 ,2000, "0", msg);
    return std::expected<Config, Config::errMsg>(cfg);
}


void Config::printValues(){
    for (const auto& entry : values) {
        std::cout << entry.first << ":" << entry.second << std::endl;
    }
}

void Config::changeOrder(const std::string& key ,const std::string& newValue){
    for (auto & i : this->order) {
        if (i.key == key) {
            i.value = newValue;
        }
    }
}
void Config::save() {

    std::string base = "/.config/nullix/nullix.conf";
    const char* HOME = std::getenv("HOME");
    if (!HOME) {
        return ;
    }
    std::string path = HOME + base;
    std::ofstream file(path);

    for (const auto& l : this->order) {
        if(l.key.empty() ){
            file << "\n";
            continue;
        }
        if (l.key == "comment") {
            file << std::format("{}\n", l.raw);
            continue;
        }
        if (needsQuotes(l.value)) {
            file << std::format("[{}] = \"{}\"{}\n", l.key, l.value , l.trailing);
        } else {
            file << std::format("[{}] = {}{}\n", l.key, l.value , l.trailing);  // NO quotes!
        }
    }
}

bool Config::needsQuotes(const std::string& value) const {
    if (value.empty()) return true;

    // Numbers, booleans → NO quotes
    if (std::all_of(value.begin(), value.end(), ::isdigit) ||
        value == "true" || value == "false" ||
        value == "on" || value == "off" ||
        value == "yes" || value == "no") {
        return false;
    }


    return true;  // Default: quote strings
}

void Config::set(const std::string& key, const std::string& value) {
    auto validMap = getValidOptionsMap();
    if (value.empty()) {

        std::string errorMsg = std::format("Invalid Value: {}", value);
        hyprNotify(3, 2000, "0",errorMsg);
        return;
    }
    if (!validMap.contains(key)) {
        std::string errorMsg = std::format("Invalid key: {}", key);
        hyprNotify(3, 2000, "0",errorMsg);
        return;
    }
    if (!values.contains(key)) {

        values[key] = value;
        order.emplace_back(Line{
            .raw = std::format("[{}] = {}", key , value),
            .key = key,
            .value = value,
            .trailing = ";",
        });

    }
    else {
        values[key]  = value;
        changeOrder(key ,value);
    }
}

void Config::setInt(const std::string& key, int value) {
    set(key, std::to_string(value));
}

void Config::setBool(const std::string& key, bool value) {
    set(key, value ? "true" : "false");
}

bool Config::has(const std::string& key) const {
    return values.contains(key);
}

std::string Config::getStr(const std::string& key) {
    auto it =values.find(key);
    if (it != values.end()) {
        return it->second;
    }
    return "";
}
int Config::getInt(const std::string& key) {
    auto it = values.find(key);
    if (it != values.end()) {
        try { return std::stoi(it->second); }
        catch (...) {
            hyprNotify(3, 2000, "#ffaa00", std::format("Invalid key: {}", key));
        }
    }
    return 0;
}
bool Config::getBool(const std::string& key){
    auto it = values.find(key);
    if (it != values.end()) {
        if (it->second == "true") {
            return true;
        }
        else if (it->second == "false") {
            return false;
        }
        else {
            hyprNotify(3, 2000, "0", std::format("Invalid value: {}",it->second));
        }
    }
    else {
        hyprNotify(3, 2000, "0", std::format("Invalid key: {}",key));
    }
    return false;
}
