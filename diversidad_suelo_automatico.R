library(viridisLite)
library(sf)
library(leaflet)
library(htmlwidgets)
library(viridis)
library(webshot)


# Carpeta que contiene los shapefiles
carpeta_shapefiles <- "C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/diversity_land_uses/output/2_version/actual/"

# Lista de archivos shapefile en la carpeta
shapefiles <- list.files(path = carpeta_shapefiles, pattern = "\\.shp$", full.names = TRUE)



# Función para procesar un shapefile y crear un mapa
generar_mapa_diversidad <- function(shp_file) {
  # Cargar el shapefile
  data_map <- read_sf(shp_file)
  
  # Eliminar la dimensión Z
  data_map <- st_zm(data_map)
  
  # Transforma a la proyección de leaflet si es necesario
  data_map <- st_transform(data_map, crs = '+proj=longlat +datum=WGS84')
  
  # Paleta de colores continua (turbo)
  pal <- colorNumeric(palette = viridis(100, option = "turbo"), domain = data_map$diversity, na.color = "transparent")
  
  # Añade popups a los polígonos
  popups <- sprintf("<b>Diversidad de Suelo:</b> %s", data_map$diversity)
  
  # Crear el objeto de mapa
  mapa_diversidad <- leaflet(data = data_map) %>%
    addTiles() %>%
    addProviderTiles(providers$CartoDB.Positron) %>%
    setView(lng = -73.06, lat = -36.83, zoom = 14) %>%
    addPolygons(
      fillColor = ~pal(data_map$diversity),
      stroke = FALSE,
      weight = 1,
      opacity = 0.8,
      color = "white",
      fillOpacity = 0.5,
      popup = popups
    ) %>%
    addLegend("bottomright", pal = pal, values = ~data_map$diversity, title = "Diversidad de Suelo")
  
  # Guardar el HTML del mapa como un archivo
  nombre_mapa <- tools::file_path_sans_ext(basename(shp_file))
  html_file <- paste0("C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/diversity_land_uses/output/2_version/", nombre_mapa, "_diversidad.html")
  htmlwidgets::saveWidget(mapa_diversidad, html_file, selfcontained = TRUE)
}

# Iterar sobre todos los shapefiles en la carpeta y generar mapas de diversidad
for (shp_file in shapefiles) {
  generar_mapa_diversidad(shp_file)

mapa_diversidad

# Capturar y guardar como PNG
#png_file <- paste0("C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/diversity_land_uses/output/2_version/", nombre_mapa, "_diversidad.png")3webshot::webshot(html_file, file = png_file, cliprect = "viewport", vwidth = 1200, vheight = 800)
}

# Iterar sobre todos los shapefiles en la carpeta y generar mapas de diversidad
#for (shp_file in shapefiles) {3  generar_mapa_diversidad(shp_file)
#}

