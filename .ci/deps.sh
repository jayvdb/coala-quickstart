set -e
set -x

# Choose the python versions to install deps for
case $CIRCLE_NODE_INDEX in
 *) dep_versions=( "3.4.3" ) ;;
 1) dep_versions=( "3.5.1" ) ;;
esac

for dep_version in "${dep_versions[@]}" ; do
  pyenv install -ks $dep_version
  pyenv local $dep_version
  python3 --version

  pip3 install --upgrade pip setuptools
  pip3 install -q -r requirements.txt -r test-requirements.txt
done
