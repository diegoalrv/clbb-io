# Instala y carga los paquetes necesarios si aún no lo has hecho
install.packages("sf")
install.packages("ggplot2")
install.packages("cowplot")
library(sf)
library(ggplot2)
library(cowplot)

# Ruta a la carpeta que contiene los archivos Shapefile
ruta_carpeta <- "C:/Users/helen/OneDrive/Documentos/Citylab/Base datos SIG antigua/PLANIFICACION_AMC"
salida <- "C:/Users/helen/OneDrive/Documentos/Citylab/Base datos SIG antigua/PLANIFICACION_AMC/mapas/"

# Listar todos los archivos .shp en la carpeta
archivos_shapefiles <- list.files(path = ruta_carpeta, pattern = "\\.shp$", full.names = TRUE)

# Bucle para exportar cada Shapefile a PNG
for (archivo_shapefile in archivos_shapefiles) {
  # Cargar el archivo Shapefile
  shapefile <- sf::st_read(archivo_shapefile)
  
  # Crear el gráfico utilizando ggplot2 (personaliza según tus necesidades)
  map_plot <- ggplot2::ggplot() +
    ggplot2::geom_sf(data = shapefile)
  
  # Generar el nombre del archivo PNG de salida
  nombre_png <- file.path(salida, sub("\\.shp$", ".png", basename(archivo_shapefile)))
  
  # Exportar el mapa como PNG
  ggplot2::ggsave(nombre_png, plot = map_plot, device = "png")
  
  cat(paste("Archivo exportado como:", nombre_png, "\n"))
}

