# Ataque-DTP-VLAN-Hopping

# Reporte Técnico: Ataque de Negociación de Enlace Troncal (DTP Spoofing)

**Estudiante:** Cristopher de los Santos  
**ID:** 2024-1414  
**Institución:** Instituto Tecnológico de Las Américas (ITLA)  
**Materia:** Seguridad de Redes

---

## 1. Objetivo del Script / Ataque
El objetivo principal de esta práctica es demostrar la vulnerabilidad del protocolo **DTP (Dynamic Trunking Protocol)** cuando los puertos de un switch están configurados en modo dinámico por defecto. Mediante la inyección de paquetes DTP maliciosos, se busca forzar al switch a establecer un enlace troncal (*Trunk*) con la máquina atacante, permitiendo a esta última realizar un "VLAN Hopping" y acceder al tráfico de todas las VLANs permitidas en el switch.

---

Aquí tienes el código completo en formato Markdown, optimizado para que lo copies y pegues directamente en tu archivo README.md. He integrado la topología exacta de tu imagen y el direccionamiento basado en tu red 10.14.14.x.

Markdown
# Reporte Técnico: Ataque de Negociación de Enlace Troncal (DTP Spoofing)

**Estudiante:** Cristopher de los Santos  
**ID:** 2024-1414  
**Institución:** Instituto Tecnológico de Las Américas (ITLA)  
**Fecha:** 27 de febrero de 2026

---

## 1. Objetivo del Script / Ataque
Demostrar la vulnerabilidad del protocolo propietario **DTP (Dynamic Trunking Protocol)** en switches Cisco. El ataque busca forzar la creación de un enlace troncal (*Trunk*) no autorizado desde una estación de trabajo (Kali Linux) para obtener acceso a múltiples VLANs y eludir los controles de segmentación de Capa 2.

---

## 2. Topología de Red
Basado en el entorno simulado en GNS3, la infraestructura se compone de los siguientes nodos:

### Conectividad de Interfaces
| Equipo | Interfaz Local | Conectado a | Función |
| :--- | :--- | :--- | :--- |
| **IOU3 (ROUTER)** | `e0/0` | IOU1 (`e0/0`) | Gateway de la Red |
| | `e1/0` | AAA-1 (`eth0`) | Servidor de Autenticación |
| | `e0/3` | IOU2 (`e0/3`) | Enlace Backbone |
| **IOU1 (SWITCH)** | `e0/2` | **KaliAttacks-1** (`e1`) | Punto de Inyección (Vulnerable) |
| | `e0/1` | IOU2 (`e0/1`) | Inter-Switch Link |
| **IOU2 (SWITCH)** | `e0/0` | webterm-7 (`eth0`) | Acceso de Usuario |
| **KaliAttacks-1** | `e1` | IOU1 (`e0/2`) | Nodo de Auditoría |

### Cuadro de Direccionamiento IP (Red 10.14.14.0/24)
| Dispositivo | Dirección IP | Gateway | VLAN |
| :--- | :--- | :--- | :--- |
| **Gateway (IOU3)** | 10.14.14.1 | N/A | 1 |
| **KaliAttacks-1** | 10.14.14.10 | 10.14.14.1 | Trunk |
| **webterm-7** | 10.14.14.50 | 10.14.14.1 | 10 |

---

## 3. Requisitos de la Herramienta
Para la ejecución exitosa de este ataque se requiere:
1.  **Sistema Operativo:** Kali Linux actualizado.
2.  **Software de Ataque:** * `Yersinia`: Para la manipulación de protocolos de Capa 2.
    * `Scapy`: Para la creación de paquetes personalizados (en caso de scripts manuales).
3.  **Drivers:** Soporte para el módulo de kernel `8021q` (VLAN tagging).

---

## 4. Parámetros Usados
Durante el ataque, se definieron los siguientes parámetros técnicos:
* **Protocolo:** DTP (Dynamic Trunking Protocol).
* **Tipo de Ataque:** "Enable Trunking" (Negotiate Trunk).
* **Encapsulación:** 802.1Q (Dot1q).
* **Timeout de Negociación:** 0.1s entre ráfagas de paquetes.

---

## 5. Procedimiento y Capturas de Pantalla

### Paso 1: Verificación de vulnerabilidad
<img width="466" height="336" alt="image" src="https://github.com/user-attachments/assets/53b669dd-ae40-4ee7-a090-1948a654aefd" />


### Paso 2: Ejecución del ataque
<img width="366" height="196" alt="image" src="https://github.com/user-attachments/assets/9647f2f4-41cb-4a96-a659-63b86d0850b8" />

### paso 3: demostracion de exito
<img width="613" height="103" alt="image" src="https://github.com/user-attachments/assets/f6a420ea-faba-4ca1-b2f5-34d4b6491f13" />

### 6. Medidas de Mitigación (Hardening)
Para asegurar la infraestructura del ITLA contra este vector de ataque, se deben implementar las siguientes configuraciones de seguridad:

1.  **Forzar Modo Acceso:** Definir estáticamente los puertos de usuario para evitar negociaciones accidentales o maliciosas.
    ```cisco
    switchport mode access
    ```
2.  **Desactivar DTP (`nonegotiate`):** Inhabilitar el protocolo DTP en todos los puertos (incluyendo troncales legítimos) para que no se envíen ni procesen tramas de negociación.
    ```cisco
    switchport nonegotiate
    ```
3.  **Gestión de VLAN Nativa:** Cambiar la VLAN nativa (por defecto 1) a una ID que no esté en uso y asegurar que no sea la misma que las VLANs de datos.
4.  **Shutdown de Puertos:** Apagar físicamente todos los puertos que no estén en uso activo.

---

## 6. Procedimiento y Resultados

### Paso 1: Captura de la Topología en GNS3
*(Insertar captura de la topología completa mostrando los puntos verdes de conexión)*

### Paso 2: Estado del Switch antes del ataque
Se observa que el puerto `Et0/2` está en modo dinámico.
*(Insertar captura del comando: `show interfaces Et0/2 switchport`)*

### Paso 3: Ejecución del ataque con Yersinia
Inyección de tramas DTP desde Kali.
```bash
sudo yersinia dtp -attack 1 -i eth1
