
import osmnx as ox
import networkx as nx
import folium
from folium.plugins import MarkerCluster
import pandas as pd
import numpy as np
import geopandas as gpd


# GRAFO A PARTIR DE COORDENADAS DE DISTRITO ELEGIDO

#Crear un grafo a partir de un punto latitud longitud
# punto = (-12.070874,-77.02552)
# g = ox.graph_from_point(punto , distance = 500)


# GRAFO : LA VICTORIA

class Rutas():
    def __init__(self,ruta_b = None):
        self.ruta_b = ruta_b

    def graficar_rutas_mapa(self,num_puntos):
        """Usando Networkx para calcular la distancia entre dos puntos aleatorios
            (de esa forma vemos las rutas que el usuario ha elegido

            num_puntos : cantidad de rutas que queremos
            Retorna --> rutas : las rutas simuladas de los usuarios del aplicativo

            """
        rutas = {}
        punto = (-12.070874,-77.02552)
        g = ox.graph_from_point(punto , distance = 500)
        for i in range(0,num_puntos):
            route = nx.shortest_path(g,np.random.choice(g.nodes),np.random.choice(g.nodes))
            rutas[f'ruta{i}'] = route
        return rutas , g

    # rutas, g = graficar_rutas_mapa(5)


    # EN ESTA FUNCION LE DAS LA RUTA (USUARIO) QUE FUE DETECTADO COMO INFECTADO


    def hallar_intersecciones(self,rutas,nombre_ruta,g):
        """
        rutas --> diccionario con los OSM ID de las rutas generadas aleatoriamente
        nombre_ruta --> nombre de la ruta que va a tener estado = infectado
        retorna : todos los tipos de intersecciones (OSM ID, latitud y longitud)
        """
        intersecciones = {}
        intersecciones_x = []
        intersecciones_y = []

        for key,value in rutas.items():
            interseccion = list(set(rutas[nombre_ruta]).intersection(rutas[key]))
            intersecciones[f'{key}'] = interseccion

        for key,route in intersecciones.items():
            if key != nombre_ruta:
                for node in route:
                    intersecciones_x.append(g.nodes[node]['x'])
                    intersecciones_y.append(g.nodes[node]['y'])
        return intersecciones_x, intersecciones_y, intersecciones


    # intersecciones_x , intersecciones_y,intersecciones = hallar_intersecciones(rutas,'ruta1',g)

    def posibles_infectados(self,rutas,intersecciones):
        """
        intersecciones -- > diccionario con las intersecciones entre el infectado y el resto de gente
        retorna : posibles rutas de infectados
        """

        rutas_posibles_afectados = {}
        for key,value in intersecciones.items():
            if key in rutas and (len(intersecciones[key]) > 0):
                rutas_posibles_afectados[f'{key}'] = rutas[key]
        return rutas_posibles_afectados


    def mapa_interactivo(self,g,rutas,nombre_ruta):
        """  crea un mapa interactivo con folium con las rutas que se le den
        g --> grafo creado del punto de ubicacion
        rutas --> diccionario con las rutas de los usuarios
        retorna : Folium.Map() con las rutas que se esecifiquen"""

        m = folium.Map(location = [-12.070874,-77.02552],zoom_start = 15,tiles = 'Stamen Terrain')
        colors = ['blue','blue','green','green','brown']
        for ruta in rutas:
            if ruta != nombre_ruta:
                color = np.random.choice(colors)
            else:
                color = 'red'
            temp = ox.plot_route_folium(g,rutas[ruta],route_map = m,route_color = color)
        return m


    def mapa_interseccion(self,intersecciones_x,intersecciones_y):
        """crea un mapa con un marcador de donde podria haber sido el punto de contacto"""

        mapa = folium.Map(location = [-12.070874,-77.02552],zoom_start = 15,tiles = 'Stamen Terrain')
        coordenadas = list(zip(intersecciones_x,intersecciones_y))
        marker_cluster = MarkerCluster().add_to(mapa)
        for coord in coordenadas:
            mapa.add_child(folium.Marker(location = [coord[1],coord[0]], fill_color='#43d9de', radius=8 ))
        return mapa


    "MAPA LA VICTORIA"
    def resultados(self,rutas,intersecciones,g,intersecciones_x,intersecciones_y,nombre_ruta):
        from IPython.display import display
        rutas_posibles_afectados = self.posibles_infectados(rutas,intersecciones)
        mapa1 = self.mapa_interactivo(g,rutas,nombre_ruta)
        mapa1.save('mapa1.html')
        mapa2 =self.mapa_interactivo(g,rutas_posibles_afectados,nombre_ruta)
        mapa2.save('mapa2.html')
        """ PUNTOS DE POSIBLE INFECCION  """

        #PUNTOS PARA POSIBLE INFECCION
        mapa = self.mapa_interseccion(intersecciones_x,intersecciones_y)
        mapa.save('mapa_interseccion.html')


    def main(self,num_puntos,nombre_ruta,n_clicks = None):
        rutas, g = self.graficar_rutas_mapa(num_puntos)
        intersecciones_x, intersecciones_y,intersecciones = self.hallar_intersecciones(rutas = rutas,nombre_ruta = nombre_ruta,g = g)
        self.resultados(rutas,intersecciones,g,intersecciones_x,intersecciones_y,nombre_ruta)


# try:
#     main(5,'ruta1')
# except:
#     print('Error de conexion')


# In[ ]:
