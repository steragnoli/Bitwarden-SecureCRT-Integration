$session=Get-Content -Path $env:LOCALAPPDATA\bitwarden-cli\session.txt

if ( $session -eq $null -or $session -eq '') # if session is empty start login and write new session key

    {
        [String]$response= bw.exe login --raw
        $env:BW_SESSION=$response
        [System.Environment]::SetEnvironmentVariable('BW_SESSION', $response,[System.EnvironmentVariableTarget]::User)
        Set-Content -Path $env:LOCALAPPDATA\bitwarden-cli\session.txt -Value $response -Force
        bw sync --session $session
    
    }

elseif($session -ne $null -or $session -ne '') # if the session key exist try to test the login and sync Vault

    {
        $response2=bw.exe get username TEST-LOGIN-DO-NOT-DELETE --raw --session $session --nointeraction

        if($response2 -match 'TEST')
            {
                Write-Host "LOGIN OK"
                bw sync --session $session
                [System.Environment]::SetEnvironmentVariable('BW_SESSION', $session,[System.EnvironmentVariableTarget]::User)
            }
        else #if the TEST Login fails, force logout and start new login
            {
            write-host $response2
            bw.exe logout
            write-host ''
            [String]$response= bw.exe login --raw
            $env:BW_SESSION=$response
            [System.Environment]::SetEnvironmentVariable('BW_SESSION', $response,[System.EnvironmentVariableTarget]::User)
            Set-Content -Path $env:LOCALAPPDATA\bitwarden-cli\session.txt -Value $response -Force
            $session=$response
            bw sync --session $session
            }             
    }
