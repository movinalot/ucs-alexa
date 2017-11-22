<#
.SYNOPSIS
Set-ImcLed, set the LED state on a UCS Rack Server
.DESCRIPTION
Set-ImcLed, set the LED state on a UCS Rack Server
.NOTES
John McDonough, Cisco Systems, Inc. (jomcdono)
#>

param( [Parameter(Mandatory=$true,HelpMessage="Enter Server IP")]
    [string] $Server,

  [Parameter(Mandatory=$true,HelpMessage="Enter Server user")]
    [string] $User,

  [Parameter(Mandatory=$true,HelpMessage="Enter Server user's Password")]
    [string] $Pass,

  [Parameter(Mandatory=$true,HelpMessage="Enter Server LED state")]
    [string] $LedState
);

Import-Module -Name Cisco.IMC

$credentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $User,$(convertto-securestring -Force -AsPlainText $Pass)

$imc_connection = Connect-Imc -Name $Server -Credential $credentials

$(Get-ImcLocatorLed | Set-ImcLocatorLed -AdminState $LedState -Force).OperState

$imc_connection = Disconnect-Imc