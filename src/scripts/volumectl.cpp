#include "../include/lib_nullix/globals.hpp"
#include "../include/lib_nullix/config.hpp"
#include <fmt/base.h>
#include <print>

using namespace std::string_view_literals;
auto inline
    adjustVolume
    ( const int stepDelta_ )
{
    using namespace nullix;

    constexpr int _maxVolume { 150 } , _minVolume { };

    const int
        _curVolume
        { std::stoi ( utils::system ( "pamixer --get-volume" ) ) }
    ;

    // 3. Apply the math (+10 or -10)
    int _newVolume { _curVolume + stepDelta_ };

    // 4. Constrain (keep it between 0 and 150)
    if ( _newVolume > _maxVolume ) _newVolume = _maxVolume;
    if ( _newVolume < _minVolume ) _newVolume = _minVolume;

    const
      std::string
        _command
        {
            std::format
            (
                "pamixer --set-limit {} --set-volume {}" ,
                _maxVolume , _newVolume
            )
        }
    ;

    system ( _command.c_str ( ) );

    return
        (
            std::format
            (
                "Volume adjusted: {} -> {}" ,
                _curVolume , _newVolume
            )
        )
    ;
}

auto
    main
    ( void )
-> int
{
    auto cfgResult = Config::load();
    if (!cfgResult.has_value()) {
        fmt::println("Config error: {}", cfgResult.error().msg);
        return 1;
    }

    Config cfg = *cfgResult;
    int step = cfg.getInt("volume.step"sv);

    using namespace std::literals;

    std::print ( "{}"sv , nullix::utils::system ( R"sh(echo $USER)sh" ) );

    std::print(stderr, "{}", ::adjustVolume ( step ) );

}
