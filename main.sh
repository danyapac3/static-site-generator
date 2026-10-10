project_root=$(dirname -- "$(realpath -- "${BASH_SOURCE[0]}")")
main_path="${project_root}/src/main.py"

if [ ! -f "$main_path" ]
then
    echo "There is no file $main_path"
    exit 1
fi

python3 "$main_path"
