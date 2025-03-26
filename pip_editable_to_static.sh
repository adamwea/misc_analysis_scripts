# install all editable packages as static packages

pip freeze | grep "^-e" | sed 's/^-e //' | while read -r package; do
    echo "Installing $package"
    # try to install, expect to error sometimes
    # if ! pip install --force-reinstall "$(echo "$package" | sed 's/.*egg=\(.*\)/\1/')"; then
    #     echo "Failed to install $package"
    # fi
done
