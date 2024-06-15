import random
import time
import paho.mqtt.client as mqtt
import json


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

# Clase para el actuador de luz LED
class LuzLED:
    def encender(self):
        print("La luz LED está encendida")

    def apagar(self):
        print("La luz LED está apagada")

# Clase para la comunicación MQTT
class ComunicacionMQTT:
    def __init__(self, dispositivo_id):
        self.client = mqtt.Client()
        self.dispositivo_id = dispositivo_id
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def conectar(self):
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Conectado al broker MQTT con código {rc}")
        client.subscribe("topic/suscripcion")

    def on_message(self, client, userdata, msg):
        print("Mensaje recibido: " + msg.topic + " " + str(msg.payload))

    def enviar_datos(self, datos):
        payload = json.dumps(datos)
        self.client.publish("topic/publicacion", payload)

# Clase para administrar dispositivos
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

# Crear instancias del sensor y la luz LED
sensor_sonido = SensorSonido()
luz = LuzLED()
comunicacion_mqtt = ComunicacionMQTT(dispositivo_id="sensor_sonido")

# Crear el administrador de dispositivos y agregar el sensor
administrador = AdministradorDispositivos()
administrador.agregar_dispositivo(sensor_sonido)

try:
    # Conectar a MQTT
    comunicacion_mqtt.conectar()
    
    while True:
        # Operar los dispositivos
        resultados = administrador.operar()
        for resultado in resultados:
            sonido, nivel_ruido, recomendar_ruta = resultado
            print(f'Sonido detectado: {sonido} decibeles\n{nivel_ruido}\n{recomendar_ruta}')
            
            # Simular el encendido o apagado de la luz LED
            if sonido >= 60:
                luz.encender()
            else:
                luz.apagar()
            
            # Enviar datos a través de MQTT
            comunicacion_mqtt.enviar_datos({
                "sonido": sonido,
                "nivel_ruido": nivel_ruido,
                "recomendar_ruta": recomendar_ruta
            })
            
        time.sleep(5)
except KeyboardInterrupt:
    print('Interrumpido')
