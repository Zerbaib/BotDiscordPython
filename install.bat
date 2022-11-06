@echo off
cls

echo Bonjour bienvenue dans le programme d'installation des package !
echo.
echo Vous allez installez les packets:
echo - discord
echo - logging
echo - platform
echo - json
echo - os
echo - random
echo - sys
echo.
echo Si un packet est deja installez il ne vas pas etre reinstaller mais juste mie a jours

pause
cls
echo Pour continuer il vous faut python 3.9 minimum (la version recommender est la 3.9.4)
echo Si vous avez pas pip il sera installer si vous l'avez deja il sera mie a jours
pause
cls

py -m ensurepip --upgrade
py get-pip.py
py -m pip install --upgrade pip
cls

pip install discord
cls

pip install logging
cls

pip install platform
cls

pip install json
cls

pip install os
cls

pip install random
cls

pip install sys
cls

echo Fini
pause