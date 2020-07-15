If (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{   
$arguments = "& '" + $myinvocation.mycommand.definition + "'"
Start-Process "$psHome\powershell.exe" -Verb runAs -ArgumentList $arguments

break
}

Push-Location (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)
$CertPath = ".\Certs"
$CertFilenamePrivate = "Private.pfx"
$CertFilenamePublic = "Public.cer"
$CertPassword = "PrivatePasswort!"
$CertSubject = "ScpVBus Self Signing"

$DriverPath = ".\ScpVBus-x64"
$DriverOSTarget = "10_X64"
$DriverCatFile = "scpvbus.cat"
$DriverInfFile = "ScpVBus.inf"
$DriverHWID = "Root\ScpVBus"


function CreateSelfSignCert([String] $Subject, [String] $Password, [String] $SavePath, [String] $FileNamePrivate, [String] $FileNamePublic){
    New-Item -ItemType "directory" -Path $SavePath -Force | Out-Null

    
    $cert = New-SelfSignedCertificate -Subject $Subject -Type CodeSigningCert -CertStoreLocation cert:\LocalMachine\My -NotAfter (Get-Date).AddYears(10)

    $CertPassword = ConvertTo-SecureString -String $Password -Force –AsPlainText

    Export-PfxCertificate -Cert $cert -FilePath "$SavePath\$FileNamePrivate" -Password $CertPassword | Out-Null
    Export-Certificate -Cert $cert -FilePath "$SavePath\$FileNamePublic" | Out-Null
    
}

function ImportTrustedCert([String] $PublicCertFile){
    Import-Certificate -FilePath $PublicCertFile -CertStoreLocation cert:\LocalMachine\Root
    Import-Certificate -FilePath $PublicCertFile -CertStoreLocation cert:\LocalMachine\TrustedPublisher


}


function ReadHostDefault([String] $PromptText, [String] $DefaultValue){
    
    $input = Read-Host -Prompt "$PromptText [Default: $DefaultValue]"
    if([String]::IsNullOrWhiteSpace($input)){
        $input = $DefaultValue

    }
    return $input
}


function CreateCatFile([String] $DriverPath, [String] $OSTarget){
    Start-Process .\Inf2Cat\Inf2Cat.exe -NoNewWindow -Wait -ArgumentList "/driver:$DriverPath","/os:$OSTarget"
}


function SignDriver([String] $CertPrivate, [String] $CertPassword, [String] $DriverCatPath){
    Start-Process .\SignTool\signtool.exe -NoNewWindow -Wait -ArgumentList "sign","/f $CertPrivate","/p $CertPassword","/t http://timestamp.verisign.com/scripts/timstamp.dll","$DriverCatPath"
}


function InstallDriver([String] $InfFile, [String] $HWID){

    $output = & .\Devcon\devcon.exe install $InfFile $HWID

    return $output
}


Write-Host "Creating Self Sign Certificate..."
CreateSelfSignCert -Subject $CertSubject -Password $CertPassword -SavePath $CertPath -FileNamePrivate $CertFilenamePrivate -FileNamePublic $CertFilenamePublic
Write-Host "Import Certificate to Root and TrustedPublisher Store"
ImportTrustedCert -PublicCertFile "$CertPath\$CertFilenamePublic"
Write-Host "Creating Driver Catalog File"
CreateCatFile -DriverPath $DriverPath -OSTarget $DriverOSTarget
Write-Host "Sign Driver Driver"
SignDriver -CertPrivate "$CertPath\$CertFilenamePrivate" -CertPassword "$CertPassword" -DriverCatPath "$DriverPath\$DriverCatFile"
Write-Host "Install Driver"
InstallDriver -InfFile "$DriverPath\$DriverInfFile" -HWID $DriverHWID
Read-Host -Prompt "Press Enter to Exit"