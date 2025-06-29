# Heatmap Object Tracking API

Este projeto implementa uma API para geração de **mapas de calor** com base em detecções de objetos extraídas de arquivos JSON no formato `deepstream-msg`.


## O que o código faz

- Lê um arquivo `sample.json` contendo detecções de objetos no formato:
  ```
  frame_id|x_min|y_min|x_max|y_max|label|region
  ```
- Filtra as detecções por tipo de objeto (ex: `person`)
- Calcula os centróides dos bounding boxes
- Gera uma matriz de densidade (`heatmap`) suavizada com filtro gaussiano
- Sobrepõe o heatmap à imagem `base_image.png`
- Salva o resultado como `static/output.png`
- Exposto via API com FastAPI


## ▶Como executar

### Requisitos: Docker + Docker Compose

```bash
docker-compose build
docker-compose up -d
```

## Endpoints

- `GET /generate?object_filter=person`  
  Gera e retorna a imagem `static/output.png` com o mapa de calor

- `GET /list_objects`  
  Lista os tipos de objeto disponíveis no arquivo `sample.json`

Com sobreposição térmica (`jet colormap`) mostrando a frequência de presença do objeto escolhido.