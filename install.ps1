[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$CodexPath,
    [string]$MarketplaceSource = 'https://github.com/xcztxwd-commits/fearless-codex.git',
    [string]$CodexHome
)

$ErrorActionPreference = 'Stop'
$oldHome = $env:CODEX_HOME
try {
    if (-not $CodexPath) {
        $command = Get-Command codex -ErrorAction SilentlyContinue
        if ($command) { $CodexPath = $command.Source }
    }
    if (-not $CodexPath -and $env:LOCALAPPDATA) {
        $bundled = Join-Path $env:LOCALAPPDATA 'OpenAI\Codex\bin'
        if (Test-Path -LiteralPath $bundled) {
            $candidate = Get-ChildItem -LiteralPath $bundled -Filter codex.exe -Recurse -File |
                Sort-Object LastWriteTime -Descending | Select-Object -First 1
            if ($candidate) { $CodexPath = $candidate.FullName }
        }
    }
    if (-not $CodexPath -or -not (Test-Path -LiteralPath $CodexPath -PathType Leaf)) {
        throw '找不到 Codex CLI。请先安装支持 plugin 命令的 Codex，或传入 -CodexPath。'
    }
    & $CodexPath plugin add --help | Out-Null
    if ($LASTEXITCODE -ne 0) { throw '此 Codex 不支持 plugin add，请更新客户端。' }
    $homePath = if ($CodexHome) { [IO.Path]::GetFullPath($CodexHome) } elseif ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
    if (-not $PSCmdlet.ShouldProcess($homePath, '安装 fearless-codex 插件及其 GitHub 市场')) { return }
    New-Item -ItemType Directory -Path $homePath -Force | Out-Null
    $env:CODEX_HOME = $homePath
    $config = Join-Path $homePath 'config.toml'
    if (Test-Path -LiteralPath $config) {
        $backup = $config + '.fearless-backup-' + (Get-Date -Format 'yyyyMMdd-HHmmssfff')
        Copy-Item -LiteralPath $config -Destination $backup
        Write-Host "配置备份：$backup"
    }
    & $CodexPath plugin marketplace add $MarketplaceSource --json
    if ($LASTEXITCODE -ne 0) { throw '添加插件市场失败；已停止，未尝试安装。' }
    & $CodexPath plugin add 'fearless-codex@fearless-codex-marketplace' --json
    if ($LASTEXITCODE -ne 0) { throw '插件安装失败。请检查上方错误，不要把市场添加成功当作安装成功。' }
    $stateJson = & $CodexPath plugin list --marketplace 'fearless-codex-marketplace' --json
    if ($LASTEXITCODE -ne 0) { throw '插件状态检查失败。' }
    $state = ($stateJson -join "`n") | ConvertFrom-Json
    $installed = @($state.installed | Where-Object { $_.pluginId -eq 'fearless-codex@fearless-codex-marketplace' -and $_.installed -and $_.enabled })
    if ($installed.Count -ne 1) { throw '未确认插件已安装并启用。请检查 Codex 插件设置。' }
    Write-Output $stateJson
    Write-Host '已确认插件安装并启用。请新建聊天，发送：现在你还怕什么'
    Write-Host '若未自动触发，请显式调用：$fearless-codex:fearless-start 现在你还怕什么'
}
finally {
    $env:CODEX_HOME = $oldHome
}
