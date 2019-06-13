$name = 'coala-quickstart'
$pip_version = '9.0.1'
$setuptools_version = '21.2.2'

$ErrorActionPreference = 'SilentlyContinue';
Export-ModuleMember -Variable name, pip_version, setuptools_version -ErrorAction:Ignore
$ErrorActionPreference = 'Continue';
