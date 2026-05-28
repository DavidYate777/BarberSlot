# BarberSlot

Plataforma de agendamiento de citas para barberias de alta gama.  
Desarrollada en HTML, CSS y JavaScript puro. Lista para desplegarse en **GitHub Pages** sin configuracion adicional de servidor.

---

## Estructura del Proyecto

```
BarberSlot/
├── index.html                   # Landing page principal
├── login.html                   # Inicio de sesion
├── registro.html                # Registro de clientes
│
├── cliente/
│   ├── dashboard.html           # Panel del cliente
│   └── agendar.html             # Agendamiento de cita
│
├── barbero/
│   └── dashboard.html           # Panel del barbero
│
├── admin/
│   ├── dashboard.html           # Panel de administracion
│   └── registrar_barbero.html   # Registro de barberos
│
└── static/
    └── style.css                # Estilos globales
```

---

## Despliegue en GitHub Pages

1. Haz un fork o sube este repositorio a tu cuenta de GitHub.
2. Ve a **Settings > Pages** en tu repositorio.
3. En **Source**, selecciona la rama `main` y la carpeta `/ (root)`.
4. Guarda los cambios. GitHub Pages publicara el sitio automaticamente.
5. Accede a tu sitio en: `https://<tu-usuario>.github.io/<nombre-repositorio>/`

---

## Acceso de Demostracion

La plataforma incluye navegacion completa en modo demostracion.  
Desde la pagina de login puedes acceder directamente a cada panel:

| Rol           | URL de acceso directo            |
|---------------|----------------------------------|
| Cliente       | `cliente/dashboard.html`         |
| Barbero       | `barbero/dashboard.html`         |
| Administrador | `admin/dashboard.html`           |

---

## Tecnologias

- HTML5 semantico
- CSS3 con variables personalizadas (sin frameworks externos)
- JavaScript vanilla (sin dependencias)
- Google Fonts: Cormorant Garamond + Montserrat

---

## Paleta de Diseño

| Token         | Valor      | Uso                         |
|---------------|------------|-----------------------------|
| `--black`     | `#0a0a0a`  | Fondo principal             |
| `--gold`      | `#c9a84c`  | Acento primario             |
| `--gold-light`| `#e2c270`  | Hover de elementos dorados  |
| `--white`     | `#f5f5f0`  | Texto principal             |
| `--white-muted`| `#b8b8b2` | Texto secundario            |

---

&copy; 2026 BarberSlot. Todos los derechos reservados.
