library(ggplot2)
library(magick)

library(sf)
library(ggplot2)
library(magrittr)
library(viridis)
library(magick)

# Rutas de entrada y salida
ruta_entrada <- "C:/Users/helen/OneDrive/Documentos/Citylab/Resultados_indicadores/export/resultado_poblacion/"
ruta_salida <- "C:/Users/helen/OneDrive/Documentos/Citylab/Resultados_indicadores/export/resultado_poblacion/"
calles_pp <- st_read("C:/Users/helen/OneDrive/Documentos/Citylab/Resultados_indicadores/shapes/lineas_pp.shp")
linea_tren <- st_read("C:/Users/helen/OneDrive/Documentos/Citylab/Resultados_indicadores/shapes/linea_tren.shp")


# Lee la lista de archivos en la carpeta de entrada
lista_archivos <- list.files(path = ruta_entrada, pattern = "\\.shp$", full.names = TRUE)

# Itera sobre cada archivo en la lista
for (archivo_actual in lista_archivos) {
  actual_PK <- st_read(archivo_actual) 
  
  # Define una paleta de colores de verde a rojo
  colores <- c("#f1bf7e","#f7b538","#db7c26","#d8572a", "#ce4329", "#c32f27", "#780116")
  # Crear una interpolación lineal de colores
  colores_interpolados <- colorRamp(colores)
  
  # Obtener la paleta de colores con n colores
  colores_final <- colores_interpolados(1000)
  
  
  
  
  # Visualización en ggplot
  mi_grafico <- ggplot() +
    geom_sf(data = actual_PK, aes(fill = population), color = "white") +
    geom_sf(data = calles_pp, color = "white", lwd = 1.5) +  # Ajusta el valor de lwd según tu preferencia
    geom_sf(data = linea_tren, aes(alpha = 0.6), color = "darkgray", lwd = 1.5) +
    scale_fill_gradientn(colours = colores, limits = c(min(actual_PK$population), max(actual_PK$population)),
                         name = "Tiempo") +
    # Añade otras capas según sea necesario
    theme_minimal() +
    theme(axis.text = element_blank(), 
          axis.title = element_blank(),
          panel.grid = element_blank(),
          axis.ticks = element_blank(),
          panel.border = element_blank(),
          plot.title = element_text(hjust = 0.5, size = 16),
          plot.margin = margin(1, 1, 1, 1, "cm"))
  
  # Especifica la ruta completa y el nombre del archivo de salida
  nombre_archivo <- tools::file_path_sans_ext(basename(archivo_actual))
  ruta_archivo <- file.path(ruta_salida, "mapas", paste0(nombre_archivo, ".png"))
  
  ancho_pulgadas <- 25.19685  # 64 cm en pulgadas
  largo_pulgadas <- 63.38583  # 161 cm en pulgadas
  
  # Guarda el gráfico en un archivo PNG
  ggsave(filename = ruta_archivo, plot = mi_grafico, width = ancho_pulgadas, height = largo_pulgadas, units = "in", limitsize = FALSE)
  
  # Carga la imagen
  imagen <- image_read(ruta_archivo)
  
  # Rota la imagen en 27.4 grados en sentido horario
  imagen_rotada <- image_rotate(imagen, 27.4)
  
  # Guarda la imagen rotada
  ruta_archivo <- file.path(ruta_salida, paste0(nombre_archivo, ".png"))
  image_write(imagen_rotada, path = ruta_archivo)
  
  # Especifica las coordenadas de recorte (ajústalas según tus necesidades)
  x_start <- 1800
  y_start <- 5200
  width <- 4050
  height <- 8550
  
  # Recorta la imagen rotada
  imagen_recortada <- image_crop(imagen_rotada, geometry = sprintf("%dx%d+%d+%d", width, height, x_start, y_start))
  
  # Guarda la imagen recortada
  ruta_carpeta_finales <- file.path(ruta_salida, "mapas", "finales")
  if (!file.exists(ruta_carpeta_finales)) {
    dir.create(ruta_carpeta_finales, recursive = TRUE)
  }
  
  ruta_archivo_recortado <- file.path(ruta_carpeta_finales, paste0(nombre_archivo, ".png"))
  image_write(imagen_recortada, path = ruta_archivo_recortado)
  rm(actual_PK)
  gc()
}

