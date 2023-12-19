
# Cargar el shapefile de proyectos
data_map <- read_sf("C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/proximidad/input/actual/consolidado/aprovisionamiento.shp")


# Eliminar la dimensión Z
data_map <- st_zm(data_map)

# Restar la porción de la capa utilizando la máscara
data_map <- sf::st_difference(data_map, mascara)

# Eliminar la dimensión Z
data_map <- st_zm(data_map)

# Transforma a la proyección de leaflet si es necesario
data_map <- st_transform(data_map, crs = '+proj=longlat +datum=WGS84')

# Paleta de colores continua
pal <- colorNumeric(palette = "plasma", domain = data_map$tiempo)

# Añade popups a los polígonos
popups <- sprintf("<b>Tiempo:</b>%s ", data_map$tiempo)

mapa_aprovisionamiento <- leaflet(data = data_map) %>%
  addTiles() %>%
  addProviderTiles(providers$CartoDB.Positron)%>%
  setView(lng = -73.06, lat = -36.83, zoom = 14) %>%
  addPolygons(
    fillColor = ~pal(data_map$tiempo),
    stroke = FALSE,
    weight = 1,
    opacity = 0.8,
    color = "white",
    fillOpacity = 1,
    popup = popups
  ) %>%
  addLegend("bottomright", pal = pal, values = ~data_map$tiempo, title = "Tiempo")

mapa_aprovisionamiento


# Guardar el HTML del mapa como un archivo
html_file <- "C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/proximidad/output/html/aprovisionamiento_Actual.html"
htmlwidgets::saveWidget(mapa_aprovisionamiento, html_file, selfcontained = TRUE)














