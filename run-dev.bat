@echo on

IF NOT EXIST ".venv-3.13" (
    ECHO "venv not exist, creating new one..."
    pyhton -m venv .venv-3.13
)

ECHO Activate venv
call .venv-3.13\Scripts\activate.bat

ECHO checking pip list
call python -m pip list

REM check requirements file
ECHO checking requirements file
IF EXIST "requirements.txt" (
    echo requirements file found, installing new dependecies
    call python -m pip install -r requirements.txt

) ELSE echo requirements file not found, skip installing from file;

REM Default IP
set IP=127.0.0.1

REM Setted PORT, change if needed
set PORT=8800
echo ======================================

if not "%~1"=="" set "IP=%~1"
echo start server on %IP%:%PORT%

watchmedo auto-restart --directory=./ --pattern="*.py;*.html" --recursive -- uvicorn manajement_keluhan.asgi:application --host %IP% --port %PORT%
