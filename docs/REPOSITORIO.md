# Crear el repositorio privado

Estos comandos son para que los ejecute el usuario. No se inicializó Git, no se hicieron commits ni se publicó el proyecto durante la documentación.

Git guarda versiones locales; GitHub aloja el remoto. Un nombre posible es `pacman-gestion-administrativa`; la elección final corresponde al grupo. Mantener visibilidad **Private**.

## 1. Iniciar y revisar

En PowerShell:

```powershell
Set-Location 'D:\Codex\7Pacman'
git init -b main
git status --short
```

`.gitignore` excluye datos, informes, respaldos, entornos virtuales y temporales. No borra los archivos locales. Un clon limpio crea los maestros y permite registrar nuevos usuarios al ejecutar `main.py`.

No agregar los documentos originales de la consigna ni sus metadatos personales por defecto; la documentación resume su relación con el proyecto.

## 2. Preparar el primer commit

```powershell
git add .gitignore README.md requirements.txt archivos_fijos.py colisiones.py config.py informes.py juego.py laberinto.py main.py objetos.py partidas.py usuarios.py docs tools
git diff --cached --stat
git ls-files
```

Revisar que no figuren `datos/`, `informes/`, `respaldos/` ni `.local/`. El maestro contiene claves en texto plano y los informes pueden reproducirlas. La privacidad del remoto no sustituye esta selección.

Consultar la identidad configurada:

```powershell
git config user.name
git config user.email
```

Si hace falta, configurar nombre y correo del autor del commit con valores propios; no inventar identidad colectiva. La identidad técnica de quien realiza el commit no cambia la autoría grupal declarada en la documentación.

```powershell
git commit -m "Documentar versión final del proyecto grupal Pac-Man"
```

## 3. Crear el remoto privado y subir

En GitHub crear un repositorio con la cuenta y nombre elegidos, seleccionar **Private** y dejarlo vacío, sin generar README, licencia ni `.gitignore` remotos. Copiar la URL real que muestre GitHub.

```powershell
# Sustituir el texto por la URL real del repositorio privado.
git remote add origin 'URL_REAL_DEL_REPOSITORIO'
git push -u origin main
```

No ejecutar con el marcador literal. Tras subir, comprobar la visibilidad privada y los archivos visibles. Invitar a los compañeros o al profesor solo cuando el grupo lo decida.

## 4. Cambios futuros

```powershell
git status --short
git diff
# Agregar únicamente los archivos que se quieran registrar.
git add docs README.md
git diff --cached
git commit -m "Ampliar explicaciones para la defensa oral"
git push
```

La licencia y las atribuciones externas quedan para acuerdo colectivo. Presentar el juego como proyecto educativo inspirado en Pac-Man, sin afirmar afiliación oficial. Para datos de demostración, usar registros ficticios; el script de verificación ya trabaja con ellos en una carpeta temporal.
