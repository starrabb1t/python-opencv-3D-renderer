import numpy as np
import cv2

height = 480
width = 640

Gx = 0
Gy = 0
Gz = 0

RotX = 0
RotY = 0
RotZ = 0

Cx = 0
Cy = 0
Cz = 5

f = 0.1
Px = 0.06
Py = 0.048
offsetX = width / 2
offsetY = height / 2
skew = 0

def getCamera(verts):

    offset = np.array([[1, 0, 0, offsetX],
                       [0, -1, 0, offsetY],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])

    P = np.array([[(f * width) / (2 * Px), skew, 0, 0],
                  [0, (f * height) / (2 * Py), 0, 0],
                  [0, 0, -1, 0],
                  [0, 0, 0, 1]])

    C = np.array([[1, 0, 0, -Cx],
                  [0, 1, 0, -Cy],
                  [0, 0, 1, -Cz],
                  [0, 0, 0, 1]])

    Rx = np.array([[1, 0, 0, 0],
                   [0, np.cos(RotX), - np.sin(RotX), 0],
                   [0, np.sin(RotX), np.cos(RotX), 0],
                   [0, 0, 0, 1]])

    Ry = np.array([[np.cos(RotY), 0, np.sin(RotY), 0],
                   [0, 1, 0, 0],
                   [- np.sin(RotY), 0, np.cos(RotY), 0],
                   [0, 0, 0, 1]])

    Rz = np.array([[np.cos(RotZ), - np.sin(RotZ), 0, 0],
                   [np.sin(RotZ), np.cos(RotZ), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])

    G = np.array([[1, 0, 0, -Gx],
                  [0, 1, 0, -Gy],
                  [0, 0, 1, -Gz],
                  [0, 0, 0, 1]])

    x = [0] * len(verts)

    for i in range(len(verts)):
        x[i] = np.matmul(G, np.array(verts[i]))
        x[i] = np.matmul(Rz, x[i])
        x[i] = np.matmul(Ry, x[i])
        x[i] = np.matmul(Rx, x[i])
        x[i] = np.matmul(C, x[i])
        x[i] = np.matmul(P, x[i])

        N = np.array([[1 / x[i][2], 0, 0, 0],
                      [0, 1 / x[i][2], 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

        x[i] = np.matmul(N, x[i])
        x[i] = np.matmul(offset, x[i])

    return x


def render(camera, edges):
    canvas = 255 * np.ones((height, width, 3), dtype='uint8')

    for edge in edges:
        cv2.line(canvas,
                 (int(camera[edge[0]][0]), int(camera[edge[0]][1])),
                 (int(camera[edge[1]][0]), int(camera[edge[1]][1])),
                 color=(0, 0, 0),
                 thickness=2)

    return canvas
