tar=$1

cur_file=$(realpath "$0")
cur_dir=$(dirname "$cur_file")
zip_dir=$cur_dir'/zips'

if [[ "$tar" = "zips" || "$tar" = "zip" ]]; then
    echo '[Remove Zips] Removing...'
    rm -rf $zip_dir/*.zip
    echo '[Remove Zips] Done'
else
    echo '[Remove All] Removing...'
    rm -rf $zip_dir/*.zip
    rm -rf $cur_dir/first
    rm -rf $cur_dir/second
    rm -rf $cur_dir/valid
    echo '[Remove All] Done'
fi