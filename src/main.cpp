#include "host/host.hpp"
#include "PathProxy.hpp"
#include <print>
#include <string>
#include <unordered_map>

auto printHelpMsg() -> void;
auto printHelpMsg() -> void{
    std::println("{} : {} {} {}","Usage","<source>","[OPTION]","<target>");
    std::println("\n{} :","OPTIONS");
    std::println("  {}   or {} : {}" ,"--link" ,"-ln","creates symlink");
    std::println("  {} or {} : {}" ,"--unlink" ,"-ul","destroys symlink");
}
auto
    main
    ( int argc , char* argv[] )
-> int
{

    if(argc < 3){
        std::println("Not enough arguments!!");
        printHelpMsg();
        return 1;
    }

    std::unordered_map<std::string, bool> validOps{
        {"--link" , false},
        {"--unlink", false},
        {"-ln", false},
        {"-ul", false}
    };

    std::string src , dest;
    for (int i = 1 ; i < argc; i++) {
        if (validOps.contains(argv[i])) {
            validOps[argv[i]] = true;
        }
        else if ((!validOps["--unlink"] && !validOps["-ul"]) && src.empty()) {
            src = argv[i];
        }
        else{
            dest = argv[i];
        }
    }

    nullix::Host host;
    auto target = (host.dirs.home( )/ dest);

    if (validOps["--link"] || validOps["-ln"]) {

        auto res = ( host.dirs.config() / src ).linkTo(target);
    }
    else if (validOps["--unlink"] || validOps["-ul"]) {
        auto r = target.prune();
        if (!r.has_value()) {
            std::println("Something went wrong.");
        }
    }

    return 0;

}
