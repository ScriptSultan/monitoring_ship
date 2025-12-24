import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

#Для построения графика
class PlotManager:
    """Класс для управления графиками в QGraphicsView"""
    
    def __init__(self, graphics_view):
        """
        Инициализация графика в QGraphicsView
        
        Args:
            graphics_view: объект QGraphicsView из UI
        """
        self.graphics_view = graphics_view
        self.setup_plot()
    
    def setup_plot(self):
        """Настройка графика"""
        # Создаем сцену
        self.scene = QtWidgets.QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        
        # Создаем фигуру и canvas Matplotlib
        self.figure = Figure(figsize=(8, 6),  # устанавливает масштаб осей  
                             dpi=100  # устанавливает масштаб плоскости
                             )
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        
        # Добавляем canvas на сцену
        self.proxy_widget = self.scene.addWidget(self.canvas)
        
        # Базовая настройка графика
        self.axes.grid(True, alpha=0.3)
        self.axes.set_xlabel('Время', fontsize=10)
        self.axes.set_ylabel('Значение', fontsize=10)
        self.axes.set_title('Мониторинг данных', fontsize=12, fontweight='bold')
        
        # Убираем белые поля вокруг графика
        self.figure.tight_layout()
        
        self.canvas.draw()
    
    def plot_data(self, x_data, y_data, plot_type='line', **kwargs):
        """
        Построение графика данных
        
        Args:
            x_data: данные по оси X
            y_data: данные по оси Y
            plot_type: тип графика ('line', 'scatter', 'bar')
            **kwargs: дополнительные параметры для matplotlib
        """
        # Очищаем предыдущий график
        self.axes.clear()
        
        # Строим новый график в зависимости от типа
        if plot_type == 'line':
            self.axes.plot(x_data, y_data, 
                          #linewidth=2, 
                          marker='o', 
                          markersize=4,
                          **kwargs)
        elif plot_type == 'scatter':
            self.axes.scatter(x_data, y_data, 
                             s=50, 
                             alpha=0.7,
                             **kwargs)
        elif plot_type == 'bar':
            self.axes.bar(x_data, y_data,
                         alpha=0.7,
                         **kwargs)
        
        # Обновляем настройки
        self.axes.grid(True, alpha=0.3)
        self.axes.set_xlabel('Время', fontsize=10)
        self.axes.set_ylabel('Значение', fontsize=10)
        self.axes.set_title('Мониторинг данных', fontsize=12, fontweight='bold')
        
        # Добавляем легенду если есть label
        if 'label' in kwargs:
            self.axes.legend()
        
        # Автоматическое масштабирование
        self.axes.relim()
        self.axes.autoscale_view()
        
        # Обновляем canvas
        self.canvas.draw()
    
    def update_plot(self, new_x, new_y):
        """
        Быстрое обновление данных без полной перерисовки
        
        Args:
            new_x: новые данные по X
            new_y: новые данные по Y
        """
        if self.axes.lines:
            self.axes.lines[0].set_data(new_x, new_y)
            self.axes.relim()
            self.axes.autoscale_view()
            self.canvas.draw()
        else:
            self.plot_data(new_x, new_y)
    
    def clear_plot(self):
        """Очистка графика"""
        self.axes.clear()
        self.axes.grid(True, alpha=0.3)
        self.axes.set_xlabel('Время', fontsize=10)
        self.axes.set_ylabel('Значение', fontsize=10)
        self.axes.set_title('Мониторинг данных', fontsize=12, fontweight='bold')
        self.canvas.draw()
    
    def set_title(self, title):
        """Установка заголовка графика"""
        self.axes.set_title(title, fontsize=12, fontweight='bold')
        self.canvas.draw()
    
    def set_labels(self, x_label, y_label):
        """Установка подписей осей"""
        self.axes.set_xlabel(x_label, fontsize=10)
        self.axes.set_ylabel(y_label, fontsize=10)
        self.canvas.draw()