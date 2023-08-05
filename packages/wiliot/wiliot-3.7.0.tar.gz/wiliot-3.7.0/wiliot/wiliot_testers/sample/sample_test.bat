@echo off
REM cd ..
:loop
cd C:\Users\%USERNAME%\eclipse-workspace\pywiliot_internal\wiliot\wiliot_testers\sample
python SampleTest.py
IF "%ERRORLEVEL%"=="1" goto loop
echo %ERRORLEVEL%
:: pause