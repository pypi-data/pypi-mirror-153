import logging
from my_package_xy import unreleased

logging.basicConfig(level=logging.DEBUG)

##Ejecuta todolo del bloque si y solo si este archivo se jecuta
###como principal.

if __name__ == "__main__":
    logging.debug(">>> Se está comenzando la ejecución del paquete.")

    workshops = unreleased()

    logging.debug(">>> Se está finalizando la ejecución del paquete")