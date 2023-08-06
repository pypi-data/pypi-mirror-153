# Super Log
### Funcion
    Enriquece la informacion de los logs para nuestro procesos python,
    los mensajes vienen en formato json para poder ser usados
    por cualquier software de captura de logs, ejemplo: New Relic.
## Pasos
### Intalar librerira
    pip install superlog
### Importar la librerira:
    from superlog.log import SuperLog
### Agregar identificador de proyecto e instanciar la clase
    log = SuperLog(app_name="my_app")
### Metodo decorador - tiempo de ejecucion por funcion:
    @log.time_func_analyze
    def mi_funcion():
        print("inicio")
        ...
        time.sleep(1)
        return True

    ## Tiempo de ejecucion de una funcion
    mi_funcion()

    # ejemplo de salida
    {"level":"INFO","timestamp":"2022-05-06 13:27:27,981","app":"my_app","log":{"total": 1.01, "function": "main"}}

### Metodo decorador - tiempo total:
    @log.time_func_analyze(total_execution=True)
    def funcion_principal():
        print("inicio")
        ...
        time.sleep(1)
        return True

    ## Tiempo de ejecucion de una funcion
    funcion_principal()

    ## ejemplo de salida
    {"level":"INFO","timestamp":"2022-05-06 13:31:35,701","app":"my_app","log":{"total_execution": 1.0}}
        
### Manejo de mensajes y errores automaticos:
    ## mensaje normal
    log.print("hola mundo")
    
    ## ejemplo de salida
    {"level":"INFO","timestamp":"2022-05-06 13:35:00,091","app":"my_app","log":{"message": "Hola Mundo", "execution": 0.01, "function": "main"}}

    ## mensaje error
    ## automaticamente superlog detecta los erres de los try y except e imprime toda la informacion correspondiente
    ## ejemplo:

    try:
        variable_no_existe
    except:
        log.print("Ocurrio un error")

    ##ejemplo salida
    {"level":"ERROR","timestamp":"2022-05-06 13:37:48,257","app":"my_app","log":{"message": "Ocurrio un error", "execution": 0.01, "file": "/ruta/archivo.py", "line": "130", "function": "main", "statement": "['variable_no_existe\n']", "error": "<class 'NameError'>", "text": "name 'variable_no_existe' is not defined", "manual": false}}

### Manejo de errores manuales:
    ## En caso de querer querer usar errores de manera manual 
    ## sin la necesidad de usar try y execpt, se puede realizar de la 
    ## siguiente manera
 
    def main():
        log.error("Hola mundo error")

    main()
    
    ## ejemplo de salida
    {"level":"ERROR","timestamp":"2022-05-06 13:40:50,094","app":"my_app","log":{"message": "Hola mundo error", "execution": 0.01, "function": "main", "manual": true}}



### Manejo de warnings manuales:
 
    def main():
        log.warning("Hola mundo warning")

    main()
    
    ## ejemplo de salida
    {"level":"WARNING","timestamp":"2022-05-06 13:40:50,094","app":"my_app","log":{"message": "Hola mundo warning", "execution": 0.01, "function": "main", "manual": true}}




### Manejo de info manuales:
 
    def main():
        log.info("Hola mundo info")

    main()
    
    ## ejemplo de salida
    {"level":"INFO","timestamp":"2022-05-06 13:40:50,094","app":"my_app","log":{"message": "Hola mundo info", "execution": 0.01, "function": "main", "manual": true}}


