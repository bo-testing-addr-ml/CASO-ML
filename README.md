# CASO-ML
ML challenge

** OBJETIVOS **
  * Leer y guardar campos del archivo "JSON_Data.txt" en base de datos.
  * Leer y guardar campos del archivo "CSV_Data.txt" en base de datos.
  * Enviar un correo al owner por cada base de datos cuya criticidad esté clasificada como "high", para solicitar su validación.
  
** SUPUESTOS **
  * El campo "row_id" del "CSV_Data.txt" corresponde al nombre de la base de datos.
  * Mail del owner es calculado a través del campo "user_id" del archivo "CSV_Data.txt", y es: user_id + "@gmail.com". Puede ser cambiado en el código.
  * Mail del manager sigue la misma lógica que el anterior, pero con el campo "user_manager", del archivo "CSV_Data.txt".
  
** DETALLES DE LA SOLUCIÓN **
  * No se instalaron paquetes o librerías adicionales a los incluidos por defecto en Python 3.9.5
  * Se construyó una base de datos guardada en memoria. Esto puede cambiarse a través del código para generar un archivo ".db".
  * Se utilizó un correo electrónico creado con este único propósito. En caso de ser necesario, solicitar la clave para ejecutar pruebas.

** ESTRUCTURAS DE ARCHIVOS (JSON & CSV) **
  * JSON_Data.txt: {
    "clasificacion-bd":[
      {
        "base-de-datos":"db-1",
        "clasificacion":"high"
      },
      {
        "base-de-datos":"db-2",
        "clasificacion":"low"
      },
    ]
  }
  * CSV_Data.txt: 
    - headers: row_id; user_id; user_state; user_manager
    - separador: ";"
