@echo off

rem Check if nbconvert is installed
jupyter nbconvert --version >nul 2>nul && (
    echo nbconvert is installed.
    echo Cleaning all notebooks...
    jupyter nbconvert --ClearOutputPreprocessor.enabled=True --clear-output *.ipynb && (
        echo Cleaned all notebooks successfully.
        exit /b 0
    ) || (
        echo Failed to clean notebooks. Please try to install nbconvert manually.
    )
) || (
    echo nbconvert is not installed. Do you want to install it? (Y/N)
    set /p "install=Do you want to install nbconvert? (Y/N): "
    if /i "%install%"=="Y" (
        pip install nbconvert
        rem Check if nbconvert is installed
        jupyter nbconvert --ClearOutputPreprocessor.enabled=True --clear-output *.ipynb && (
            echo Cleaned all notebooks successfully.
        ) || (
            echo Failed to clean notebooks. Please try to install nbconvert manually.
        )
    ) else (
        echo Please install nbconvert manually.
    )
)

pause
