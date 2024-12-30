# from devices.ar_condicionado.ar_condicionado import ArCondicionado
from devices.ar_condicionado import ArCondicionado
from devices.caixa_de_som import CaixaDeSom
from devices.luz_artificial import LuzArtificial

print("1 - Ar Condicionado")
print("2 - Caixa de Som")
print("3 - Luz Artificial")
device_to_start = int(input("Qual dispositivo iniciar? "))

if device_to_start > 0 and device_to_start < 4:
  [ArCondicionado, CaixaDeSom, LuzArtificial][device_to_start - 1]().start()
