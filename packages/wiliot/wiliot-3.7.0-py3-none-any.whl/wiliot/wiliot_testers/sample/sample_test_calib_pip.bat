@echo off
REM cd ..
setlocal enableextensions 
for /f "tokens=*" %%a in ( 
'python -c "import wiliot as _; print(_.__file__)"' 
) do ( 
set pyPath=%%a\..
) 
cd %pyPath%\wiliot_testers\sample
:loop
python SampleTest.py --calib
IF "%ERRORLEVEL%"=="1" goto loop
echo %ERRORLEVEL%
:: pause