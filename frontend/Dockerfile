# Imagen de desarrollo, simple y de una sola etapa (multi-stage queda para otra clase).
FROM node:22-alpine

# pnpm con la versión registrada en el TRD
RUN npm install -g pnpm@12.4.1

WORKDIR /app

# Primero las dependencias (fijadas por pnpm-lock.yaml), después el código.
# Se copian carpetas puntuales para no arrastrar el node_modules de Windows.
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY index.html vite.config.js ./
COPY public ./public
COPY src ./src

EXPOSE 5173
CMD ["pnpm", "dev", "--host", "0.0.0.0"]