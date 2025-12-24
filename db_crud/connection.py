import pyodbc
import os
from dotenv import load_dotenv
from typing import Optional, Tuple
import logging

# Загружаем переменные окружения
load_dotenv()

class DBConn:
    def __init__(self):
        self.connection_db: Optional[pyodbc.Connection] = None
        self.cursor_db: Optional[pyodbc.Cursor] = None
        self.logger = self._setup_logger()
        self.connect()
    
    def _setup_logger(self) -> logging.Logger:
        """Настройка логгера"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def _get_connection_string(self) -> str:
        """Получение строки подключения из .env"""
        try:
            # Чтение параметров из переменных окружения
            driver = os.getenv('DB_DRIVER', '{SQL Anywhere 17}')
            server = os.getenv('DB_SERVER', 'amos')
            database = os.getenv('DB_NAME', 'amos')
            port = os.getenv('DB_PORT', "2638")
            host = os.getenv('DB_HOST', 'localhost')
            username = os.getenv('DB_USERNAME', '')
            password = os.getenv('DB_PASSWORD', '')
            
            if not all([server, database]):
                raise ValueError("Не указаны обязательные параметры подключения")
            
            if username and password:
                # Аутентификация SQL Server
                conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};HOST={host};PORT={port};UID={username};PWD={password}'
            else:
                # Windows Authentication
                conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes'
            
            return conn_str
            
        except Exception as e:
            self.logger.error(f"Ошибка формирования строки подключения: {e}")
            raise
    
    def connect(self) -> Tuple[pyodbc.Connection, pyodbc.Cursor]:
        """Установка подключения к базе данных"""
        try:
            connection_string = self._get_connection_string()
            
            self.connection_db = pyodbc.connect(connection_string)
            self.cursor_db = self.connection_db.cursor()
            
            self.logger.info("Успешное подключение к базе данных")
            
            return self.connection_db, self.cursor_db
            
        except pyodbc.Error as e:
            self.logger.error(f"Ошибка подключения к базе данных: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка: {e}")
            raise
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Optional[list]:
        """Выполнение SQL запроса"""
        try:
            if params:
                self.cursor_db.execute(query, params)
            else:
                self.cursor_db.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return self.cursor_db.fetchall()
            else:
                self.connection_db.commit()
                return None
                
        except pyodbc.Error as e:
            self.logger.error(f"Ошибка выполнения запроса: {e}")
            self.connection_db.rollback()
            raise
    
    def close(self) -> None:
        """Закрытие подключения"""
        try:
            if self.cursor_db:
                self.cursor_db.close()
            if self.connection_db:
                self.connection_db.close()
            self.logger.info("Подключение к базе данных закрыто")
        except pyodbc.Error as e:
            self.logger.error(f"Ошибка при закрытии подключения: {e}")
    
    def __enter__(self):
        """Поддержка контекстного менеджера"""
        return self
    
    def __exit__(self):
        """Выход из контекстного менеджера"""
        self.close()
    
    def __del__(self):
        """Деструктор - автоматическое закрытие при удалении объекта"""
        self.close()

