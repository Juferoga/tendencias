# -*- coding: utf-8 -*-

# Importaciones necesarias
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import seaborn as sns
import matplotlib.pyplot as plt

# Clase para interactuar con la API de MercadoLibre
class MercadoLibreAPI:
    BASE_URL = "https://api.mercadolibre.com"

    def __init__(self, token):
        self.token = token

    def search_products(self, query):
        url = f"{self.BASE_URL}/products/search?status=active&site_id=MLA&q={query}"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch data"}

    def get_categories(self):
        url = f"{self.BASE_URL}/sites/MLA/categories"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch data"}

    def get_products_by_category(self, category_id):
        url = f"{self.BASE_URL}/sites/MLA/search?category={category_id}&"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch data"}

# Inicialización de la API de MercadoLibre
ml_api = MercadoLibreAPI("eltoken")

search_results = ml_api.search_products("laptop")
print(search_results)

categories = ml_api.get_categories()
print(categories)

products_in_category = ml_api.get_products_by_category("MLA1055")
print(products_in_category)

df_product = pd.json_normalize(search_results, 'results')
df_product

# Normalización y manejo de datos
df = pd.json_normalize(products_in_category, 'results')
df.describe()

df

# Exportar datos a CSV
df.to_csv('hola.csv')
df['seller.seller_reputation.transactions.total'].describe()

# Actualizar DataFrame y guardar a CSV
df_updated = df['seller.seller_reputation.transactions.total']
mean_value = df_updated.mean()
df_updated = df_updated.apply(lambda val: 'Alto' if val >= mean_value else 'Bajo')
df_updated.to_csv('hola_2.csv')

# Mostrar la tabla de datos (específico de Colab)
print(str(df.columns))

df_updated

def guardar_grafico(fig, filename):
    """
    Guarda un archivo en la carpeta de Google Drive especificada.
    Args:
    - fig: Objeto de figura de matplotlib a guardar.
    - filename: Nombre del archivo para guardar el gráfico.
    """
    path = f'./reporte/imagenes/{filename}'
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)

fig = plt.figure(figsize=(10, 6))
plt.scatter(df['price'], df['sold_quantity'], c='blue', label='Precio vs Cantidad Vendida')
plt.xlabel('Precio')
plt.ylabel('Cantidad Vendida')
plt.title('Relación entre el Precio y la Cantidad Vendida')
plt.legend()
plt.grid(True)
plt.show()
guardar_grafico(fig, 'precio_ccantidad.png')

fig = plt.figure(figsize=(10, 6))
plt.hist(df['price'], bins=20, color='green', alpha=0.7)
plt.xlabel('Precio')
plt.ylabel('Frecuencia')
plt.title('Distribución de Precios de los Productos')
plt.grid(True)
plt.show()
guardar_grafico(fig, 'precio_prod.png')

fig = plt.figure(figsize=(10, 6))
index = np.arange(len(df))
bar_width = 0.35
plt.bar(index, df['seller.seller_reputation.transactions.completed'], bar_width, label='Completadas')
plt.bar(index + bar_width, df['seller.seller_reputation.transactions.canceled'], bar_width, label='Canceladas', color='red')
plt.xlabel('Vendedor')
plt.ylabel('Transacciones')
plt.title('Comparación de Transacciones Completadas y Canceladas por Vendedor')
plt.xticks(index + bar_width / 2, df['seller.id'])
plt.legend()
plt.show()
guardar_grafico(fig, 'transacts.png')

fig = plt.figure(figsize=(10, 6))
plt.plot(df.index, df['sold_quantity'], marker='o', linestyle='-', color='blue', label='Cantidad Vendida')
plt.xlabel('Orden de Producto')
plt.ylabel('Cantidad Vendida')
plt.title('Evolución de la Cantidad Vendida')
plt.legend()
plt.show()
guardar_grafico(fig, 'evolution.png')

category_counts = df['category_id'].value_counts()
fig = plt.figure(figsize=(10, 8))
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Distribución de Productos por Categoría')
plt.show()
guardar_grafico(fig, 'category.png')

"""## Otras cosas"""

fig = plt.figure(figsize=(12, 6))
df.boxplot(column='price', by='category_id')
plt.title('Distribución de Precios por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Precio')
plt.xticks(rotation=45)
plt.show()
guardar_grafico(fig, 'price_cat_box.png')

fig = plt.figure(figsize=(12, 6))
plt.stackplot(df.index, df['available_quantity'], df['sold_quantity'], labels=['Cantidad Disponible', 'Cantidad Vendida'])
plt.xlabel('Orden del Producto')
plt.ylabel('Cantidad')
plt.title('Tendencias de Cantidad Disponible y Vendida')
plt.legend()
plt.show()
guardar_grafico(fig, 'tendency.png')

"""Este gráfico puede ser útil para comparar las métricas de diferentes vendedores, como cantidad vendida, reputación, etc."""

from math import pi
import matplotlib.pyplot as plt

column_names = ['sold_quantity', 'seller.seller_reputation.transactions.completed', 'price', 'seller.seller_reputation.transactions.canceled']
categories = ['Cantidad Vendida', 'Transacciones Completadas', 'Precio', 'Transacciones Canceladas']
num_vars = len(categories)

values = df[column_names].head(5).values.tolist()
values = [value + [value[0]] for value in values]

angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

for value in values:
    ax.plot(angles, value)
    ax.fill(angles, value, alpha=0.25)

ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)
ax.set_xticks(angles[:-1], categories)
plt.show()
guardar_grafico(fig, 'axes.png')

fig = plt.figure(figsize=(42, 22))

### SEABORN

sns.set_style("white")
cmap = sns.diverging_palette(230, 20, as_cmap=True)

df_numeric = df.select_dtypes(include=[np.number])
sns.heatmap(df_numeric.corr(), annot=True, fmt=".2f", cmap=cmap, linewidths=.5, cbar_kws={"shrink": .1})

plt.xticks(rotation=90, ha='right')
plt.yticks(rotation=0)

plt.title('Mapa de Calor de Correlación entre Variables', fontsize=16)
plt.show()
guardar_grafico(fig, 'correlation.png')