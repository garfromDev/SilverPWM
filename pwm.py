#-*- coding: utf-8 -*-

# Application de controle flux Led par PWM

import RPi.GPIO as GPIO
import time

# ==  Partie afficheur =============
# indique quel port GPIO est connecté à quel segment de l'afficheur
branchements =   {"A" : 25, "B" : 23, "C" : 27, "D" : 5, "E" : 17, "F" : 12, "G" : 20}

# Affiche le nombre passé en paramètre
# x : la nombre entier entre 0 et 9
# afficheur : le dictionaire de correspondance 
def displayNumber (afficheur, x) :
    GPIO.output(afficheur['A'], x in [0,2,3,5,6,7,8,9])

    GPIO.output(afficheur['B'], x in [0,1,2,3,4,7,8,9])

    GPIO.output(afficheur['C'], x in [0,1,3,4,5,6,7,8,9])

    GPIO.output(afficheur['D'], x in [0,2,3,5,6,8,9])

    GPIO.output(afficheur['E'], x in [0,2,6,8])

    GPIO.output(afficheur['F'], x in [0,4,5,6,8,9])

    GPIO.output(afficheur['G'], x in [2,3,4,5,6,8,9])
    print("for " + str(x) + " segment G est " + str(x in [2,3,4,5,6,8,9]))

# Affiche le nombre passé en paramètre
# x : le caractère  entre A et F
# afficheur : le dictionaire de correspondance     
def displayChar(afficheur, x):
    GPIO.output(afficheur['A'], x in ['A', 'B', 'C', 'D', 'E', 'F'])
    GPIO.output(afficheur['B'], x in ['A', 'B',  'D'])
    GPIO.output(afficheur['C'], x in ['A', 'B',  'D' ])
    GPIO.output(afficheur['D'],  x in [ 'B', 'C', 'D', 'E'])
    GPIO.output(afficheur['E'],  x in ['A', 'B', 'C', 'D', 'E', 'F'])
    GPIO.output(afficheur['F'],  x in ['A', 'B', 'C', 'D', 'E', 'F'])
    GPIO.output(afficheur['G'], x in ['A', 'B',   'E', 'F'])   

#initialise les sortie nécessaire pour l'affichage
def initDisplay(afficheur):
    outputs = [ afficheur[i] for i in afficheur]
    GPIO.setup(outputs, GPIO.OUT, initial = GPIO.LOW)


#===== Initialisation =========
GPIO.setmode(GPIO.BCM)
flux = 100
initDisplay(branchements)

#bouton augmenter
#on cable le bouton pour forcer a la masse en cas d'appui
#donc on configure un pul up par defaut
hBtn = 26
GPIO.setup(hBtn,GPIO.IN, pull_up_down=GPIO.PUD_UP)

def higher(channel):
	global flux
	global pwm
	if flux < 100:
		flux = flux + 10
		print(flux)
		if flux < 100:
			displayNumber(branchements, flux / 10)
		else:
			displayChar(branchements, 'F')

		pwm.ChangeDutyCycle(100 - flux)

GPIO.add_event_detect(hBtn, GPIO.FALLING, callback=higher, bouncetime=200)

#bouton diminuer
lBtn = 19
GPIO.setup(lBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def lower(channel):
	global flux
	global pwm
	if flux > 0:
		flux = flux - 10
		print(flux)
		pwm.ChangeDutyCycle(100 - flux)
		displayNumber(branchements, flux / 10)


GPIO.add_event_detect(lBtn, GPIO.FALLING, callback=lower, bouncetime=200)


# ==== Demarage du programme ===	
#lancement du PWM
pwmOutput = 18
GPIO.setup(pwmOutput,GPIO.OUT)
pwm = GPIO.PWM(pwmOutput, 2200)
print("starting")
displayChar(branchements, 'F')
pwm.start(0)

while True:
	time.sleep(0.1)



