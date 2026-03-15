import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# style
plt.style.use('seaborn-v0_8-darkgrid')

# data_load
history = pd.read_csv('history.csv')  # epoch, accuracy, loss
train_labels = pd.read_csv('train_labels.csv')  # class
test_preds = pd.read_csv('test_predictions.csv')  # true_class, predicted_class
valid_labels = pd.read_csv('valid_labels.csv')  # class

## GRAPH 1
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

## GRAPH 2
plt.figure(figsize=(12, 6))
class_counts = train_labels['class'].value_counts().sort_index()
colors = plt.cm.viridis(np.linspace(0, 1, len(class_counts)))
bars = plt.bar(class_counts.index.astype(str), class_counts.values, color=colors)

plt.xlabel('Класс', fontsize=12)
plt.ylabel('Количество записей', fontsize=12)
plt.title('Распределение записей по классам в обучающем наборе',
          fontsize=14, fontweight='bold')

# numbers
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{int(height)}', ha='center', va='bottom', fontsize=9)

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('static/graph_classes.png', dpi=100, bbox_inches='tight')
plt.close()

## GRAPH 3
plt.figure(figsize=(14, 5))
correct = (test_preds['true_class'] == test_preds['predicted_class']).astype(int)

# colours
colors = ['#2ecc71' if x == 1 else '#e74c3c' for x in correct]

plt.bar(range(len(correct)), correct, color=colors, width=0.8)
plt.xlabel('Номер записи в тестовом наборе', fontsize=12)
plt.ylabel('Правильность', fontsize=12)
plt.title('Точность определения каждой записи из тестового набора',
          fontsize=14, fontweight='bold')
plt.yticks([0, 1], ['Ошибка', 'Верно'])
plt.ylim(-0.1, 1.1)

# stats
accuracy = correct.mean() * 100
plt.text(0.95, 0.95, f'Общая точность: {accuracy:.1f}%',
          transform=plt.gca().transAxes, ha='right', va='top',
          bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('static/graph_test_accuracy.png', dpi=100, bbox_inches='tight')
plt.close()
