@echo off

set "input=%~1"
set "ffmpeg=%~2"

rem echo "%ffmpeg%" -i "%input%" 2^>^&1

rem search "  Duration: HH:MM:SS.mm, start: NNNN.NNNN, bitrate: xxxx kb/s"
for /F "tokens=1,2,3,4,5,6 delims=:., " %%i in ('chcp 1251 ^&^& "%ffmpeg%" -i "%input%" 2^>^&1') do (
    rem echo "%%i"
    if "%%i"=="Duration" call :calcLength %%j %%k %%l %%m
)
goto :EOF

:calcLength
set /A s=%3
set /A s=s+%2*60
set /A s=s+%1*60*60
set /A VIDEO_LENGTH_S = s
set /A VIDEO_LENGTH_MS = s*1000 + %4
rem echo Video duration %1:%2:%3.%4 = %VIDEO_LENGTH_MS%ms = %VIDEO_LENGTH_S%s
rem echo Duration %1:%2:%3.%4
echo %VIDEO_LENGTH_S%
