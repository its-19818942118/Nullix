#pragma once

#include <cstdlib>
#include <filesystem>
#include <diagnostics.h>
#include <string>

namespace
    std::fs
{
    using namespace ::std::filesystem;
} // this isn't recommended but i always do this. to make it
// std::fs instead of std::filesystem

namespace
    nullix::dirs
{

    auto inline
        homeDir
        ( void )
    -> const std::fs::path
    {

        if
            ( const auto& home = std::getenv ( "HOME" ) )
        {
            return std::fs::path { home };
        }
        else if
            ( const auto& xdgHome = std::getenv ( "$XDG_HOME" ) )
        {
            return std::fs::path { xdgHome };
        }

        return { "/tmp/home/nullix_user" };

    }

    auto inline
        src
        ( void )
    -> const std::fs::path
    {

        return
            {
                std::fs::read_symlink
                ( "/proc/self/exe" ).parent_path ( ).lexically_normal ( )
            }
        ;

    }

    auto inline
        cache
        ( void )
    -> const std::fs::path
    {

        const auto
            path
            {
                homeDir ( ) /
                std::fs::path { ".cache/nullix" }
            }
        ;

        return { path };

    }

    auto inline
        thmbCache
        ( void )
    -> const std::fs::path
    {

        const auto path { cache ( ) / "thumbnails" };

        return { path };

    }

    auto inline
        blurCache
        ( void )
    -> const std::fs::path
    {

        const auto path { cache ( ) / "blur" };

        return { path };

    }

    auto inline
        clrsCache
        ( void )
    -> const std::fs::path
    {

        const auto path { cache ( ) / "clrs" };

        return { path };

    }

}


namespace
    nullix::utils
{

    auto
      inline
        getEnv
        ( std::string envVar_ )
    -> const std::string
    {

        if
            ( envVar_.starts_with('$') )
        {
            envVar_.erase ( 0 , 1 );
        }

        if
            ( const auto& _envVar = std::getenv ( envVar_.c_str ( ) ) )
        {
            return { _envVar };
        }

        return { };

    }

    auto
      inline
        system
        ( const std::string& cmd )
    -> const std::string
    {

        using PipeDeleter = int (*)(FILE*);
        std::unique_ptr <FILE , PipeDeleter>
            pipe
            (
                popen ( cmd.c_str ( ) , "r" ) , pclose
            )
        ;

        if
            ( !pipe )
        {
            throw std::runtime_error ( "popen() failed!" );
        }

        std::string result;
        std::array <char , 4096> buffer { };

        while
            ( true )
        {
            // To satisfy Clang, we must prove the pointer we pass to fread
            // comes from a bounded source. But fread is still a C function.
            // The only way to stop the 'unsafe buffer usage' warning on a libc call
            // is to use the attribute [[unsafe_buffer_usage]] or a pragma.

            #pragma clang diagnostic push
            #pragma clang diagnostic ignored "-Wunsafe-buffer-usage"
            const size_t
                bytesRead
                {
                    std::fread
                    (
                        buffer.data ( ) , 1L ,
                        buffer.size ( ) , pipe.get ( )
                    )
                }
            ;
            #pragma clang diagnostic pop

            if
                ( bytesRead == 0 )
            {
                if
                    ( std::ferror ( pipe.get ( ) ) != 0 )
                {
                    throw std::runtime_error ( "Pipe read error" );
                }

                break;
            }

            result.append ( buffer.data ( ) , bytesRead );

        }

        return { result };
    }

    auto
      inline
        mkdir
        ( const std::fs::path& path )
    -> const std::fs::path
    {

        if
            ( path.is_relative() )
        {

            const auto& relPath { std::fs::current_path ( ) / path };

            std::fs::create_directories ( relPath );
            return { relPath.lexically_normal ( ) };
        }

        else if
            ( path.is_absolute ( ) )
        {

            std::fs::create_directories ( path );

            return { path.lexically_normal ( ) };

        }

        return { };

    }

}
