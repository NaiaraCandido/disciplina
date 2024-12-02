# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 20:50:11 2024

@author: naiar
"""

#usei para extrair as coordenadas 2d marcando os pontos manualmente
import cv2
import csv
import os
import re

# Função para extrair o número completo do nome do arquivo
def get_number_from_filename(filename):
    # Usar expressão regular para encontrar números no nome do arquivo
    numbers = re.findall(r'\d+', filename)  # Encontra todos os números no nome
    return [int(num) for num in numbers]  # Retorna uma lista de inteiros (caso haja mais de um número)

# Caminho para as pastas dos frames
frames_dir_cam1 = "C:/Users/naiar/OneDrive/Documentos/VIDA_PROFISSIONAL/MESTRADO_USP/AULAS/PYTHON/TRABALHO_FINAL/Frames_Cam1"  # Pasta dos frames da Câmera 1
frames_dir_cam2 = "C:/Users/naiar/OneDrive/Documentos/VIDA_PROFISSIONAL/MESTRADO_USP/AULAS/PYTHON/TRABALHO_FINAL/Frames_Cam2"  # Pasta dos frames da Câmera 2

# Listar os arquivos de cada câmera e ordenar numericamente
frames_cam1 = sorted(os.listdir(frames_dir_cam1), key=lambda x: get_number_from_filename(x))
frames_cam2 = sorted(os.listdir(frames_dir_cam2), key=lambda x: get_number_from_filename(x))

# Exibir os arquivos ordenados de cada câmera
print("Frames Camera 1 (ordenados):")
for frame in frames_cam1:
    print(frame)

print("\nFrames Camera 2 (ordenados):")
for frame in frames_cam2:
    print(frame)
    
# Arquivos CSV para salvar as coordenadas
output_csv_cam1 = "coordenadas_cam1.csv"  # Coordenadas para a Câmera 1
output_csv_cam2 = "coordenadas_cam2.csv"  # Coordenadas para a Câmera 2

# Lista para armazenar as coordenadas de cada câmera
coordenadas_cam1 = []
coordenadas_cam2 = []

# Função de callback para registrar cliques
def clique(event, x, y, flags, param):
    global frame_display  # Usamos a variável frame_display para modificar o frame atual
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordenada clicada: ({x}, {y})")
        
        # Desenhando um círculo no ponto clicado para marcar visualmente
        cv2.circle(frame_display, (x, y), 5, (0, 0, 255), -1)  # Bolinha vermelha de raio 5
        
        # Adiciona a coordenada clicada na lista
        if param == 'cam1':
            coordenadas_cam1.append((param, x, y))
        elif param == 'cam2':
            coordenadas_cam2.append((param, x, y))

# Função para marcar os pontos em cada frame
def marcar_pontos(frames, frames_dir, camera_label):
    for frame_name in frames:
        frame_path = os.path.join(frames_dir, frame_name)
        frame = cv2.imread(frame_path)

        if frame is None:
            print(f"Erro ao carregar o frame: {frame_name}")
            continue

        global frame_display
        frame_display = frame.copy()  # Criando uma cópia do frame para edição visual

        # Exibindo a imagem e esperando o clique do mouse
        cv2.imshow(f"Clique nos pontos - {camera_label}", frame_display)
        cv2.setMouseCallback(f"Clique nos pontos - {camera_label}", clique, param=camera_label)

        print(f"Marque os pontos no frame: {frame_name} da {camera_label}")
        print("Pressione 'n' para o próximo frame quando terminar.")

        while True:
            # Exibe o frame com a bolinha desenhada
            cv2.imshow(f"Clique nos pontos - {camera_label}", frame_display)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('n'):  # Pressionar 'n' para ir para o próximo frame
                break

    cv2.destroyAllWindows()

# Marcar pontos para as duas câmeras
print("Iniciando marcação de pontos para a Câmera 1...")
marcar_pontos(frames_cam1, frames_dir_cam1, 'cam1')
print("Iniciando marcação de pontos para a Câmera 2...")
marcar_pontos(frames_cam2, frames_dir_cam2, 'cam2')

# Salvar as coordenadas das câmeras em arquivos CSV
with open(output_csv_cam1, mode='w', newline='') as csvfile_cam1:
    writer = csv.writer(csvfile_cam1)
    writer.writerow(['frame', 'x', 'y'])  # Cabeçalhos para Câmera 1
    writer.writerows(coordenadas_cam1)

with open(output_csv_cam2, mode='w', newline='') as csvfile_cam2:
    writer = csv.writer(csvfile_cam2)
    writer.writerow(['frame', 'x', 'y'])  # Cabeçalhos para Câmera 2
    writer.writerows(coordenadas_cam2)

print(f"Coordenadas da Câmera 1 salvas em: {output_csv_cam1}")
print(f"Coordenadas da Câmera 2 salvas em: {output_csv_cam2}")
