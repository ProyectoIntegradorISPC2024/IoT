import random
import time

class DispositivoIoT:
    def operar(self):
        pass

class SensorSonido(DispositivoIoT):
    def obtener_lectura(self):
        return round(random.uniform(20, 80), 1)
    
    def operar(self):
        sonido = self.obtener_lectura()
        nivel_ruido = self.clasificar_ruido(sonido)
        recomendar_ruta = self.recomendar_ruta(sonido)
        return sonido, nivel_ruido, recomendar_ruta
        
    def clasificar_ruido(self, sonido):
        if sonido < 40:
            return 'Nivel de ruido apto'
        elif 40 <= sonido <= 60:
            return 'Nivel de ruido tolerable' 
        else:
            return 'Nivel de ruido no apto'
        
    def recomendar_ruta(self, sonido):
        if sonido < 40:
            return 'Ruta recomendable'
        elif 40 <= sonido <= 60:
            return 'Ruta riesgosa'
        else:
            return 'Ruta no recomendable'

class LuzLED:
    def encender(self):
        print("La luz LED está encendida")

    def apagar(self):
        print("La luz LED está apagada")

class AdministradorDispositivos:
    def __init__(self):
        self.dispositivos = []
    
    def agregar_dispositivo(self, dispositivo):
        self.dispositivos.append(dispositivo)
    
    def operar(self):
        resultados = []
        for dispositivo in self.dispositivos:
            resultado = dispositivo.operar()
            resultados.append(resultado)
        return resultados

administrador = AdministradorDispositivos()
administrador.agregar_dispositivo(SensorSonido())

luz = LuzLED()

try:
    while True:
        resultados = administrador.operar()
        for resultado in resultados:
            sonido, nivel_ruido, recomendar_ruta = resultado
            print(f'Sonido detectado: {sonido} decibeles\n{nivel_ruido}\n{recomendar_ruta}')
            
            # Simular el encendido o apagado de la luz LED
            if sonido >= 60:
                luz.encender()
            else:
                luz.apagar()
            
        time.sleep(5)
except KeyboardInterrupt:
    print('Interrumpido')
