from PyQt6 import QtWidgets, QtWidgets, uic
import sys
import numpy as np
import pyqtgraph as pg

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Загружаем .ui файл динамически (self — это QMainWindow)
        uic.loadUi('untitled.ui', self)

        self.replace_graphics_view_with_plot()

        # Инициализация графика
        self.add_plot_data()

        # Если нужны сигналы (кнопки и т.д.)
        # self.connect_signals()
    def replace_graphics_view_with_plot(self):
        """
            Замена QGraphicsView на pyqtgraph PlotWidget
        """
        # Находим graphicsView в UI
        graphics_view = self.findChild(QtWidgets.QGraphicsView, "graphicsView")
        # if graphics_view:
        # Сохраняем геометрию и родителя
        geometry = graphics_view.geometry()
        parent = graphics_view.parent()
        
        #PlotWidget
        self.plot_graph = pg.PlotWidget(parent=parent)
        self.plot_graph.setObjectName("plot_graph")
        self.plot_graph.setGeometry(geometry)  # Та же позиция/размер
        
        self.plot_graph.setBackground((40, 40, 40)) 
        self.plot_graph.setStyleSheet("""
            QWidget { 
                background: rgb(40, 40, 40); 
                color: rgb(255, 255, 255); 
                border: 1px solid rgb(60, 60, 60); 
                border-radius: 4px; 
            }
            QGraphicsView { 
                border: none; 
            }
            /* Стили скроллбаров (скопируйте из вашего .ui stylesheet для graphicsView) */
            QScrollBar:vertical {
                background: rgb(25, 25, 25);
                width: 15px;
                margin: 0px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: rgb(210, 96, 255);
                min-height: 20px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgb(225, 130, 255);
            }
            QScrollBar::handle:vertical:pressed {
                background: rgb(190, 70, 235);
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: rgb(25, 25, 25);
                border: none;
            }/* Аналогично для horizontal */
            QScrollBar:horizontal {
                background: rgb(25, 25, 25);
                height: 15px;
                margin: 0px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background: rgb(210, 96, 255);
                min-width: 20px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgb(225, 130, 255);
            }
            QScrollBar::handle:horizontal:pressed {
                background: rgb(190, 70, 235);
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: rgb(25, 25, 25);
                border: none;
            }
        """)
        
        # Скрываем/удаляем старый graphicsView
        graphics_view.hide()
        graphics_view.setParent(None)  # Освобождаем, но нужно ли это?
        graphics_view.deleteLater()  # Удаляем позже (Qt best practice)
        # else:
        #     print("graphicsView не найден в UI!")
    
    def add_plot_data(self):
        """
            Добавление данных на график
        """
        if hasattr(self, 'plot_graph'):
            time = [i for i in range(40)]
            self.plot_graph.addLegend(offset=(10, 10))  # offset — отступ от края

            #Тестовые данные для 1 графика
            pen_1= pg.mkPen(color=(255, 0, 0), width=2)  # Красная линия
            temperature = [30, 32, 34, 32, 30, 31, 29, 32, 35, 45, 30, 32, 34, 32, 30, 31, 29, 32, 35, 45, 30, 32, 34, 
                           32, 30, 31, 29, 32, 35, 45, 30, 32, 34, 32, 30, 31, 29, 32, 35, 45]
            self.plot_graph.plot(time, temperature, pen=pen_1, name = "стоковое потребление")

            #Тестовые данные для 2 графика
            pen_2 = pg.mkPen(color=(0, 0, 255), width=2)  # Синяя линия
            pressure = [30, 32, 20, 32, 30, 31, 30, 32, 35, 45, 30, 20, 34, 32, 30, 31, 29, 32, 35, 45, 30, 32, 34, 
                           32, 30, 31, 29, 32, 37, 36, 32, 40, 38, 31, 30, 31, 29, 32, 35, 45]
            self.plot_graph.plot(time, pressure, pen=pen_2, name = "потребление")

            # self.plot_graph.addLegend(offset=(10, 10))  # отступ от края

            # Настройки осей (под тёмную тему)
            self.plot_graph.setLabel('left', 'КГ', color='white')
            self.plot_graph.setLabel('bottom', 'Дни', color='white')
            self.plot_graph.showGrid(x=True, y=True, alpha=0.2)  # Сетка полупрозрачная
            self.plot_graph.getAxis('left').setTextPen('white')  # Цвет текста осей
            self.plot_graph.getAxis('bottom').setTextPen('white')
            self.plot_graph.getAxis('left').setTickPen('white')
            self.plot_graph.getAxis('bottom').setTickPen('white')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()  # Теперь MyWindow — это QMainWindow с загруженным UI
    window.show()
    sys.exit(app.exec())
