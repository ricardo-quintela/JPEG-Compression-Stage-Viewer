# The Imgtools package


  
---
---
  ## create\_colormap
---  
  
**Signature:**  
  
```
create_colormap(        first_color: Tuple[float, float, float],        second_color: Tuple[float, float, float],        name:str,        rgb_quantization: int = 256,    ) -> LinearSegmentedColormap
```  
**Description:**  
  
>Cria um colorido de segmento linear com os valores de cores RGB fornecidos  
>o mapa de cor será nomeado com o nome dado  
  
**Arguments:**  
  
```
first_color (Tuple[float, float, float]): a primeira cor  
second_color (Tuple[float, float, float]): a cor final  
name (str): o nome do colorido  
rgb_quantization (int, optional): os níveis de quantização de RGB. Default a 256.  
```  
**Returns:**  
  
```
LinearSegmentedColormap: Um objeto LinearSegmentedColormap ou None se ocorrer um erro
```  
  


  ---

  

  
---
---
  ## add\_padding
---  
  
**Signature:**  
  
```
add_padding(img: ndarray, min_size: int)
```  
**Description:**  
  
>Adiciona preenchimento à imagem para complementar a falta de linhas/colunaspara ajudar o codec JPEG na compressão  
  
**Arguments:**  
  
```
img (ndarray): a matriz da imagem  
min_size (int): o tamanho mínimo de linhas/colunas necessários para concluir  
```  
**Returns:**  
  
```
Tuple[ndarray, int, int]: a imagem estendida e a linha antiga e o número da coluna
```  
  


  ---

  

  
---
---
  ## read\_bmp
---  
  
**Signature:**  
  
```
read_bmp(path: str) -> ndarray
```  
**Description:**  
  
>Lê um arquivo BMP  
  
**Arguments:**  
  
```
path (str): O caminho para o arquivo BMP  
```  
**Returns:**  
  
```
ndarray: Uma matriz com os valores de pixel de imagem em formato RGB
ou None se o arquivo for inválido ou ocorrer um erro
```  
  


  ---

  

  ---

  

  ---

  