<#
.SYNOPSIS
Get-UcsFaultCount, get the counts of Critical, Major, Minor and Warning faults from a UCS Manager domain
.DESCRIPTION
Get-UcsFaultCount, get the counts of Critical, Major, Minor and Warning faults from a UCS Manager domain
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

$ucsFaults = Get-UcsFault

$criticalFaults = $($ucsFaults | ?{$_.Severity -match "critical"}).Count
$majorFaults = $($ucsFaults | ?{$_.Severity -match "major"}).Count
$minorFaults = $($ucsFaults | ?{$_.Severity -match "minor"}).Count
$warningFaults = $($ucsFaults | ?{$_.Severity -match "warning"}).Count

"$criticalFaults,$majorFaults,$minorFaults,$warningFaults"

Disconnect-Ucs