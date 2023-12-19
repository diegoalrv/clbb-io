library(sf)
library(leaflet)
library(htmlwidgets)
library(viridis)


# Carpeta que contiene los shapefiles
carpeta_shapefiles <- "C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/Áreas verdes/Output/6_version/consolidado/"

# Lista de archivos shapefile en la carpeta
shapefiles <- list.files(path = carpeta_shapefiles, pattern = "\\.shp$", full.names = TRUE)

# Función para procesar un shapefile y crear un mapa
generar_mapa <- function(shp_file) {
  # Cargar el shapefile
  data_map <- read_sf(shp_file)
  
  # Eliminar la dimensión Z
  data_map <- st_zm(data_map)
  
  # Transforma a la proyección de leaflet si es necesario
  data_map <- st_transform(data_map, crs = '+proj=longlat +datum=WGS84')
  
  # Paleta de colores continua (turbo)
  pal <- colorNumeric(palette = viridis(100, option = "turbo"), domain = data_map$travel_tim, na.color = "transparent")
  
  # Añade popups a los polígonos
  popups <- sprintf("<b>Tiempo:</b> %s", data_map$travel_tim)
  
  # Crear el objeto de mapa
  mapa_aprovisionamiento <- leaflet(data = data_map) %>%
    addTiles() %>%
    addProviderTiles(providers$CartoDB.Positron) %>%
    setView(lng = -73.06, lat = -36.83, zoom = 14) %>%
    addPolygons(
      fillColor = ~pal(data_map$travel_tim),
      stroke = FALSE,
      weight = 1,
      opacity = 0.8,
      color = "white",
      fillOpacity = 0.5,
      popup = popups
    ) %>%
    addLegend("bottomright", pal = pal, values = ~data_map$travel_tim, title = "Tiempo")
  
  # Guardar el HTML del mapa como un archivo
  nombre_mapa <- tools::file_path_sans_ext(basename(shp_file))
  html_file <- paste0("C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/Áreas verdes/Output/6_version/", nombre_mapa, "_turbo.html")
  htmlwidgets::saveWidget(mapa_aprovisionamiento, html_file, selfcontained = TRUE)
}

# Iterar sobre todos los shapefiles en la carpeta y generar mapas
for (shp_file in shapefiles) {
  generar_mapa(shp_file)
}