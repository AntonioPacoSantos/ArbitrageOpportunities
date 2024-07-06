# ArbitrageOpportunities
La idea del siguiente proyecto es dar los primeros pasos en la creación de un bot que automatice la búsqueda de oportunidades de arbitraje de tasas de interés. 
Se implementa entonces, en la clase ArbitrageOpportunities, un modelo que hace lo siguiente: 
1. Primero, see conecta al websocket de remarkets y lee el bid y el offer de cada instrumento elegido. 
2. Luego, computa la tasa implícita tomadora o colocadora, según corresponda, y se imprimen todas en pantalla.
  a. La tasa tomadora se computa como t = ln(bid/spot)/t, donde t = tiempo hasta que cierre el futuro (en años). 
  b. La tasa colocadora se computa como t = ln(offer/spot)/t. 
4. En caso de que haya una oportunidad de arbitraje, se notifica al usuario mediante un print en pantalla.
  a. Si la tasa tomadora es mayor que la tasa de interés de mercado, entonces hay una oportunidad de arbitraje: vender el futuro y comprar el activo subyacente a tasa de mercado.
  b. Si la tasa colocadora es menor que la tasa de interés de mercado, entonces hay una oportunidad de arbitraje: comprar el futuro y vender el activo subyacente; luego, invertir el capital y obtener el interés de mercado. Finalmente, comprar el activo a precio de mercado una vez que cierre el futuro. 
