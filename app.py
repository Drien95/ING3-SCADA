from flask import Flask, render_template, request, jsonify
from pyModbusTCP.client import ModbusClient
import threading

app = Flask(__name__)

# Configuration Modbus
MODBUS_HOST = '127.0.0.1'
MODBUS_PORT = 502
MODBUS_CLIENT = ModbusClient(host=MODBUS_HOST, port=MODBUS_PORT)

# Adresses Modbus (COILS) 
SENSOR_ADDRESS = 0
ENTRY_CONVEYOR_ADDRESS = 0
STOP_BLADE_ADDRESS = 1
EXIT_CONVEYOR_ADDRESS = 2
BLUE_SORTER_BELT_ADDRESS = 4
BLUE_SORTER_TURN_ADDRESS = 3 
GREEN_SORTER_BELT_ADDRESS = 6
GREEN_SORTER_TURN_ADDRESS = 5 
METAL_SORTER_BELT_ADDRESS = 8
METAL_SORTER_TURN_ADDRESS = 7 
EMITTER_ADDRESS = 8 

# Variables globales pour le statut manuel 
manual_control_states = {
    'entry_conveyor': None,
    'stop_blade': None,
    'exit_conveyor': None,
    'blue_belt': None,
    'green_belt': None,
    'metal_belt': None, 
    'blue_sorter': None, # Blue
    'green_sorter': None, # Green
    'metal_sorter': None  # Metal
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
    elif control_name == 'blue_belt': 
        address = BLUE_SORTER_BELT_ADDRESS
        thread = threading.Thread(target=send_modbus_command, args=(address, state))
    elif control_name == 'green_belt': 
        address = GREEN_SORTER_BELT_ADDRESS
        thread = threading.Thread(target=send_modbus_command, args=(address, state))
    elif control_name == 'metal_belt': 
        address = METAL_SORTER_BELT_ADDRESS
        thread = threading.Thread(target=send_modbus_command, args=(address, state))
    elif control_name == 'blue_sorter': #
        belt_address = BLUE_SORTER_BELT_ADDRESS
        turn_address = BLUE_SORTER_TURN_ADDRESS
      
        thread_belt = threading.Thread(target=send_modbus_command, args=(belt_address, state))
        thread_turn = threading.Thread(target=send_modbus_command, args=(turn_address, state))
        thread_belt.start()
        thread_turn.start()
        thread = None 
    elif control_name == 'green_sorter': 
        belt_address = GREEN_SORTER_BELT_ADDRESS
        turn_address = GREEN_SORTER_TURN_ADDRESS
       
        thread_belt = threading.Thread(target=send_modbus_command, args=(belt_address, state))
        thread_turn = threading.Thread(target=send_modbus_command, args=(turn_address, state))
        thread_belt.start()
        thread_turn.start()
        thread = None 
    elif control_name == 'metal_sorter':
        belt_address = METAL_SORTER_BELT_ADDRESS
        turn_address = METAL_SORTER_TURN_ADDRESS
    
        thread_belt = threading.Thread(target=send_modbus_command, args=(belt_address, state))
        thread_turn = threading.Thread(target=send_modbus_command, args=(turn_address, state))
        thread_belt.start()
        thread_turn.start()
        thread = None 
    else:
        return jsonify({'status': 'error', 'message': 'Contrôle inconnu'}), 400

    if thread: 
        thread.start() 
    return jsonify({'status': 'success', 'control': control_name, 'state': state})

if __name__ == '__main__':
    app.run(debug=True)
