import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


plt.style.use('ggplot')


history = pd.read_csv('history.csv')

plt.figure(figsize=(10, 5))
plt.plot(history['epoch'], history['accuracy'], marker='o', label='Точность')
plt.xlabel('Эпоха')
plt.ylabel('Точность')
plt.title('Зависимость точности на валидации от эпох обучения')
plt.legend()
plt.grid(True)
plt.show()



plt.figure(figsize=(8, 6))
top5.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.title('Топ-5 наиболее частых классов в валидационном наборе')
plt.ylabel('')
plt.show()
