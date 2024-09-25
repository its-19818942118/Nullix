#!/usr/bin/env sh


#// set variables

export scrDir="$(dirname "$(realpath "$0")")"
source "${scrDir}/globalcontrol.sh"
export thmbDir

[ -d "${lycrThemeDir}" ] && cacheIn="${lycrThemeDir}" || exit 1
[ -d "${thmbDir}" ] || mkdir -p "${thmbDir}"
[ -d "${cacheDir}/landing" ] || mkdir -p "${cacheDir}/landing"


#// define functions

fn_wallcache()
{
    local x_hash="${1}"
    local x_wall="${2}"
    [ ! -e "${thmbDir}/${x_hash}.thmb" ] && magick "${x_wall}"[0] -strip -resize 1000 -gravity center -extent 1000 -quality 90 "${thmbDir}/${x_hash}.thmb"
    [ ! -e "${thmbDir}/${x_hash}.sqre" ] && magick "${x_wall}"[0] -strip -thumbnail 500x500^ -gravity center -extent 500x500 "${thmbDir}/${x_hash}.sqre"
    [ ! -e "${thmbDir}/${x_hash}.blur" ] && magick "${x_wall}"[0] -strip -scale 10% -blur 0x3 -resize 100% "${thmbDir}/${x_hash}.blur"
    [ ! -e "${thmbDir}/${x_hash}.quad" ] && magick "${thmbDir}/${x_hash}.sqre" \( -size 500x500 xc:white -fill "rgba(0,0,0,0.7)" -draw "polygon 400,500 500,500 500,0 450,0" -fill black -draw "polygon 500,500 500,0 450,500" \) -alpha Off -compose CopyOpacity -composite "${thmbDir}/${x_hash}.png" && mv "${thmbDir}/${x_hash}.png" "${thmbDir}/${x_hash}.quad"
}

fn_wallcache_force()
{
    local x_hash="${1}"
    local x_wall="${2}"
    magick "${x_wall}"[0] -strip -resize 1000 -gravity center -extent 1000 -quality 90 "${thmbDir}/${x_hash}.thmb"
    magick "${x_wall}"[0] -strip -thumbnail 500x500^ -gravity center -extent 500x500 "${thmbDir}/${x_hash}.sqre"
    magick "${x_wall}"[0] -strip -scale 10% -blur 0x3 -resize 100% "${thmbDir}/${x_hash}.blur"
    magick "${thmbDir}/${x_hash}.sqre" \( -size 500x500 xc:white -fill "rgba(0,0,0,0.7)" -draw "polygon 400,500 500,500 500,0 450,0" -fill black -draw "polygon 500,500 500,0 450,500" \) -alpha Off -compose CopyOpacity -composite "${thmbDir}/${x_hash}.png" && mv "${thmbDir}/${x_hash}.png" "${thmbDir}/${x_hash}.quad"
}

export -f fn_wallcache
export -f fn_wallcache_force


#// evaluate options

while getopts "w:t:f" option ; do
    case $option in
    w ) # generate cache for input wallpaper
        if [ -z "${OPTARG}" ] || [ ! -f "${OPTARG}" ] ; then
            echo "Error: Input wallpaper \"${OPTARG}\" not found!"
            exit 1
        fi
        cacheIn="${OPTARG}"
        ;;
    t ) # generate cache for input theme
        cacheIn="$(dirname "${lycrThemeDir}")/${OPTARG}"
        if [ ! -d "${cacheIn}" ] ; then
            echo "Error: Input theme \"${OPTARG}\" not found!"
            exit 1
        fi
        ;;
    f ) # full cache rebuild
        cacheIn="$(dirname "${lycrThemeDir}")"
        mode="_force"
        ;;
    * ) # invalid option
        echo "... invalid option ..."
        echo "$(basename "${0}") -[option]"
        echo "w : generate cache for input wallpaper"
        echo "t : generate cache for input theme"
        echo "f : full cache rebuild"
        exit 1 ;;
    esac
done


#// generate cache

wallPathArray=("${cacheIn}")
wallPathArray+=("${wallAddCustomPath[@]}")
get_hashmap "${wallPathArray[@]}"
parallel --bar --link "fn_wallcache${mode}" ::: "${wallHash[@]}" ::: "${wallList[@]}"
exit 0
