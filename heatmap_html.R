install.packages("leaflet.extras")
install.packages("magrittr")

library(leaflet)
library(leaflet.extras)
library(magrittr)
library(sf)
library(RColorBrewer)

# Cargar el shapefile
amenities_sf <- read.csv2("C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/Amenities/bd/actual/amenities_actual.csv")

#paleta <- c('#d7191c', '#fdae61', '#ffffbf', '#a6d96a', '#1a9641')

# Crear el mapa de calor





mapa_densidad <- amenities_sf%>%
  leaflet()%>%
  addTiles()%>%
  addProviderTiles(providers$CartoDB.Positron)%>%
  setView(-73.06, -36.83, 14)%>%
 # htmlwidgets::onRender("
 #   function(el, x) {
#      var map = this;
#      var degree = 25.5; // Cambia el ángulo de rotación según sea necesario
#      map.getContainer().style.transform = 'rotate(' + degree + 'deg)';
 #   }
#  ") %>%
  addHeatmap(lng =~x, lat =~y, max = 100, radius = 30, blur = 10, cellSize = 1 )%>%
  addLegend(position = "bottomright",
          title = "Leyenda",
          values = c(0, 20, 40, 60, 80, 100),
          colors = c("#bfb8ef", "#a2a2f4", "#c2f77f", "#ecf976", "#F78d04", "#F71604"),
          labels = c("10", "20", "40", "60", "80", "100"),  opacity = 0.8)
  
mapa_densidad 
 
# Mostrar el mapa
#mapa_densidad

# Guardar el HTML del mapa como un archivo
html_file <- "C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/Amenities/bd/amenities_actual.html"
htmlwidgets::saveWidget(mapa_densidad, html_file, selfcontained = TRUE)



# Selecciona la paleta "viridis"
#palette_heatmap <- viridis(n = 100, option = "A", begin = 0, end = 1)

# Crea el mapa con el heatmap utilizando la paleta "viridis"
#mapa_densidad <- amenities_sf %>%
 # leaflet() %>%
#  addTiles() %>%
#  addProviderTiles(providers$OpenStreetMap) %>%
#  setView(-73.06, -36.83, 14) %>%
#  addHeatmap(
#    lng = ~x,
#    lat = ~y,
#    max = 100,
#    radius = 20,
#    blur = 10,
#    cellSize = 1,
#    gradient = palette_heatmap
#  )
#mapa_densidad
