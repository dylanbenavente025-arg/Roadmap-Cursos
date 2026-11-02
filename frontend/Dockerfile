# ---------- Etapa 1: builder (instala dependencias y genera el build de Vite) ----------
FROM node:22-alpine AS builder

# pnpm con la versión registrada en el TRD
RUN npm install -g pnpm@12.4.1

WORKDIR /app

# Primero las dependencias, para aprovechar la caché de capas
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# El .dockerignore (ticket C27-T8) deja afuera node_modules, dist y los tests
COPY . .
RUN pnpm run build

# ---------- Etapa 2: runtime (nginx sirve los archivos estáticos) ----------
FROM nginx:alpine-slim AS runtime

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

# nginx responde /health sin depender del backend
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1/health || exit 1