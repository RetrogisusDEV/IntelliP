# Compiling Guide for Intelli-P

## Overview
This guide provides step-by-step instructions on how to compile the `index.py` script, convert it to an executable, and run the `compile.bat` file.

## Steps to Compile and Execute

### 1. Compile the Python Script
To compile the `index.py` script into an executable:
- Open a command prompt or terminal.
- Navigate to the project directory where `index.py` is located.
- Run the following command:
  ```bash
  python src/index.py
  ```

### 2. Convert to Executable
After running the script, the generated C code will be saved in the `c_output` directory as `output.c`. To convert this C code into an executable:
- Use a C compiler (e.g., GCC) to compile the code:
  ```bash
  gcc c_output/output.c -o output.exe
  ```

### 3. Run the Compile Script
To automate the compilation process, you can run the `compile.bat` file:
- Double-click `compile.bat` or run it from the command line:
  ```bash
  compile.bat
  ```

## Conclusion
Following these steps will allow you to compile the `index.py` script, generate the corresponding C code, and create an executable file for your project.
