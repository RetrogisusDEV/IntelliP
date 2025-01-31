@echo off

cd src

REM Check if the converter file exists
if not exist "ipcetocpp.exe" (
    echo Error: The converter ipce to cpp does not exist.
    pause
    exit /b
)

start ipcetocpp.exe

REM Check if the output.cpp file exists
if not exist "cpp_output\output.cpp" (
    echo Error: The file output.cpp does not exist.
    pause
    exit /b
)

REM Compile the output.cpp file
g++ -O1 -std=c++11 -static cpp_output\output.cpp -o ..\project.exe

REM Check if the compilation was successful
if errorlevel 1 (
    echo Compilation failed.
) else (
    echo Compilation succeeded. Executable created in the bin directory.
    start ..\project.exe
)

pause
