'''
Atividade Pontuada 01
Autor: João Victor Guimarães Florêncio
Disciplina: Processamento de Imagens - T02 - 2022.2
Professor: Dr. Leonardo Nogueira Matos

Enunciado:Elabore um programa em Python 3 para realizar o pré-processamento de imagens de caracteres
óticos tipográficos a fim de que sejam utilizados por um programa para reconhecimento de textos -
pytesseract .
O pré-processamento consiste em identificar parâmetros apropriados para ajuste de brilho e contraste
a serem aplicados a fim de maximizar o desempenho do OCR, que deve possuir acurácia superior a
90% em uma base de teste.
Serão utilizados a base de dados fornecida pelo professor, onde constam 100 imagens 
'''

# Importando bibliotecas
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import pytesseract
from skimage.filters import threshold_otsu


# Criando uma lista vazia para armazenar os nomes dos arquivos
nomes_arquivos = []
imagens = []
# Adicionando os nomes dos arquivos na lista usando um loop for
for i in range(1, 101):
    
    # Criando o nome do arquivo
    nome_arquivo = "img" + str(i).zfill(4) + ".png"
    # Adicionando o nome do arquivo na lista
    nomes_arquivos.append(nome_arquivo)
    # Lendo a imagem
    imagem = (io.imread(nome_arquivo, as_gray=True) * 255).astype('uint8')
    # Adicionando a imagem na lista
    imagens.append(imagem)

imagens_cortadas = []

for imagem in imagens:
    # Obtendo as dimensões da imagem
    l,c = imagem.shape
    # Obtendo as linhas e colunas da imagem
    h = imagem[l//2,:]
    v = imagem[:,c//2]
    # Encontrando o valor em que a imagem deixa de ser preta e onde ela volta a ser preta (inicio e fim) e armazenando em variáveis diferentes para fazer o corte
    inicio_h = np.where(h>5)[0][0]
    fim_h = np.where(h>5)[0][-1]
    inicio_v = np.where(v>5)[0][0]
    fim_v = np.where(v>5)[0][-1]
    # Fazendo o corte na imagem
    imagem = imagem[inicio_v:fim_v,inicio_h:fim_h]
    # Adicionando a imagem cortada na lista
    imagens_cortadas.append(imagem)

stretch = []
for imagem in range(len(imagens_cortadas)):
    imagem_ = imagens_cortadas[imagem]
    imagem_ = imagem_.astype(int)*2
    #Stretch do histograma
    #Ao inves de tomar os limites superior e inferior, como maximo e minimo, eu tomo 5% e 95% do histograma
    amin = np.percentile(imagem_, 5)
    amax = np.percentile(imagem_, 95)
    imagem_[imagem_ < amin] = amin
    imagem_[imagem_ > amax] = amax
    imagem_ = imagem_ - imagem_.min()
    imagem_ = (imagem_ * 255) / imagem_.max()
    imagem_ = imagem_.astype('uint8')
    stretch.append(imagem_)


binarizadas = []
for i in range(len(stretch)):
    limiar = threshold_otsu(stretch[i])
    binarizada = stretch[i] > limiar
    #convertendo para uint8
    binarizada = binarizada.astype('uint8')*255
    binarizadas.append(binarizada)


textos = []
for i in range(len(binarizadas)):
    texto = pytesseract.image_to_string(binarizadas[i])
    textos.append(texto)

#Mostrando as imagens e os textos obtidos 
for i in range(len(binarizadas)):
    plt.imshow(binarizadas[i], cmap='gray')
    plt.title("Texto obtido: " + textos[i])
    plt.show()
        