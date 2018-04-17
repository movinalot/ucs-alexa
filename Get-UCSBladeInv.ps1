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

  [switch] $fromSpark

);

Import-Module -Name Cisco.UCSManager

$credentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $ucsUser,$(convertto-securestring -Force -AsPlainText $ucsPass)

$ucs_connection = Connect-Ucs -Name $ucsHost -Credential $credentials


if ($fromSpark) {

    $ucsBladeInv = Get-ucsblade | Select-Object ucs, ChassisId, SlotId, OperPower, NumOfCpus, TotalMemory, Serial | Format-Table -AutoSize
    #$ucsBladeInv = Get-ucsblade | Select-Object ucs, ChassisId, SlotId, OperPower, NumOfCpus, TotalMemory, Serial 

    write-output $ucsBladeInv

} else {

    $ucsBlades = Get-ucsblade | Select-Object SlotId
    $ucsBladesCount = $ucsBlades.Count
    "There are $ucsBladesCount UCS blades"

}

$ucs_connection = Disconnect-Ucs
