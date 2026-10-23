@echo off
cd /d "%~dp0"
if not exist bin mkdir bin
set "COMPILADOR=%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
if not exist "%COMPILADOR%" set "COMPILADOR=%WINDIR%\Microsoft.NET\Framework\v4.0.30319\csc.exe"
if not exist "%COMPILADOR%" (
  echo Se requiere .NET Framework 4.7.2 o posterior en Windows.
  pause
  exit /b 1
)
"%COMPILADOR%" /nologo /out:bin\BoticaInkaSalud.exe Program.cs
if errorlevel 1 (
  pause
  exit /b 1
)
bin\BoticaInkaSalud.exe
pause
