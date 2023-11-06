# Utilizamos una imagen base de R oficial de Docker Hub
FROM r-base:4.3.2

# Establecemos el directorio de trabajo en /usr/src/myapp
WORKDIR /app/

COPY . /app/

RUN apt-get update && apt-get install -y libudunits2-dev libssl-dev libgdal-dev libmagick++-dev

# Instalamos los paquetes de R que necesitas
RUN Rscript -e "install.packages('units');     if (!library(units, logical.return=T)) quit(status=10)"
RUN Rscript -e "install.packages('s2');     if (!library(s2, logical.return=T)) quit(status=10)"
RUN Rscript -e "install.packages('sf');     if (!library(sf, logical.return=T)) quit(status=10)"
RUN Rscript -e "install.packages('raster');     if (!library(raster, logical.return=T)) quit(status=10)"
RUN Rscript -e "install.packages('magick');     if (!library(magick, logical.return=T)) quit(status=10)"