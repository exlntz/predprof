import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# style
plt.style.use('seaborn-v0_8-darkgrid')

## GRAPH 1
# data_load
history = pd.read_csv('history.csv')  # epoch, accuracy, loss
train_labels = pd.read_csv('train_labels.csv')  # class
test_preds = pd.read_csv('test_predictions.csv')  # колонки: true_class, predicted_class
valid_labels = pd.read_csv('valid_labels.csv')  # колонка: class

## GRAPH 2
plt.figure(figsize=(10, 6))
plt.plot(history['epoch'], history['accuracy'], marker='o',
         linewidth=2, markersize=6, color='#2E86AB', label='Точность')
plt.xlabel('Эпоха', fontsize=12)
plt.ylabel('Точность', fontsize=12)
plt.title('Зависимость точности на валидации от количества эпох',
          fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('static/graph_accuracy.png', dpi=100, bbox_inches='tight')
plt.close()
