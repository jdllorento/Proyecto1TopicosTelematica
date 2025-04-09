import sys
import os

# Obtener la ruta absoluta del directorio del proyecto
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MICROSERVICES_PATH = os.path.join(PROJECT_ROOT, "microservices")

# Agregar al path si no está ya
if MICROSERVICES_PATH not in sys.path:
    sys.path.insert(0, MICROSERVICES_PATH)  # insert(0) tiene prioridad
