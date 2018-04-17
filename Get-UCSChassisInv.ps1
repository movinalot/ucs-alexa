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
    [string] $ucsPass,

  [Parameter(Mandatory=$true,HelpMessage="Enter Chassis Id")] 
    [string] $chassisId,

  [Parameter(Mandatory=$true,HelpMessage="Enter Slot Id")] 
    [string] $slotId,
    
  [switch] $fromSpark

);

Import-Module -Name Cisco.UCSManager

$credentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $ucsUser,$(convertto-securestring -Force -AsPlainText $ucsPass)

$ucs_connection = Connect-Ucs -Name $ucsHost -Credential $credentials

$ucsChassisSlot = $a | ? {$_.chassisid -eq $chassisId -and $_.slotid -eq $slotId}


if ($fromSpark) {
    
    $ucsChassisSlot

} else {

    if ($ucsChassisSlot.Association -eq "none" -and $ucsChassisSlot.Availability -eq "available" -and $ucsChassisSlot.AdminState -eq "in-service") {
        "Usable"
    } else {
        "Not usable"
    }

}

$ucs_connection = Disconnect-Ucs
