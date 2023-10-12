import subprocess
import re
import time

def get_signal_strength():
    try:
        # Exécute la commande 'netsh wlan show interfaces' pour obtenir les informations sur les interfaces Wi-Fi
        output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], encoding='utf-8')
        
        # Utilise une expression régulière pour rechercher la puissance du signal
        signal_strength_match = re.search(r'Signal[ ]+: (\d+)%', output)
        
        if signal_strength_match:
            signal_strength = signal_strength_match.group(1)
            print(f"Puissance du signal : {signal_strength}%")
        else:
            print("Aucune information sur la puissance du signal trouvée.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    while True:
        get_signal_strength()
        time.sleep(1)  
