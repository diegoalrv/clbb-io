# Usa una imagen base con Node.js
FROM node:14

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# Copia el archivo package.json e instala las dependencias
COPY package*.json ./
RUN npm install

# Copia todos los archivos del proyecto al contenedor
COPY . .

# Compila la aplicación React
RUN npm run build

# Expone el puerto 3000
EXPOSE 3000

# Inicia la aplicación cuando se ejecute el contenedor
CMD ["npm", "start"]
