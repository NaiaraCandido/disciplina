# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 23:41:17 2024

@author: naiar
"""
import pandas as pd
import numpy as np
from numpy.linalg import inv
import os
from time import sleep
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Caminhos para os arquivos CSV e txt
csv_file_camera1 = 'C:/Users/naiar/OneDrive/Documentos/VIDA_PROFISSIONAL/MESTRADO_USP/AULAS/PYTHON/TRABALHO_FINAL/coordenadas_cam1.csv'
csv_file_camera2 = 'C:/Users/naiar/OneDrive/Documentos/VIDA_PROFISSIONAL/MESTRADO_USP/AULAS/PYTHON/TRABALHO_FINAL/coordenadas_cam2.csv'

coordenadas_2d_camera1 = pd.read_csv(csv_file_camera1).iloc[:, 1:].values  # Ignorar a primeira coluna se for índice
coordenadas_2d_camera2 = pd.read_csv(csv_file_camera2).iloc[:, 1:].values

# Garantir que os dados sejam numéricos
coordenadas_2d_camera1 = coordenadas_2d_camera1.astype(float)
coordenadas_2d_camera2 = coordenadas_2d_camera2.astype(float)

# Combinar os dados 2D das câmeras em um único array
cp2d = np.hstack([coordenadas_2d_camera1, coordenadas_2d_camera2])

# Carregar as coordenadas 3D do bastão
coordenadas_3d_bastao_path = 'C:/Users/naiar/OneDrive/Documentos/VIDA_PROFISSIONAL/MESTRADO_USP/AULAS/PYTHON/TRABALHO_FINAL/Coordenadas.txt'
coordenadas_3d_bastao = np.loadtxt(coordenadas_3d_bastao_path, delimiter=',')

# Verificar se o número de pontos 2D e 3D é consistente
n_pontos_3d = coordenadas_3d_bastao.shape[0]
n_pontos_2d = cp2d.shape[0]

if n_pontos_3d != n_pontos_2d:
    raise ValueError("O número de pontos 2D e 3D não é o mesmo. Verifique os arquivos!")

# Função de calibração DLT
def dlt_calib(cp3d, cp2d):
    cp3d = np.asarray(cp3d)
    if cp3d.shape[1] > 3:  # Remover índice se presente
        cp3d = cp3d[:, 1:]

    m = cp3d.shape[0]
    M = np.zeros((m * 2, 11))
    N = np.zeros((m * 2, 1))

    for i in range(m):
        x, y = cp2d[i, :2]
        X, Y, Z = cp3d[i, :3]

        M[i * 2, :] = [X, Y, Z, 1, 0, 0, 0, 0, -x * X, -x * Y, -x * Z]
        M[i * 2 + 1, :] = [0, 0, 0, 0, X, Y, Z, 1, -y * X, -y * Y, -y * Z]
        N[i * 2, 0] = x
        N[i * 2 + 1, 0] = y

    Mt = M.T
    M1 = inv(Mt @ M)
    MN = Mt @ N
    DLT = (M1 @ MN).flatten()

    return DLT

# Calcular os parâmetros DLT
dlt_parameters = dlt_calib(coordenadas_3d_bastao, cp2d)

# Exibir os parâmetros calculados
print("Parâmetros DLT calculados:")
print(dlt_parameters)

# Plotar os pontos 3D reconstruídos
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotar os pontos do bastão calibrador
ax.scatter(coordenadas_3d_bastao[:, 0], 
           coordenadas_3d_bastao[:, 1], 
           coordenadas_3d_bastao[:, 2], 
           c='r', label='Pontos 3D Reconstruídos', marker='o')

# Configurações do gráfico
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Reconstrução 3D - Pontos do Bastão Calibrador')
ax.legend()

# Mostrar o gráfico
plt.show()