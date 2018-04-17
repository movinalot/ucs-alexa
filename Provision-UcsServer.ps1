<#
.SYNOPSIS
Provision-UcsServer, Associate UCS Server with Service Profile
.DESCRIPTION
Provision-UcsServer, Associate UCS Server with Service Profile
.NOTES
John McDonough, Cisco Systems, Inc. (jomcdono)
#>

param( [Parameter(Mandatory=$true,HelpMessage="Enter UCS Manager IP")]
    [string] $ucsHost,

  [Parameter(Mandatory=$true,HelpMessage="Enter UCS Manager user")]
    [string] $ucsUser,

  [Parameter(Mandatory=$true,HelpMessage="Enter UCS Manager user's Password")]
    [string] $ucsPass
);

Import-Module -Name Cisco.UCSManager

$credentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $ucsUser,$(convertto-securestring -Force -AsPlainText $ucsPass)

$ucs_connection = Connect-Ucs -Name $ucsHost -Credential $credentials

Get-UcsServiceProfile -Ucs $ucs_connection -Name Win2012 | Associate-UcsServiceProfile -Ucs $ucs_connection -Blade (Get-UcsBlade -Ucs $ucs_connection -Chassis 2 -SlotId 4) -Force

$ucs_connection = Disconnect-Ucs