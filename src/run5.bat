@echo off

REM Navigate to the desired directory
cd C:\Users\NamVu\source\repos\Year4\Semeter2\Distributed-System_SES\Distributed-System_SES-Algorithms

REM Activate the virtual environment
call venv\Scripts\activate

cd src

REM Run the main_client.py script with port numbers from 7670 to 7674
for /L %%i in (7670, 1, 7674) do (
    start cmd /k "python main_client.py %%i"
)

REM Keep the script window open to view output
pause
