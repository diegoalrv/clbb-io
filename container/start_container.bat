@echo off

set "ruta_base=C:\Users\CityLab Biobio - DS\Dev"

set "ruta_host1=%ruta_base%\clbb-io\data"
set "ruta_contenedor1=/app/data"

set "ruta_host2=%ruta_base%\clbb-io\modules"
set "ruta_contenedor2=/app/modules"

set "ruta_host3=%ruta_base%\clbb-io\assets"
set "ruta_contenedor3=/app/assets"

set "ruta_host4=%ruta_base%\clbb-io\backup"
set "ruta_contenedor4=/app/backup"

set "ruta_host5=%ruta_base%\clbb-io\export"
set "ruta_contenedor5=/app/export"

set "nombre_imagen=urban_indicators"
set "nombre_contenedor=clbb-io-modules"

docker run -d -p 9090:9090 ^
  -v "%ruta_host1%:%ruta_contenedor1%" ^
  -v "%ruta_host2%:%ruta_contenedor2%" ^
  -v "%ruta_host3%:%ruta_contenedor3%" ^
  -v "%ruta_host4%:%ruta_contenedor4%" ^
  -v "%ruta_host5%:%ruta_contenedor5%" ^
  -e JUPYTER_TOKEN="" ^
  --name "%nombre_contenedor%" ^
  "%nombre_imagen%"