import paho.mqtt.client as mqtt
import json
import time
import random

# CLASE PARA DISP IOT
class DispositivoIoT:
    def operar(self):
        pass

# CL P/SENSOR
class SensorSonido(DispositivoIoT):
    def obtener_lectura(self):
        # SIMULA LECTURA
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

# CL PARA COMU MQTT
class ComunicacionMQTT:
    def __init__(self, dispositivo_id):
        self.client = mqtt.Client()
        self.dispositivo_id = dispositivo_id
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def conectar(self):
        # CONECTAR BROKER MQTT
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        # RECIBIR MJES
        client.subscribe("topic/suscripcion")

    def on_message(self, client, userdata, msg):
        # MANEJAR MJES REC
        print("Mensaje recibido: " + msg.topic + " " + str(msg.payload))

    def enviar_datos(self, datos):
        # PUBLICAR DATOS
        payload = json.dumps(datos)
        self.client.publish("topic/publicacion", payload)

# CREA INSTANCIA SENSOR Y COM MQTT
sensor_sonido = SensorSonido()
comunicacion_mqtt = ComunicacionMQTT(dispositivo_id="sensor_sonido")

try:
    # CONECTA  MQTT
    comunicacion_mqtt.conectar()
    
    while True:
        # OBTIENE LECTURA Y OPERA
        resultados = sensor_sonido.operar()
        
        # ENVIA DATOS A TRAVES  MQTT
        comunicacion_mqtt.enviar_datos(resultados)
        
        # ESPERA ´
        time.sleep(5)

except KeyboardInterrupt:
    print('Interrumpido')
