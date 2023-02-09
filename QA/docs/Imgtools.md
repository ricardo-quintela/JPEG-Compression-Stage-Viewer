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
  
>Creates a linear segment colormap with the given RGB color values  
>the colormap will be named with the given name  
  
**Arguments:**  
  
```
first_color (Tuple[float, float, float]): the first color  
second_color (Tuple[float, float, float]): the final color  
name (str): the name of the colormap  
rgb_quantization (int, optional): the RGB quantization levels. Defaults to 256.  
```  
**Returns:**  
  
```
LinearSegmentedColormap: A LinearSegmentedColormap object or None if an error occurs
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
  
>Reads a bmp file  
  
**Arguments:**  
  
```
path (str): the path to the bmp file  
```  
**Returns:**  
  
```
ndarray: an array with the image pixel values in RGB format
or None if the file is invalid or an error occurs
```  
  


  ---

  

  ---

  

  ---

  