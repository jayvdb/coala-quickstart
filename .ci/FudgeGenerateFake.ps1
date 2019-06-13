Set-StrictMode -Version latest

$template = @'
<?xml version="1.0"?>
<package xmlns="http://schemas.microsoft.com/packaging/2010/07/nuspec.xsd">
  <metadata>
    <id>{name}</id>
    <version>{version}</version>
    <title>{name} {version}</title>
    <authors>AppVeyor</authors>
    <description>Fake generated {name} package to fulfil dependencies.</description>
    <dependencies>
      <dependency id="chocolatey"/>
    </dependencies>
  </metadata>
</package>
'@

function GenerateFakeNuspec {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $name,

        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $version
    )

    $content = $template -replace '{name}', $name
    $content = $content -replace '{version}', $version

    $nuspec = ($env:FudgeCI + '\nuspecs\' + $name + '.nuspec')

    Set-Content $nuspec $content

    Write-Output "Created $nuspec"
}

function GenerateFakeNuspecs {
    param(
        [array]
        $Packages
    )

    foreach ($pkg in $Packages) {
        GenerateFakeNuspec $pkg.Name $pkg.version
    }
}

function PackFakeNupkgs {
    param(
        [array]
        $Packages
    )

    mkdir -Force $env:FudgeCI\nuspecs\ > $null

    GenerateFakeNuspecs $Packages

    # This should work, but is failing
    # fudge pack -FudgefilePath .ci/Fudgefile.appveyor
    foreach ($pkg in $Packages) {
        $filename = ($pkg.Name + '.nuspec')
        choco pack "$env:FudgeCI\nuspecs\$filename" > $null
    }
    mv *.nupkg $env:FudgeCI\nuspecs\

    Write-Output 'Packed!'
}
