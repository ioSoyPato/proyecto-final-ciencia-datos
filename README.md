#  MLOBS Deployment: IoT Sensor Data on AWS 🚀

## 📚 Motivación del proyecto
Nuestro enfoque actual es la prueba de modelos con **datos de sensores IoT**. El proyecto busca aprovechar el potencial de los datos IoT para ofrecer soluciones inteligentes que no solo mejoren la eficiencia y precisión en la predicción de variables ambientales, sino que también ofrezcan una experiencia de usuario amigable y accesible.

## 🎯 Objetivo
Desarrollar una solución de **ML Deployment** eficiente y escalable que permita desplegar modelos de machine learning y analizarlos de manera gráfica, aprovechando los servicios de AWS para ofrecer resultados rápidos y confiables.

##  Objetivos específicos
1. **Entrenamiento y optimización de modelos predictivos:**

    Desarrollar modelos de predicción para variables ambientales como la temperatura, la humedad y la detección de gases utilizando los datos de sensores IoT.

2. **Automatización y escalabilidad del proceso de deployment:**

    Automatizar el proceso de deployment de los modelos en AWS utilizando MLOps para asegurar actualizaciones continuas y el manejo de nuevas versiones del modelo.

3. **Análisis de la precisión de predicciones:**

    Realizar análisis exhaustivos de la precisión de los modelos en diferentes escenarios.

##  Planteamiento del problema:
Se predecirá la temperatura a través de la toma de sensores.


## 🌱 Dataset: Environmental Sensor Telemetry Data
Este proyecto inicial se basa en un dataset de telemetría ambiental que incluye lecturas de temperatura, humedad, gases y movimiento. Estos datos fueron generados a través de una serie de **dispositivos IoT conectados a Raspberry Pi**, que fueron colocados en ubicaciones con condiciones ambientales variadas.

### 🧠 Estructura del Dataset:
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

## 📜 Antecedentes

### Predicción de la Temperatura
Los avances en el análisis de datos de sensores IoT han permitido predecir variables ambientales críticas, como la temperatura, con gran precisión. Existen numerosos estudios que han utilizado datos de telemetría ambiental para mejorar la predicción de condiciones climáticas y ambientales en tiempo real. Modelos como las redes neuronales, máquinas de soporte vectorial (SVM) y bosques aleatorios (random forests) se han aplicado en este ámbito, con un enfoque en la reducción del error de predicción al utilizar características adicionales como la humedad, gases y presencia de luz o movimiento. Este enfoque multidimensional permite obtener predicciones más precisas, particularmente en entornos variables, como los observados en sensores IoT conectados en ubicaciones geográficas diversas.

### Desarrollo de Plataformas Visuales
El objetivo final de este proyecto es desarrollar una plataforma visual que permita a los usuarios, incluso sin experiencia técnica, realizar análisis de ciencia de datos de manera sencilla. Herramientas como Orange han revolucionado la forma en que se interactúa con grandes volúmenes de datos al proporcionar una interfaz gráfica que facilita la creación de flujos de trabajo de análisis mediante arrastrar y soltar. La combinación de potentes modelos de aprendizaje automático con una interfaz visual amigable ha demostrado ser una solución exitosa para democratizar el análisis de datos, lo que inspiró este proyecto. Al aprovechar AWS para el despliegue y la escalabilidad, este proyecto busca extender estas capacidades hacia el análisis de datos de sensores IoT, ofreciendo una experiencia de usuario optimizada y accesible.

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

