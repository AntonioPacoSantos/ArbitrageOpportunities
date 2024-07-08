# ArbitrageOpportunities
## Introducción 
La idea del siguiente proyecto es dar los primeros pasos en la creación de un bot que automatice la búsqueda de oportunidades de arbitraje de tasas de interés. 
Se implementa entonces, en la clase ArbitrageOpportunities, un modelo que hace lo siguiente: 
1. Primero, see conecta al websocket de remarkets y lee el bid y el offer de cada instrumento elegido. 
2. Luego, computa la tasa implícita tomadora o colocadora, según corresponda, y se imprimen todas en pantalla.
  - La tasa tomadora se computa como t = ln(bid/spot)/t, donde t = tiempo hasta que cierre el futuro (en años). 
  - La tasa colocadora se computa como t = ln(offer/spot)/t. 
4. En caso de que haya una oportunidad de arbitraje, se notifica al usuario mediante un print en pantalla.
  - Si la tasa tomadora es mayor que la tasa de interés de mercado, entonces hay una oportunidad de arbitraje: vender el futuro y comprar el activo subyacente a tasa de mercado.
  - Si la tasa colocadora es menor que la tasa de interés de mercado, entonces hay una oportunidad de arbitraje: comprar el futuro y vender el activo subyacente; luego, invertir el capital y obtener el interés de mercado. Finalmente, comprar el activo a precio de mercado una vez que cierre el futuro. 
  - Si la tasa tomadora es mayor que la colocadora (este caso es casi imposible de encontrar, pero existe la ínfima posibilidad, por lo que no se debería descartar), se vende y se compra el futuro. 
  
## Ejecución 
Para ejecutarlo, alcanza con correr el comando 
`python3 arbitrage_detection.py`
Para correr los tests, 
`python3 test.py`
La primera vez, es necesario que el usuario ingrese sus credenciales (usuario,contraseña y cuenta). Luego de esto, se creará un archivo config.txt, en el que se guardarán los datos para no tener que volver a solicitarlos al correr el programa en un futuro.

## Algunas consideraciones 
- Para determinar la tasa de interés de mercado, se utilizaron los bonos del tesoro americano a 13 semanas, IRX. 
- Para obtener un valor del dolar real (notar que el que provee por defecto yfinance es el oficial, que no se puede utilizar para operar), se calculó el CCL dividiendo el valor de la acción de YPF en pesos (YPFD.BA), por el de la acción de YPF en dolares (YPF). 

