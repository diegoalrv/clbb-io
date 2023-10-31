library(sf)
library(raster)
library(magick)


# Leer los datos
shapefile <- st_read("C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/Seguridad/Manzanas_CityScope_Delitos_utm.shp")
raster_data <- brick("C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/base2.tif")
extent(raster_data) <- c(671610.9, 674360.3, 5920185, 5923530)

# Tamaño de la hoja en pulgadas
hoja_ancho_pulgadas <- 49.21  # Ancho de la hoja en pulgadas
hoja_alto_pulgadas <- 25.59  # Alto de la hoja en pulgadas

# Calcular el ancho y alto en píxeles basado en la resolución
ancho_pixeles <- hoja_ancho_pulgadas * 600  # 600 DPI
alto_pixeles <- hoja_alto_pulgadas * 600    # 600 DPI


# Abrir un dispositivo de salida PNG
png("C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/mi_plot.png",
    width = ancho_pixeles, height = alto_pixeles, units = "px", 
    res = 600, pointsize = 50)  # Ajusta el punto por pulgada (pointsize) según tus necesidades

# Crear el plot
plotRGB(raster_data)
plot(shapefile, add = TRUE)

# Cerrar el dispositivo de salida PNG
dev.off()


# Cargar la imagen PNG
imagen <- image_read("C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/mi_plot.png")


# Rotar la imagen en sentido horario 
imagen_rotada <- image_rotate(imagen, 295.3)

# Guardar la imagen rotada


image_write(imagen_rotada, "C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/mi_plot_rotada_.png", density = "300x300")

# Cargar la imagen PNG
imagen <- image_read("C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/mi_plot_rotada_.png")

# Coordenadas del área a recortar (izquierda, arriba, ancho, alto)
x <- 8090  # Coordenada izquierda
y <- 3850  # Coordenada superior
ancho <- 13150  # Ancho del área a recortar
alto <- 7600  # Alto del área a recortar

# Recortar la imagen
imagen_recortada <- image_crop(imagen, geometry = paste(ancho, "x", alto, "+", x, "+", y))

# Escalar la imagen
#imagen_escala <- image_scale(imagen_recortada, paste(13300, "x", 7550))

# Aplicar el efecto espejo horizontal
imagen_espejo <- image_flop(imagen_recortada)


# Guardar la imagen recortada
image_write(imagen_espejo, "C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/mi_plot_rotada.png")


gc()
