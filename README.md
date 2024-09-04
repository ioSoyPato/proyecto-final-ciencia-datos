# 🌐 MLOBS Deployment: IoT Sensor Data on AWS 🚀

## 📚 Overview
Este proyecto tiene como objetivo la creación de un **modelo de MLOBS** (Machine Learning Operations and Deployment) centrado en la implementación de modelos de aprendizaje automático utilizando servidores de AWS. Nuestro enfoque actual es la prueba de modelos con **datos de sensores IoT** y, en el futuro, este proyecto podría evolucionar para convertirse en una **plataforma visual al estilo "Orange"** para el análisis de ciencia de datos de cualquier dataset, ¡todo con una interfaz gráfica amigable!

## 🎯 Objetivo
Desarrollar una solución de **ML Deployment** eficiente y escalable que permita desplegar modelos de machine learning y analizarlos de manera gráfica, aprovechando los servicios de AWS para ofrecer resultados rápidos y confiables.

## 🌱 Dataset: Environmental Sensor Telemetry Data
Este proyecto inicial se basa en un dataset de telemetría ambiental que incluye lecturas de temperatura, humedad, gases y movimiento. Estos datos fueron generados a través de una serie de **dispositivos IoT conectados a Raspberry Pi**, que fueron colocados en ubicaciones con condiciones ambientales variadas.

### 🧠 Características del Dataset:
- **Periodo**: 07/12/2020 - 07/19/2020
- **Dispositivos IoT**: 
  - `00:0f:00:70:91:0a`: Condiciones estables, más frío y húmedo.
  - `1c:bf:ce:15:ec:4d`: Temperatura y humedad altamente variables.
  - `b8:27:eb:bf:9d:51`: Condiciones estables, más cálido y seco.
  
- **Sensores y Medidas**:
  - Temperatura (°F)
  - Humedad (%)
  - Monóxido de Carbono (ppm)
  - Gas LP (ppm)
  - Detección de humo (ppm)
  - Luz (Booleano)
  - Movimiento (Booleano)
  
- **Formato de Mensajes**: Los datos fueron transmitidos usando el protocolo MQTT, que sigue el estándar ISO para la transmisión de telemetría en redes de sensores.

### 🔢 Ejemplo de Payload MQTT:

```json
{
  "data": {
    "co": 0.0061,
    "humidity": 55.1,
    "light": true,
    "lpg": 0.0089,
    "motion": false,
    "smoke": 0.0239,
    "temp": 31.8
  },
  "device_id": "6e:81:c9:d4:9e:58",
  "ts": 1594419195.292461
}
```

### 📝 Estructura del Dataset:
| Column   | Descripción          | Unidades    |
|----------|----------------------|------------|
| `ts`     | Timestamp del evento  | Epoch      |
| `device` | ID único del dispositivo | String  |
| `co`     | Monóxido de carbono   | ppm (%)    |
| `humidity` | Humedad            | %          |
| `light`  | Detección de luz      | Boolean    |
| `lpg`    | Gas LP               | ppm (%)    |
| `motion` | Detección de movimiento | Boolean   |
| `smoke`  | Humo                 | ppm (%)    |
| `temp`   | Temperatura          | Fahrenheit |

## 🏗️ Próximos Pasos
1. **Entrenamiento y Evaluación** de modelos predictivos basados en los datos de sensores.
2. Implementación de **pruebas en AWS** para evaluar el rendimiento y escalabilidad.
3. Creación de una **interfaz gráfica** intuitiva para que cualquier usuario pueda realizar análisis de ciencia de datos fácilmente.

## 🛠️ Tecnologías Utilizadas
- **AWS (Amazon Web Services)**: Para el deployment y la infraestructura.
- **Python**: Lenguaje de programación principal para el desarrollo de los modelos.
- **IoT MQTT Protocol**: Para la transmisión de datos en tiempo real.
- **Machine Learning**: Modelos de predicción y análisis.

---

### 🚀 Únete al Viaje
Este es solo el comienzo de un viaje emocionante para democratizar el análisis de datos mediante una plataforma visual impulsada por IA. ¡Te invitamos a seguir nuestras actualizaciones y colaborar con nosotros en este emocionante proyecto!
