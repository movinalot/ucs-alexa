<#
.SYNOPSIS
Get-ImcSerial, Get the serial number from a Cisco UCS Rack Server
.DESCRIPTION
Get-ImcSerial, Get the serial number from a Cisco UCS Rack Server
.NOTES
John McDonough, Cisco Systems, Inc. (jomcdono)
#>

param( [Parameter(Mandatory=$true,HelpMessage="Enter Server IP")]
    [string] $Server,

  [Parameter(Mandatory=$true,HelpMessage="Enter Server user")]
    [string] $User,

  [Parameter(Mandatory=$true,HelpMessage="Enter Server user's Password")]
    [string] $Pass
);

Import-Module -Name Cisco.IMC

$credentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $User,$(convertto-securestring -Force -AsPlainText $Pass)

$imc_connection = Connect-Imc -Name $Server -Credential $credentials

$serialno = $(Get-ImcRackUnit).Serial

for($x = 0; $x -lt $serialno.length; $x++) {
    $newserialno += $serialno[$x] + ", "
}
$newserialno

Disconnect-Imc