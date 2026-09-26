@echo off
setlocal
set "result=1"
set "CODEX_EXE="
for /f "delims=" %%C in ('where codex.exe 2^>nul') do if not defined CODEX_EXE set "CODEX_EXE=%%C"
for /f "delims=" %%C in ('where codex.cmd 2^>nul') do if not defined CODEX_EXE set "CODEX_EXE=%%C"
if not defined CODEX_EXE for /f "delims=" %%D in ('dir /b /ad /o-d "%LOCALAPPDATA%\OpenAI\Codex\bin" 2^>nul') do if not defined CODEX_EXE if exist "%LOCALAPPDATA%\OpenAI\Codex\bin\%%D\codex.exe" set "CODEX_EXE=%LOCALAPPDATA%\OpenAI\Codex\bin\%%D\codex.exe"
if not defined CODEX_EXE (
  echo Codex CLI not found. Install or update Codex first.
  goto done
)
call "%CODEX_EXE%" plugin add --help >nul
if errorlevel 1 goto failed
if not defined CODEX_HOME set "CODEX_HOME=%USERPROFILE%\.codex"
if not exist "%CODEX_HOME%" mkdir "%CODEX_HOME%"
if errorlevel 1 goto failed
if not exist "%CODEX_HOME%\config.toml" goto install
:backup
set "BACKUP=%CODEX_HOME%\config.toml.fearless-backup-%RANDOM%-%RANDOM%"
if exist "%BACKUP%" goto backup
copy /b "%CODEX_HOME%\config.toml" "%BACKUP%" >nul
if errorlevel 1 goto failed
echo Config backup: "%BACKUP%"
:install
call "%CODEX_EXE%" plugin marketplace add https://github.com/xcztxwd-commits/fearless-codex.git --json
if errorlevel 1 goto failed
call "%CODEX_EXE%" plugin add fearless-codex@fearless-codex-marketplace --json
if errorlevel 1 goto failed
call "%CODEX_EXE%" plugin list --marketplace fearless-codex-marketplace --json
if errorlevel 1 goto failed
echo Installation commands completed. Check installed/enabled above, then open a new Codex chat.
echo Explicit skill: $fearless-codex:fearless-start
set "result=0"
goto done
:failed
echo Installation failed. Read the error above. No success is assumed.
:done
if /i not "%~1"=="--no-pause" pause
exit /b %result%
