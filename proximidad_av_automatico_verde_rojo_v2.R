library(sf)
library(leaflet)
library(htmlwidgets)
library(webshot)
library(RColorBrewer)

# Carpeta que contiene los shapefiles
carpeta_shapefiles <- "C:/Users/helen/OneDrive/Documentos/Citylab/Indicadores/Áreas verdes/Output/6_version/consolidado/actual_PK.shp"

# Lista de archivos shapefile en la carpeta
shapefiles <- list.files(path = carpeta_shapefiles, pattern = "\\.shp$", full.names = TRUE)

# Función para procesar un shapefile y crear un mapa
generar_mapa <- function(shp_file) {
  # Cargar el shapefile
  data_map <- st_read(shp_file)
  
  # Cargar la máscara que debe ser un polígono disuelto
  mascara_rio <- "C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/area_rio_quitar3.shp"
  mascara_rio <- sf::st_read(mascara_rio)
  
  # Asegurarse de que ambos objetos tengan la misma proyección
  mascara_rio <- st_transform(mascara_rio, st_crs(data_map))
  
  # Eliminar la dimensión Z
  data_map <- st_zm(data_map)
  mascara_rio <- st_zm(mascara_rio)
  
  # Restar la porción de la capa utilizando la máscara
  data_map <- sf::st_difference(data_map, mascara_rio)
  
  # Eliminar la dimensión Z nuevamente (por si acaso)
  data_map <- st_zm(data_map)
  
  # Transformar a la proyección de leaflet si es necesario
  data_map <- st_transform(data_map, crs = '+proj=longlat +datum=WGS84')
  
  # Paleta de colores discreta (RdYlGn)
  pal <- colorFactor(palette = rev(brewer.pal(11, "RdYlGn")), domain = data_map$travel_tim, na.color = "transparent")
  
  # Añadir popups a los polígonos
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
      fillOpacity = 0.7,
      popup = popups
    )
  
  # Añadir el polígono de calles_pp al mapa
  calles_pp <- read_sf("C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/lineas_pp.shp")  # Reemplaza con la ruta correcta
  mapa_aprovisionamiento <- mapa_aprovisionamiento %>%
    addPolylines(
      data = calles_pp,
      weight = 3,
      color = "white",  # Puedes cambiar el color según tus necesidades
      opacity = 0.8
    )
  
  return(mapa_aprovisionamiento)
}
