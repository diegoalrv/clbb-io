# Instala y carga los paquetes necesarios si aún no lo has hecho
install.packages("sf")
install.packages("ggplot2")
install.packages("cowplot")
install.packages("viridisLite")
library(sf)
library(ggplot2)
library(cowplot)
library(magick)
library(viridisLite)


# Ruta a la carpeta que contiene los archivos Shapefile
ruta_carpeta <- "C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/proximidad/input/actual/consolidado/"
salida <- "C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/proximidad/output/"
mascara_shapefile <- "C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/proximidad/area_rio_quitar2.shp"


# Listar todos los archivos .shp en la carpeta
archivos_shapefiles <- list.files(path = ruta_carpeta, pattern = "\\.shp$", full.names = TRUE)

# Cargar la máscara que debe ser un polígono disuelto
mascara <- sf::st_read(mascara_shapefile)

# Bucle para exportar cada Shapefile a PNG
for (archivo_shapefile in archivos_shapefiles) {
  # Cargar el archivo Shapefile
  shapefile <- sf::st_read(archivo_shapefile)
  
  # Restar la porción de la capa utilizando la máscara
  shapefile <- sf::st_difference(shapefile, mascara)
  
  # Crear el gráfico utilizando ggplot2 y cambiar el color según travel_tim
  map_plot <- ggplot2::ggplot() +
    ggplot2::geom_sf(data = shapefile, aes(fill = travel_tim)) +
    viridis::scale_fill_viridis(name = NULL, option = "turbo", limits = c(0, max(shapefile$travel_tim)), trans = "log1p") +
    #option cambia la paleta de colores
    
    theme_void()+  # Eliminar fondo y ejes
    guides(fill = FALSE) #elimina la barra de color de leyenda
  
  # Generar el nombre del archivo PNG de salida
  nombre_png <- file.path(salida, sub("\\.shp$", ".png", basename(archivo_shapefile)))
 
  # Definir los límites de los rangos (ajustar según tus necesidades)
  limites_rangos <- c(0, 5, 10, 15, 100)
  
  # Cambiar la escala de colores por rangos utilizando la misma paleta
  map_plot_rangos <- ggplot2::ggplot() +
    ggplot2::geom_sf(data = shapefile, aes(fill = cut(travel_tim, breaks = limites_rangos))) +
    viridis::scale_fill_viridis(name = NULL, option = "plasma", limits = c(0, max(shapefile$travel_tim)), trans = "log1p") +
    theme_void() +  # Eliminar fondo y ejes
    guides(fill = FALSE)  # Eliminar la guía de colores
  
  
    # Exportar el mapa como PNG
  ggplot2::ggsave(nombre_png, plot = map_plot, device = "png")
 
  # Rotar el archivo PNG utilizando la función image_rotate de magick
  imagen <- image_read(nombre_png)
  imagen_rotada <- image_rotate(imagen, 295.3)
  
  # Guardar la imagen rotada
  nombre_png_rotado <- sub(".png", "_rotado.png", nombre_png)
  image_write(imagen_rotada, path = nombre_png_rotado)
  

  
  cat(paste("Archivo exportado como:", nombre_png, "\n"))
}






