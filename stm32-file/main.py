# Lecture et numérisation du signal d'un capteur Grove de luminosité (LS06-S phototransistor)
# Attention : le capteur doit être alimenté en 5V pour donner une réponse entre 0 et 4095.

from pyb import ADC, Pin # Convertisseur analogique-numérique et GPIO
from time import sleep_ms, time # Pour gérér les temporisations et l'horodatage
import ble_sensor # Pour implémenter le protocole GATT pour Blue-ST
import bluetooth # Classes "primitives du BLE" 

# Instanciation et démarrage du convertisseur analogique-numérique
adc = ADC(Pin('A0'))

# Instance de la classe BLE
ble = bluetooth.BLE()
ble_device = ble_sensor.BLESensor(ble)
led_presence = pyb.LED(2)
presence = 0

sw1 = Pin('SW1' , Pin.IN)
sw1.init(Pin.IN, Pin.PULL_UP, af=-1) 
sw2 = Pin('SW2' , Pin.IN)
sw2.init(Pin.IN, Pin.PULL_UP, af=-1) 

while True:
	valeur_sw1 = sw1.value()
	valeur_sw2 = sw2.value()
	timestamp = time()
	mesure = adc.read()
	valueToDeliver = 0
	
	# Numérise la valeur lue, produit un résultat variable dans le temps dans l'intervalle [0 ; 4095]
	if(presence>0):
		valueToDeliver = 255-(mesure/4095)*255
	
		if(valueToDeliver>220):
			valueToDeliver = 255
		if(valueToDeliver<50):
			valueToDeliver = 0
	
		mesureStr = str(mesure)
		valueToDeliverStr = str(valueToDeliver)
	
		print("Luminosité : "+mesureStr+" (unités arbitraires), puissance délivrée : " + valueToDeliverStr)
		sleep_ms(500)
	else:
		print("Piéce vide, aucune puissance délivrée.")
		sleep_ms(500)

	if valeur_sw1 == 0:
		led_presence.on()
		presence = presence+1
		print("Quelqu'un est entré ! Il y a "+str(presence)+" personne(s).")
		sleep_ms(1000)

	if valeur_sw2 == 0:
		if(presence>0):
			presence = presence-1
			if(presence==0):
				print("Quelqu'un est sortie ! La salle est désormais vide !")
				led_presence.off()
			else:
				print("Quelqu'un est sortie ! Il y a "+str(presence)+" personne(s).")
			sleep_ms(1000)
			
	# Envoie des donn饳 en BLE 
	ble_device.set_data_env(timestamp, int(mesure), int(valueToDeliver), presence, True) 