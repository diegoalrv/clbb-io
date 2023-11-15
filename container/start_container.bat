@echo off

set "ruta_base=C:\Users\dalex\Documents"

set "ruta_host1=%ruta_base%\clbb-io\data"
set "ruta_contenedor1=/app/data"

set "ruta_host2=%ruta_base%\clbb-io\modules"
set "ruta_contenedor2=/app/modules"

set "ruta_host3=%ruta_base%\clbb-io\assets"
set "ruta_contenedor3=/app/assets"

set "nombre_imagen=ui_clbb"
set "nombre_contenedor=clbb-io-modules"

docker run -d -p 9090:9090 ^
  -v "%ruta_host1%:%ruta_contenedor1%" ^
  -v "%ruta_host2%:%ruta_contenedor2%" ^
  -v "%ruta_host3%:%ruta_contenedor3%" ^
  -e JUPYTER_TOKEN="" ^
  --name "%nombre_contenedor%" ^
  "%nombre_imagen%"