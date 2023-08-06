import logging
from codigofacilito_copia_de_nolan import unreleased

# """
# TIPO -> Nivel
# INFO -> 10
# DEBUG -> 20
# WARNING -> 30
# ERROR -> 40
# CRITICAL -> 50
# """
# Solo los mensajes de nivel 30 o mayor se ejecutan en consola por defecto

# Con este comando, a partir de nivel DEBUG, se mostrará en consola
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
  logging.debug("Se está comenzando la ejecución del paquete")
  
  workshops = unreleased()
  logging.debug(workshops)

  logging.debug("Finalizó la ejecución del paquete")