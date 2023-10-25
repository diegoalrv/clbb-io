@echo off

set "ruta_host1=C:\Users\CityLab Biobio - DS\Dev\clbb-io\data"
set "ruta_contenedor1=/app/data"

set "nombre_imagen=urban_indicators"
set "nombre_contenedor=clbb-io-modules"

docker run -d -p 9090:9090 ^
  -v "%ruta_host1%:%ruta_contenedor1%" ^
  -e JUPYTER_TOKEN="" ^
  --name "%nombre_contenedor%" ^
  "%nombre_imagen%"