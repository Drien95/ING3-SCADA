from flask import Flask, render_template, request, jsonify
from pyModbusTCP.client import ModbusClient
import threading

app = Flask(__name__)

# Configuration Modbus
MODBUS_HOST = '127.0.0.1'
MODBUS_PORT = 502
MODBUS_CLIENT = ModbusClient(host=MODBUS_HOST, port=MODBUS_PORT)

# Adresses Modbus (COILS) - Mise à jour avec les adresses fournies
SENSOR_ADDRESS = 0
ENTRY_CONVEYOR_ADDRESS = 0
STOP_BLADE_ADDRESS = 1
EXIT_CONVEYOR_ADDRESS = 2
BLUE_SORTER_BELT_ADDRESS = 4
BLUE_SORTER_TURN_ADDRESS = 3 # Note: Turn address is numerically *lower* than belt
GREEN_SORTER_BELT_ADDRESS = 6
GREEN_SORTER_TURN_ADDRESS = 5 # Note: Turn address is numerically *lower* than belt
METAL_SORTER_BELT_ADDRESS = 8
METAL_SORTER_TURN_ADDRESS = 7 # Note: Turn address is numerically *lower* than belt
EMITTER_ADDRESS = 8 # Typo in your list, assuming EMITTER_ADDRESS = 9 was intended, corrected to 8 to match your list

# Variables globales pour le statut manuel (optionnel, pour un contrôle plus avancé)
manual_control_states = {
    'entry_conveyor': None,
    'stop_blade': None,
    'exit_conveyor': None,
    'blue_belt': None,
    'green_belt': None,
    'metal_belt': None, # Ajout pour Metal Belt/Turn
    'blue_sorter': None, # Ajout pour commande combinée Blue
    'green_sorter': None, # Ajout pour commande combinée Green
    'metal_sorter': None  # Ajout pour commande combinée Metal
}

def send_modbus_command(address, state):
    """Fonction pour envoyer une commande Modbus (exécutée dans un thread)."""
    try:
        print(f"Tentative d'écriture Modbus : Adresse={address}, Etat={state}")
        if not MODBUS_CLIENT.is_open:
            print("Connexion Modbus non ouverte, tentative d'ouverture...")
            MODBUS_CLIENT.open()
        if MODBUS_CLIENT.is_open:
            print("Connexion Modbus ouverte.")
            MODBUS_CLIENT.write_single_coil(address, state)
            print(f"Commande Modbus écrite avec succès : Adresse={address}, Etat={state}")
        else:
            print("Erreur: Impossible d'ouvrir la connexion Modbus pour l'envoi de la commande.")
    except Exception as e:
        print(f"Erreur Modbus dans le thread: {e}")
    finally:
        if MODBUS_CLIENT.is_open:
            MODBUS_CLIENT.close()
            print("Connexion Modbus fermée.")

@app.route('/', methods=['GET'])
def index():
    """Page principale."""
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    """Route pour recevoir les commandes et lancer un thread pour Modbus."""
    control_name = request.form.get('control')
    state = request.form.get('state') == 'true'

    if control_name == 'entry_conveyor':
        address = ENTRY_CONVEYOR_ADDRESS
        thread = threading.Thread(target=send_modbus_command, args=(address, state))
    elif control_name == 'stop_blade':
        address = STOP_BLADE_ADDRESS
        thread = threading.Thread(target=send_modbus_command, args=(address, state))
    elif control_name == 'exit_conveyor':
        address = EXIT_CONVEYOR_ADDRESS
        thread = threading.Thread(target=send_modbus_command, args=(address, state))
    elif control_name == 'blue_belt': # Anciens boutons individuels - conservés pour compatibilité si vous les utilisez encore
        address = BLUE_SORTER_BELT_ADDRESS
        thread = threading.Thread(target=send_modbus_command, args=(address, state))
    elif control_name == 'green_belt': # Anciens boutons individuels - conservés pour compatibilité si vous les utilisez encore
        address = GREEN_SORTER_BELT_ADDRESS
        thread = threading.Thread(target=send_modbus_command, args=(address, state))
    elif control_name == 'metal_belt': # Anciens boutons individuels - conservés pour compatibilité si vous les utilisez encore
        address = METAL_SORTER_BELT_ADDRESS
        thread = threading.Thread(target=send_modbus_command, args=(address, state))
    elif control_name == 'blue_sorter': # Nouveaux boutons combinés Blue Sorter (Belt + Turn)
        belt_address = BLUE_SORTER_BELT_ADDRESS
        turn_address = BLUE_SORTER_TURN_ADDRESS
        # Lancer deux threads pour activer Belt et Turn en parallèle
        thread_belt = threading.Thread(target=send_modbus_command, args=(belt_address, state))
        thread_turn = threading.Thread(target=send_modbus_command, args=(turn_address, state))
        thread_belt.start()
        thread_turn.start()
        thread = None # Pas besoin de thread principal pour le jsonify, on a lancé les 2 threads spécifiques
    elif control_name == 'green_sorter': # Nouveaux boutons combinés Green Sorter (Belt + Turn)
        belt_address = GREEN_SORTER_BELT_ADDRESS
        turn_address = GREEN_SORTER_TURN_ADDRESS
        # Lancer deux threads pour activer Belt et Turn en parallèle
        thread_belt = threading.Thread(target=send_modbus_command, args=(belt_address, state))
        thread_turn = threading.Thread(target=send_modbus_command, args=(turn_address, state))
        thread_belt.start()
        thread_turn.start()
        thread = None # Pas besoin de thread principal pour le jsonify, on a lancé les 2 threads spécifiques
    elif control_name == 'metal_sorter': # Nouveaux boutons combinés Metal Sorter (Belt + Turn)
        belt_address = METAL_SORTER_BELT_ADDRESS
        turn_address = METAL_SORTER_TURN_ADDRESS
        # Lancer deux threads pour activer Belt et Turn en parallèle
        thread_belt = threading.Thread(target=send_modbus_command, args=(belt_address, state))
        thread_turn = threading.Thread(target=send_modbus_command, args=(turn_address, state))
        thread_belt.start()
        thread_turn.start()
        thread = None # Pas besoin de thread principal pour le jsonify, on a lancé les 2 threads spécifiques
    else:
        return jsonify({'status': 'error', 'message': 'Contrôle inconnu'}), 400

    if thread: # S'assurer qu'un thread a été créé (pour les contrôles simples)
        thread.start() # Démarrer le thread
    return jsonify({'status': 'success', 'control': control_name, 'state': state})

if __name__ == '__main__':
    app.run(debug=True)