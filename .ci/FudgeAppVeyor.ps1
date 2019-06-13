. $env:FudgeCI/FudgeGenerateFake.ps1
. $env:FudgeCI/PrepareAVVM.ps1

Set-StrictMode -Version latest

function Fix-MinGW {
    # TODO: Handle versions other than 8.1.0
    Move-Item C:\mingw-w64\x86_64-8.1.0-posix-seh-rt_v6-rev0\mingw64 C:\MinGW81-x64
}

function Choose-Preinstalled-Products {
    param(
        [array]
        $Packages
    )

    foreach ($pkg in $Packages) {
        try {
            $product = $pkg.AppVeyor
        } catch {
            continue
        }

        $version = $pkg.Version

        $version_parts = ($version.Split('.'))

        if ($product -eq 'jdk') {
            # 8 -> 1.8.0
            $version = "1." + $version_parts[0] + ".0"
        } elseif ($product -eq 'MinGW') {
            Fix-MinGW
        } elseif ($product -eq 'miniconda') {
            # TODO improve translation of real miniconda versions
            # into AppVeyor versions which are the python version
            if ($version -eq '4.5.12') {
                $version = '3.7'
            }

            if ($version[0] -eq '2') {
                Fix-Miniconda27
            }
        }

        # Allow the installed version of python to be over
        if ($product -eq 'python') {
            if ($env:PYTHON_VERSION) {
                $version = $env:PYTHON_VERSION
            }
        }

        Add-Product $product $version $env:PLATFORM
        if (Test-Path "C:\avvm\$product\$version\$env:PLATFORM") {
            Install-Product $product $version $env:PLATFORM
        } elseif (Test-Path "C:\avvm\$product\$version") {
            if ($env:PLATFORM -eq 'x86') {
                $platform = 'x64'
            } else {
                $platform = 'x86'
            }
            Install-Product $product $version $platform
        }
    }
}

function Fix-AppVeyor {
    # Special case, so the generated file isnt in mobans repository assets
    if (Test-Path assets/fudge) {
        $config = Get-FudgefileContent .ci/Fudgefile.appveyor
    } else {
        $config = Get-FudgefileContent $env:FudgeCI/Fudgefile.appveyor
    }

    PackFakeNupkgs $config.packages

    SetDefaultVersions

    Choose-Preinstalled-Products $config.packages
}

Export-ModuleMember -Function Fix-AppVeyor
