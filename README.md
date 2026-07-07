# Map Tiles

## Downloading Map Tiles

The script `script.py` downloads the tiles from the following MapServer:

```python
BASE_URL = https://services.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer
```

You can adjust the zoom level (max zoom level is 23, so the max it can go is `range(0, 24)`):

```python
ZOOM_LEVELS = range(0, 15)
```

Run `script.py` in Google Colab (or any other Python environment).

Run the following command to zip the output folder:

```bash
!zip -r tiles.zip /content/tiles
```

Download, then unzip the folder in the current project root `/tiles`.

## Serving Map Tiles

Run the following command:

```
docker compose up -d
```
