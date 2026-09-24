from PIL import Image

# Cambia 'tu_imagen.jpg' por la ruta de tu archivo de imagen
ruta_imagen = "imagen/a.png"

try:
    # Abrir la imagen
    imagen = Image.open(ruta_imagen)
    
    # Mostrar la imagen en el visor predeterminado del sistema
    imagen.show()
except FileNotFoundError:
    print(f"No se encontró la imagen en la ruta: {ruta_imagen}")

print("Por si no jala")