# AISol
# Intérprete de Lengua de Señas Colombiana con IA

![Interprete LSC](https://example.com/banner.png)

## Descripción
Este proyecto utiliza inteligencia artificial para interpretar el Lenguaje de Señas Colombiano (LSC) en tiempo real. Aplicamos modelos de aprendizaje profundo para mejorar la accesibilidad y comunicación de la comunidad sorda en Colombia.

## Autores
- **Nicole Páez Vásquez**
- **Javier Esteban Arciniegas Moreno**

## Tecnologías
- **Señas estáticas**: YOLO, OpenCV, PyTorch, Roboflow
- **Señas en movimiento**: TensorFlow, Keras, OpenCV, MediaPipe, Scikit-learn

## Repositorios
- [Señas estáticas](https://github.com/Estebax20006/senias-yolo)
- [Señas en movimiento](https://github.com/Nik-nicole/proyecto-IA_sena)

## Metodología
1. **Recolección de Datos**: Captura de imágenes y videos de señas en múltiples contextos.
2. **Entrenamiento de Modelos**:
   - Modelo de detección de señas estáticas.
   - Modelo de reconocimiento de señas en movimiento.
3. **Implementación**: Integración en aplicaciones web y móviles.

## Resultados
- **Señas estáticas**: +90% de precisión.
- **Señas en movimiento**: 40-60% de precisión con datos limitados.

## Conclusiones
Este proyecto representa un avance en accesibilidad para la comunidad sorda. La precisión en señas estáticas es alta, mientras que las señas en movimiento requieren más datos para mejorar su rendimiento.

## Próximos pasos
- Aumentar la base de datos de señas en movimiento.
- Optimizar los modelos para dispositivos móviles.

## Licencia
Este proyecto se distribuye bajo la licencia MIT.

---
Servicio Nacional de Aprendizaje - Centro de Servicios Financieros

---
# Estructuara del proyecto y recomendaciones
![image](https://github.com/user-attachments/assets/50352332-3ebf-4a23-9670-f514e000726b)

aqui tu puedes encontrar la estructura en carpetas que se ve en el codigo 

donde la carpeta back_user contiene todo el back y configuracion del inicio de sesion como el de registro

y las carpetas MP_DATA, animals y Fruits contienen toda la data de videos que se necesecitaron y se necesitan para entrenar los modelos 

lo demas son los notbooks donde se encuentra paso a paso como entrenar cada modelo y como estos se pueden usar

cabe aclarar que antes de iniciar en este proyecto voy a dar unas recomendaciones tecnicas:

version de python recomendada : 3.12.5 o 3.12.9
instalar anaconda para la gestion de entornos virtuales con varias versiones de python
instalar flask 
Tener en cuenta tanto la carpeta migratiosn como el .env para el back , ya que esto puede generar una serie de errores si no es configurado correctamente, para inicializar tanto la base de datos y sus rutas como lo es los package pip del .env que son aparte del entorno virtual creado en anaconda.
