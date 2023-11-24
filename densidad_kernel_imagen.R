#install.packages("tmap")
#install.packages("sf")
library(sp)
library(sf)
library(tmap)
#library(sp)
library(ggplot2)
library(tiff)

library(png)
library(gridExtra)
#install.packages("grid")
#install.packages("gridGraphics")
#install.packages("ks")
library(grid)
library(gridGraphics)
library(ks)
library(cowplot)

# Carga la imagen base

amenities <- read.csv2("C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/Amenities/actuales/amenities_costanera_utm.csv")

amenities <- amenities[!is.na(amenities$POINT_X)&!is.na(amenities$POINT_Y),]
coordinates(amenities) <- ~POINT_X + POINT_Y
amenities <- st_as_sf(amenities)
st_crs(amenities)= 32718
coord_den <- st_coordinates(amenities)

# Ruta a la imagen PNG de fondo
#ruta_imagen <- "C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/imagen_liviana.png"

# Coordenadas para posicionar la imagen de fondo
#MIN_X <- 36.820
#MAX_X <- 36.845
#MIN_Y <- 73.050
#MAX_Y <- 73.070


# Ruta a la imagen de fondo
img.file <- "C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/imagen_liviana.png"

# Cargar la imagen desde la ruta absoluta
img <- png::readPNG(img.file)

# Crear el gráfico de densidad de núcleo
gg <- ggplot() +
  geom_sf(data = amenities, size = 0.001, alpha = 0.2) +
  stat_density2d(aes(x = coord_den[, 1], y = coord_den[, 2],
                     fill = ..level.., alpha = ..level..),
                 geom = "polygon") +
  scale_fill_gradient(low = "yellow", high = "green")

# Superponer la imagen de fondo en el gráfico utilizando cowplot

gg_with_background <- ggplot() +
  annotation_custom(
    grob = rasterGrob(img, width = 1.2, height = 1, interpolate = TRUE),
    xmin = -Inf, xmax = Inf, ymin = -Inf, ymax = Inf
  ) +
  geom_sf(data = amenities, size = 1, alpha = 1) +
  stat_density2d(aes(x = coord_den[, 1], y = coord_den[, 2],
                     fill = ..level.., alpha = ..level..),
                 geom = "polygon") +
  scale_fill_gradient(low = "orange", high = "green")+

  guides(fill = "none", alpha = "none") +  # Quitar la leyenda de fill
  theme(axis.text.x = element_blank(),
        axis.text.y = element_blank(),
        axis.title.x = element_blank(),
        axis.title.y = element_blank())



# Mostrar el gráfico completo
print(gg_with_background)

















