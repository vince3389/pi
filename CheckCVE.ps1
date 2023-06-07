$CVEFile = Join-Path -Path $PSScriptRoot -ChildPath "cve_list.txt"  # Path to the CVE text file in the same folder as the script

if (Test-Path $CVEFile) {
    $CVEList = Get-Content $CVEFile
    foreach ($cve in $CVEList) {
        # Rest of the script remains the same
        $nvdApiUrl = "https://services.nvd.nist.gov/rest/json/cve/1.0/$cve"
        $nvdResponse = Invoke-RestMethod -Uri $nvdApiUrl -Method Get

        $exploitDbUrl = "https://www.exploit-db.com/search?cve=$cve"
        $exploitDbResponse = Invoke-WebRequest -Uri $exploitDbUrl -Method Get

        $cveExists = $nvdResponse.result.CVE_Items.Count -gt 0
        $exploitDbExists = $exploitDbResponse.Content -like "*No results found for*"

        if ($cveExists) {
            $cveData = $nvdResponse.result.CVE_Items[0].cve
            $cvss = $cveData.baseMetricV3.cvssV3.baseScore
            Write-Host "CVE $cve found in the NVD database with a CVSS score of $cvss"
        } elseif ($exploitDbExists) {
            Write-Host "CVE $cve found in Exploit-DB but not in the NVD database"
        } else {
            Write-Host "CVE $cve not found in any of the data sources"
        }
    }
} else {
    Write-Host "CVE file not found in the script folder."
}
