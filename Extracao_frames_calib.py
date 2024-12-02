# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 19:16:39 2024

@author: naiar
"""
# Usei para extrair os frames especificos com o calibrador nivelado nos pontos
import cv2
import sys
import os

# Caminhos para os vídeos
video_path_cam1 = "C:/Users/naiar/OneDrive/Documentos/VIDA_PROFISSIONAL/MESTRADO_USP/AULAS/PYTHON/TRABALHO_FINAL/CAM_D/CAM_2D.MP4"
video_path_cam2 = "C:/Users/naiar/OneDrive/Documentos/VIDA_PROFISSIONAL/MESTRADO_USP/AULAS/PYTHON/TRABALHO_FINAL/CAM_E/CAM_2E.MP4"

# Criar subpastas para os frames de cada câmera
output_dir_cam1 = "Frames_Cam1"
output_dir_cam2 = "Frames_Cam2"

os.makedirs(output_dir_cam1, exist_ok=True)
os.makedirs(output_dir_cam2, exist_ok=True)

# Abrir os dois vídeos
cap_cam1 = cv2.VideoCapture(video_path_cam1)
cap_cam2 = cv2.VideoCapture(video_path_cam2)

# Verificar se os vídeos foram abertos corretamente
if not cap_cam1.isOpened():
    print("Erro ao abrir o vídeo da câmera 1.")
    sys.exit()

if not cap_cam2.isOpened():
    print("Erro ao abrir o vídeo da câmera 2.")
    sys.exit()

# Definir os tempos desejados (em segundos)
tempos_desejados = [41, 67, 88, 108, 134, 153, 166, 180, 205, 225, 241, 263]

# Obter o FPS dos dois vídeos (assumindo que ambos têm o mesmo FPS)
fps_cam1 = cap_cam1.get(cv2.CAP_PROP_FPS)
fps_cam2 = cap_cam2.get(cv2.CAP_PROP_FPS)

if fps_cam1 != fps_cam2:
    print("Os vídeos têm FPS diferentes, verifique os arquivos.")
    sys.exit()

fps = fps_cam1  # Usar o mesmo FPS para ambas as câmeras

# Loop para percorrer os tempos desejados
for tempo in tempos_desejados:
    # Calcular o número do frame correspondente ao tempo desejado
    frame_desejado = int(fps * tempo)

    # Ir para o frame correspondente na câmera 1
    cap_cam1.set(cv2.CAP_PROP_POS_FRAMES, frame_desejado)
    ret1, frame_cam1 = cap_cam1.read()

    # Ir para o frame correspondente na câmera 2
    cap_cam2.set(cv2.CAP_PROP_POS_FRAMES, frame_desejado)
    ret2, frame_cam2 = cap_cam2.read()

    # Verificar se os frames foram lidos corretamente
    if ret1 and ret2:
        # Salvar os frames nas pastas correspondentes
        cv2.imwrite(f"{output_dir_cam1}/frame_cam1_{tempo}s.png", frame_cam1)
        cv2.imwrite(f"{output_dir_cam2}/frame_cam2_{tempo}s.png", frame_cam2)
        print(f"Frames aos {tempo}s salvos: '{output_dir_cam1}/frame_cam1_{tempo}s.png' e '{output_dir_cam2}/frame_cam2_{tempo}s.png'.")
    else:
        print(f"Erro ao ler os frames aos {tempo}s.")

# Fechar as capturas de vídeo
cap_cam1.release()
cap_cam2.release()

# Fechar todas as janelas do OpenCV
cv2.destroyAllWindows()
