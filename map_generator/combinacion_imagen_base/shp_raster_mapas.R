
library(sf)
library(raster)
library(magick)

# Leer los datos
shapefile <- st_read("/app/data/shapefile/indicadores/seguridad/Manzanas_CityScope_Delitos_utm/Manzanas_CityScope_Delitos_utm.shp")
raster_data <- brick("/app/data/raster/base2.tif")
extent(raster_data) <- c(671610.9, 674360.3, 5920185, 5923530)

# nombres_columnas <- names(shapefile)

# # Imprimir los nombres de las columnas uno por uno
# cat("Nombres de las columnas:\n")
# for (nombre_columna in nombres_columnas) {
#   cat(nombre_columna, "\n")
# }

# Tamaño de la hoja en pulgadas
hoja_ancho_pulgadas <- 49.21  # Ancho de la hoja en pulgadas
hoja_alto_pulgadas <- 25.59  # Alto de la hoja en pulgadas

# Calcular el ancho y alto en píxeles basado en la resolución
ancho_pixeles <- hoja_ancho_pulgadas * 600  # 600 DPI
alto_pixeles <- hoja_alto_pulgadas * 600    # 600 DPI


# Abrir un dispositivo de salida PNG
png("/app/data/output/mi_plot.png",
    width = ancho_pixeles, height = alto_pixeles, units = "px", 
    res = 600, pointsize = 50)  # Ajusta el punto por pulgada (pointsize) según tus necesidades

# Crear el plot
plotRGB(raster_data)
# colores <- colorRampPalette(c("yellow", "orange", "red"))(10)  # Ejemplo de paleta de colores personalizada
colores <- colorRampPalette(c("lightblue", "blue", "darkblue"))(10)

# Crear un gráfico personalizado
plot(shapefile["TOTAL_PERS"], col = colores, add = TRUE)

# Agregar una leyenda con la barra de colores
legend("topright", legend = seq(min(shapefile$TOTAL_PERS), max(shapefile$TOTAL_PERS), length.out = 10), fill = colores)
print("Antes de cerrar")
# Cerrar el dispositivo de salida PNG
dev.off()

# Cargar la imagen PNG
imagen <- image_read("/app/data/output/mi_plot.png")
print("Imagen leida")

# Rotar la imagen en sentido horario 
imagen_rotada <- image_rotate(imagen, 295.3)
print("imagen rotada")

# # Guardar la imagen rotada
# gc()
# rm()
# image_write(imagen_rotada, "/app/data/output/mi_plot_rotada_.jpg")
# print("Imagen rotada guardada")
# # Cargar la imagen PNG
# imagen <- image_read("/app/data/output/mi_plot_rotada_.png")

# Coordenadas del área a recortar (izquierda, arriba, ancho, alto)
x <- 8090  # Coordenada izquierda
y <- 3850  # Coordenada superior
ancho <- 13150  # Ancho del área a recortar
alto <- 7600  # Alto del área a recortar

# Recortar la imagen
imagen_recortada <- image_crop(imagen_rotada, geometry = paste(ancho, "x", alto, "+", x, "+", y))
print("Imagen recortada")
# Escalar la imagen
#imagen_escala <- image_scale(imagen_recortada, paste(13300, "x", 7550))

# Aplicar el efecto espejo horizontal
imagen_espejo <- image_flop(imagen_recortada)
print("espejo")

# Guardar la imagen recortada
image_write(imagen_espejo, "/app/data/output/mi_plot_rotada_.png")


gc()