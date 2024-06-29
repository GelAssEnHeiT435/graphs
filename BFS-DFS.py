import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import os

class graph:
   def __init__(self):
      self.nodes = None # список вершин
      self.graph_matrix = None # исходная матрица смежности

      self.__dfs_matrix = np.array([]) # матрица смежности графа после поиска в глубину
      self.__bfs_matrix = np.array([]) # матрица смежности графа после поиска в ширину
      self.__visited = np.array([]) # список посещенных вершин (приватно)
      self.__queue = np.array([]) # список очереди вершин (приватно)

   # метод чтения структуры графа из csv-файла
   def loadAdjMatrix_csv(self, path):
      data = pd.read_csv(path)

      # разбиваем данные на список вершин и матрицу смежности
      self.nodes = data.columns.to_numpy()
      self.graph_matrix = data.to_numpy()

      # инициализируем конечные матрицы смежности размерности исходного графа
      self.__dfs_matrix = self.nullMatrix()
      self.__bfs_matrix = self.nullMatrix()

   def __dfs_method(self, node):
      if node not in self.__visited: # если вершина не была посещена, то добавляем и анализируем ее
         self.__visited = np.append(self.__visited, node)

         for i in range(len(self.nodes)): # смотрим все вершины, с которыми она смежна и которых нет в списке посещенных
            if (self.graph_matrix[int(node) - 1][i] == 1) and (str(i + 1) not in self.__visited): # если такая есть, то отмечаем смежность (учитывается ориентированность ребра)

               self.__dfs_matrix[int(node) - 1][i] += 1

               if self.graph_matrix[int(node) - 1][i] == self.graph_matrix[i][int(node) - 1]:
                  self.__dfs_matrix[i][int(node) - 1] += 1

               self.__dfs_method(str(i + 1)) # рекурсия до последнего не отмеченного ребра

   def __bfs_method(self, node):
      self.__visited = np.append(self.__visited, node) # список посещенных вершин
      self.__queue = np.append(self.__queue, node) # список очереди
    
      while len(self.__queue): # пока очередь не пуста
         vis_node = self.__queue[0] # отмечаем вершину, по смежным вершинам которой будем идти
         self.__queue = np.delete(self.__queue, 0)
         
         for i in range(len(self.nodes)):
            if (self.graph_matrix[int(vis_node) - 1][i] == 1) and (str(i + 1) not in self.__visited): # если не посещена и смежна, то помещаем в очередь и помечаем
               self.__queue = np.append(self.__queue, str(i + 1))
               self.__visited = np.append(self.__visited, str(i + 1))

               self.__bfs_matrix[int(vis_node) - 1][i] += 1

               if self.graph_matrix[int(vis_node) - 1][i] == self.graph_matrix[i][int(vis_node) - 1]:
                  self.__bfs_matrix[i][int(vis_node) - 1] += 1

   def dfs(self, node):
      self.__dfs_method(node) # вызов алгоритма 
      self.__checkConnect() # проверка связности

      # очистка данных
      self.__visited = np.array([])
      matrix = self.__dfs_matrix
      self.__dfs_matrix = self.nullMatrix()

      return matrix

   def bfs(self, node):
      self.__bfs_method(node) # вызов алгоритма
      self.__checkConnect() # проверка связности

      # очистка данных
      self.__visited = np.array([])
      self.__queue = np.array([])
      matrix = self.__bfs_matrix
      self.__bfs_matrix = self.nullMatrix()

      return matrix

   def __checkConnect(self): # проверка связности. Если прошелся по всем вершинам, то граф связный
      for i in self.nodes:
         if i not in self.__visited:
            raise Exception("Отсутствует связность графа!")
   
   def nullMatrix(self): # генерация нулевой матрицы
      matrix = np.array([])

      for i in range(len(self.nodes) ** 2):
         matrix = np.append(matrix, 0)

      matrix = matrix.reshape(len(self.nodes), len(self.nodes))
      return matrix
      
   def drawGraph(self, matrix): # отрисовка исходного и итогового графов
      OrigG = nx.from_numpy_array(self.graph_matrix, create_using = nx.DiGraph) # граф по матрице смежности
      mapping = {i: self.nodes[i] for i in range(len(self.nodes))} # устанавливаем вершинам их обозначения
      OrigG = nx.relabel_nodes(OrigG, mapping)

      nx.draw(OrigG, with_labels=True) # отрисовка
      plt.show()

      G = nx.from_numpy_array(matrix, create_using=nx.DiGraph)
      mapping = {i: self.nodes[i] for i in range(len(self.nodes))}
      G = nx.relabel_nodes(G, mapping)

      nx.draw(G, with_labels=True)
      plt.show()
      
def interface():
   exit = False

   while not exit:
      Obj = graph()
      
      try:
         path = input("Введите имя файла: ")
         Obj.loadAdjMatrix_csv(path)

      except FileNotFoundError:
         print(f"[ERROR] No such file or directory: {path}")
         continue

      while True:
         print("Функции:\n1) Поиск в глубину(dfs);\t\t2) Поиск в ширину(bfs);\t\t 3) Выход(exit).")
         mode = input("Укажите алгоритм, который вы хотите применить: ")

         if mode == 'dfs':
            while True:
               print(f"В данном файле были обнаружены следующие вершины: {Obj.nodes}")
               node = str(input("Укажите стартовую вершину: "))
               matrix = None

               if node not in Obj.nodes:
                  print("[ERROR] Нет такой вершины")
                  os.system('pause')
                  os.system('cls')
                  continue
               else:
                  matrix = Obj.dfs(node)
                  print(matrix)
               
               assent = input("Желаете отобразить результаты? (y/n): ")

               if assent == 'y':
                  Obj.drawGraph(matrix)
               
               os.system('pause')
               os.system('cls')
               break

         elif mode == 'bfs':
            while True:
               print(f"В данном файле были обнаружены следующие вершины: {Obj.nodes}")
               node = str(input("Укажите стартовую вершину: "))
               matrix = None

               if node not in Obj.nodes:
                  print("[ERROR] Нет такой вершины")
                  os.system('pause')
                  os.system('cls')
                  continue
               else:
                  matrix = Obj.bfs(node)
                  print(matrix)
               
               assent = input("Желаете отобразить результаты? (y/n): ")

               if assent == 'y':
                  Obj.drawGraph(matrix)
               
               os.system('pause')
               os.system('cls')
               break

         elif mode == 'exit':
            exit = True
            break

         else:
            print("[ERROR] Нет такого алгоритма")

            os.system('pause')
            os.system('cls')
            continue
         
interface()