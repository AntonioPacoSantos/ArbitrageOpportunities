# ArbitrageOpportunities
La idea del siguiente proyecto es dar los primeros pasos en la creación de un bot que automatice la búsqueda de oportunidades de arbitraje de tasas de interés. 
Se implementa entonces, en la clase ArbitrageOpportunities, un modelo que hace lo siguiente: 
1. Primero, see conecta al websocket de remarkets y lee el bid y el offer de cada instrumento elegido. 
2. Luego, computa la tasa implícita tomadora o colocadora, según corresponda, y se imprimen todas en pantalla.
3. En caso de que haya una oportunidad de arbitraje, se notifica al usuario mediante un print en pantalla.

