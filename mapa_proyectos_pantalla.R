
# Instala las bibliotecas si no las tienes instaladas
install.packages(c("leaflet", "sf"))

# Carga las bibliotecas necesarias
library(leaflet)
library(sf)

# Carga el shapefile de proyectos
proyecto_aurora <- read_sf("C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/proyectos/Aurora_de_Chile.geojson")
proyecto_pdv<- read_sf("C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/proyectos/Pedro_de_Valdivia.geojson")
proyecto_pdr<- read_sf("C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/proyectos/Pedro_del_Rio.geojson")
placas<- read_sf("C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/proyectos/placas.geojson")
#id_placa <- read_sf("C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/punto_etiqueta.geojson")

# Transforma a la proyección de leaflet si es necesario
proyecto_aurora <- st_transform(proyecto_aurora, crs = '+proj=longlat +datum=WGS84')
proyecto_pdv <- st_transform(proyecto_pdv, crs = '+proj=longlat +datum=WGS84')
proyecto_pdr <- st_transform(proyecto_pdr, crs = '+proj=longlat +datum=WGS84')
placas <- st_transform(placas, crs = '+proj=longlat +datum=WGS84')
#id_placa <- st_transform(id_placa, crs = '+proj=longlat +datum=WGS84')

# Obtener los centroides de los polígonos de placas
#centroids_placas <- st_centroid(placas)
#centroids_placas <- st_transform(placas, crs = '+proj=longlat +datum=WGS84')


# Colores y nombres de etiqueta (leyenda)
colores <- c('#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c',
             '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928')
etiquetas <- levels(as.factor(proyecto_aurora$Tipo))


# Cambiando color
paleta_aurora <- colorFactor(palette = colores, domain = proyecto_aurora$Tipo)
paleta_pdv <- colorFactor(palette = colores, domain = proyecto_pdv$Tipo)
paleta_pdr <- colorFactor(palette = colores, domain = proyecto_pdr$Tipo)


# Añade popups a los polígonos
popups_aurora <- sprintf("<b>Nombre:</b> %s<br/><b>Tipo:</b> %s", proyecto_aurora$Nom_proy, proyecto_aurora$Tipo)
popups_pdv <- sprintf("<b>Nombre:</b> %s<br/><b>Tipo:</b> %s", proyecto_pdv$Nom_proy, proyecto_pdv$Tipo)
popups_pdr <- sprintf("<b>Nombre:</b> %s<br/><b>Tipo:</b> %s", proyecto_pdr$Nombre, proyecto_pdr$Tipo)



st_crs(proyecto_aurora)
st_crs(proyecto_pdv)
st_crs(proyecto_pdr)
st_crs(placas)





mapa <-  leaflet() %>%
  addProviderTiles(providers$CartoDB.Positron) %>%
  setView(lng = -73.06, lat = -36.83, zoom = 14) %>%
  addPolygons(data = proyecto_aurora, fillColor = ~paleta_aurora(etiquetas), color = "white", weight = 0.5, fillOpacity = 1, popup = popups_aurora, group = "Cartera de proyectos")%>% 
  addPolygons(data = proyecto_pdv, fillColor = ~paleta_pdv(Tipo), color = "white", weight = 0.5, fillOpacity = 1, popup = popups_pdv, group = "Cartera de proyectos") %>%
  addPolygons(data = proyecto_pdr, fillColor = ~paleta_pdr(Tipo), color = "white", weight = 0.5, fillOpacity = 1, popup = popups_pdr, group = "Cartera de proyectos") %>%
  addPolygons(data = placas, fillColor = "transparent", color = "black", weight = 2, fillOpacity = 0, dashArray = "5,5", group = "Placas") %>%
  addLayersControl(overlayGroups = c("Cartera de proyectos", "Placas"), options = layersControlOptions(collapsed = TRUE))
#  addCircleMarkers(data = id_placa, lng = ~st_coordinates(.)[, 6], lat = ~st_coordinates(.)[, 5], radius = 1, color = "transparent", fillOpacity = 0, label = ~ID_PLACA)

  
mapa <- mapa %>% 
  addLegend(data = proyecto_pdr, position =  "bottomleft", pal = paleta_pdr,
            values = ~Tipo, title = "Temáticas", opacity = 1,
            group = "Leyenda")
mapa

html_file <- "C:/Users/helen/OneDrive/Documentos/Citylab/Maqueta/proyectos.html"
htmlwidgets::saveWidget(mapa, html_file, selfcontained = TRUE)

















































