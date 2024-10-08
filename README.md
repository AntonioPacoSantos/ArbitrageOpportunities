# ArbitrageOpportunities
## Introducción 
La idea del siguiente proyecto es dar los primeros pasos en la creación de un bot que automatice la búsqueda de oportunidades de arbitraje de tasas de interés utilizando futuros. 
Se implementa entonces, en la clase ArbitrageOpportunities, un modelo que hace lo siguiente: 
1. Primero, see conecta al websocket de remarkets y lee el bid y el offer de cada instrumento elegido. 
2. Luego, computa la tasa implícita tomadora o colocadora, se actualiza- si corresponde- y se imprime su valor en pantalla.
  - La tasa tomadora se computa como t = ln(bid/spot)/t, donde t = tiempo hasta que cierre el futuro (en años). 
  - La tasa colocadora se computa como t = ln(offer/spot)/t. 
3. En caso de que haya una oportunidad de arbitraje, se almacena esa información y se imprime en pantalla la oportunidad de arbitraje. 
  - Si la tasa tomadora es mayor que la tasa de interés de mercado, entonces hay una oportunidad de arbitraje: vender el futuro y comprar el activo subyacente a tasa de mercado.
  - Si la tasa colocadora es menor que la tasa de interés de mercado, entonces hay una oportunidad de arbitraje: comprar el futuro y vender el activo subyacente; luego, invertir el capital y obtener el interés de mercado.  
  - Si la tasa tomadora es mayor que la colocadora (este caso es casi imposible de encontrar, pero existe la ínfima posibilidad, por lo que no se debería descartar), se vende y se compra el futuro. 
  
## Ejecución 
Para ejecutarlo, acceder al directorio api y luego correr el comando 
`python3 arbitrage_detection.py`
Para correr los tests, 
`python3 test.py`
La primera vez, es necesario que el usuario ingrese sus credenciales (usuario,contraseña y cuenta). Luego de esto, se creará un archivo config.txt, en el que se guardarán los datos para no tener que volver a solicitarlos al correr el programa en un futuro.

## Algunas consideraciones 
- Para determinar la tasa de interés de mercado, se utilizaron los bonos del tesoro americano a 13 semanas, IRX. 
- Con ese valor, se computó el valor para la tasa de interés de mercado mediante la fórmula: r = ((1+IRX)^t) -1, donde t es el tiempo hasta que cierre el futuro (t = 1 implica 13 semanas restantes, ya que ese es el plazo del IRX)
- Para obtener un valor del dolar real (notar que el que provee por defecto yfinance es el oficial, que no se puede utilizar para operar), se calculó el CCL dividiendo el valor de la acción de YPF en pesos (YPFD.BA), por el de la acción de YPF en dolares (YPF). 

## REST API y frontend (Actualización)
- En esta actualización, se implementó una rest api, que permite a los usuarios loggearse con sus cuentas de remarkets y observar las oportunidades de arbitraje que el bot encuentra en una interfaz frontend. 
Para acceder a la misma, la url es [Link](https://frontend-arbitrage-opportunities.pages.dev/login)

## Actualización 
- Actualmente, el proyecto no se encuentra deployado. 

