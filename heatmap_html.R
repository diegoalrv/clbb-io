install.packages("leaflet.extras")
install.packages("magrittr")

library(leaflet)
library(leaflet.extras)
library(magrittr)
library(sf)

# Cargar el shapefile
amenities_sf <- read.csv2("C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/Amenities/actuales/amenities_costanera.csv")

paleta <- c('#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641')

# Crear el mapa de calor


mapa_densidad <- amenities_sf%>%
  leaflet()%>%
  addTiles()%>%
  addProviderTiles(providers$OpenStreetMap)%>%
  setView(-73.06, -36.83, 14)%>%
  addHeatmap(lng =~x, lat =~y, max = 100, radius = 20, blur = 10, cellSize = 1 )%>%
  
  
 
# Mostrar el mapa
mapa_densidad

# Guardar el HTML del mapa como un archivo
html_file <- "C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/Amenities/actuales/amenities_actuales.html"
htmlwidgets::saveWidget(mapa_densidad, html_file, selfcontained = TRUE)


