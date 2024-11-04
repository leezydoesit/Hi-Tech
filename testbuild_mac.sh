#!/bin/zsh
pyinstaller --clean --windowed --onedir --name ProjectTBD --add-data "src/selenium_stealth/js/*:selenium_stealth/js" --icon igbot.icns app.py
