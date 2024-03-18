diccionario_f26 = {
    (1, 0, 0): 'a',
    (1, 1, 0): 'b',
    (0, 1, 0): 'c',
    (-1, 1, 0): 'd',
    (-1, 0, 0): 'e',
    (-1, -1, 0): 'f',
    (0, -1, 0): 'g',
    (1, -1, 0): 'h',
    (1, 0, 1): 'i',
    (1, 1, 1): 'j',
    (0, 1, 1): 'k',
    (-1, 1, 1): 'l',
    (-1, 0, 1): 'm',
    (-1, -1, 1): 'n',
    (0, -1, 1): 'o',
    (1, -1, 1): 'p',
    (1, 0, -1): 'q',
    (1, 1, -1): 'r',
    (0, 1, -1): 's',
    (-1, 1, -1): 't',
    (-1, 0, -1): 'u',
    (-1, -1, -1): 'v',
    (0, -1, -1): 'w',
    (1, -1, -1): 'x',
    (0, 0, 1): 'y',
    (0, 0, -1): 'z',
}
RAIZ_2 = 1.4142
RAIZ_3 = 1.7321
DOS1 = 2.2361
DOS2 = 2.4495
UNO = 1.0
diccionario_3drc = {
    # Grupo 1 
    (0, RAIZ_2, tuple([0,0,0])): 'a',
    (45, RAIZ_3, tuple([0,0,1])): 'b',
    (90, RAIZ_2, tuple([0,0,1])): 'c',
    (135, RAIZ_3, tuple([0,0,1])): 'd',
    (180, RAIZ_2, tuple([0,0,0])): 'e',
    (135, RAIZ_3, tuple([0,0,-1])): 'f',
    (90, RAIZ_2, tuple([0,0,-1])): 'g',
    (45, RAIZ_3, tuple([0,0,-1])): 'h',
    (45, DOS1, tuple([0,-1,0])): 'i',
    (54, DOS2, tuple([0,-1,1])): 'j',
    (90, DOS1, tuple([0,-1,1])): 'k',
    (125, DOS2, tuple([0,-1,1])): 'l',
    (135, DOS1, tuple([0,-1,0])): 'm',
    (125, DOS2, tuple([0,-1,-1])): 'n',
    (90, DOS1, tuple([0,-1,-1])): 'o',
    (54, DOS2, tuple([0,-1,-1])): 'p',
    (45, UNO, tuple([0,-1,-1])): 'q',
    (54, RAIZ_2, tuple([0,1,1])): 'r',
    (90, UNO, tuple([0,1,1])): 's',
    (125, RAIZ_2, tuple([0,1,1])): 't',
    (135, UNO, tuple([0,1,0])): 'u',
    (125, RAIZ_2, tuple([0,1,-1])): 'v',
    (90, UNO, tuple([0,1,-1])): 'w',
    (54, RAIZ_2, tuple([0,1,-1])): 'x',
    # Grupo 2
    (45, RAIZ_2, tuple([0,1,0])): 'a',
    (60, RAIZ_3, tuple([-1,1,1])): 'b',
    (90, RAIZ_2, tuple([-1,0,1])): 'c',
    (120, RAIZ_3, tuple([-1,1,1])): 'd',
    (135, RAIZ_2, tuple([0,-1,0])): 'e',
    (120, RAIZ_3, tuple([1,-1,-1])): 'f',
    (90, RAIZ_2, tuple([1,0,-1])): 'g',
    (60, RAIZ_3, tuple([1,1,-1])): 'h',
    (0, DOS1, tuple([0,0,0])): 'i',
    (35, DOS2, tuple([-1,0,1])): 'j',
    (60, DOS1, tuple([-1,-1,1])): 'k',
    (90, DOS2, tuple([-1,-2,1])): 'l',
    (90, DOS1, tuple([0,-2,0])): 'm',
    (90, DOS2, tuple([1,-2,-1])): 'n',
    (60, DOS1, tuple([1,-1,-1])): 'o',
    (35, DOS2, tuple([1,0,-1])): 'p',
    (90, UNO, tuple([0,2,0])): 'q',
    (90, RAIZ_2, tuple([-1,2,1])): 'r',
    (120, UNO, tuple([-1,1,1])): 's',
    (145, RAIZ_2, tuple([-1,0,1])): 't',
    (180, UNO, tuple([0,0,0])): 'u',
    (145, RAIZ_2, tuple([1,0,-1])): 'v',
    (120, UNO, tuple([1,1,-1])): 'w',
    (90, RAIZ_2, tuple([1,2,-1])): 'x',
    # Grupo 3
    (45, RAIZ_2, tuple([0,-1,0])): 'a',
    (60, RAIZ_3, tuple([1,-1,1])): 'b',
    (90, RAIZ_2, tuple([1,0,1])): 'c',
    (120, RAIZ_3, tuple([1,1,1])): 'd',
    (135, RAIZ_2, tuple([0,1,0])): 'e',
    (120, RAIZ_3, tuple([-1,1,-1])): 'f',
    (90, RAIZ_2, tuple([-1,0,-1])): 'g',
    (60, RAIZ_3, tuple([-1,-1,-1])): 'h',
    (90, DOS1, tuple([0,-2,0])): 'i',
    (90, DOS2, tuple([1,-2,1])): 'j',
    (120, DOS1, tuple([1,-1,1])): 'k',
    (145, DOS2, tuple([1,0,1])): 'l',
    (180, DOS1, tuple([0,0,0])): 'm',
    (145, DOS2, tuple([-1,0,-1])): 'n',
    (120, DOS1, tuple([-1,-1,-1])): 'o',
    (90, DOS2, tuple([-1,-2,-1])): 'p',
    (0, UNO, tuple([0,0,0])): 'q',
    (35, RAIZ_2, tuple([1,0,1])): 'r',
    (60, UNO, tuple([1,1,1])): 's',
    (90, RAIZ_2, tuple([1,2,1])): 't',
    (90, UNO, tuple([0,2,0])): 'u',
    (90, RAIZ_2, tuple([-1,2,-1])): 'v',
    (60, UNO, tuple([-1,1,-1])): 'w',
    (35, RAIZ_2, tuple([-1,0,-1])): 'x',
    (0, 1.0, tuple([0,0,0])): 'y',
}