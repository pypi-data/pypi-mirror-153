#!/usr/bin/env python
# coding: utf-8


import os
import folium
import webbrowser
import geopandas as gpd
from pathlib import Path
import py7zr
import importlib.resources
from open_geodata import geo, lyr
from folium import plugins


def list_datasets():
    data_pkg = importlib.resources.files(__package__)
    return [p.name for p in data_pkg.rglob('*') if p.suffix == '.7z']


def read_data(select_file):
    with py7zr.SevenZipFile(select_file, 'r') as archive:
        allfiles = archive.getnames()

        # Quero apenas um arquivo por gpkg
        if len(allfiles) == 1:
            for filename, bio in archive.read(allfiles).items():
                pass
        else:
            raise RuntimeError('.zip tem mais de um gpkg')
    return gpd.read_file(bio)


def limite():
    # Input
    root = Path(__file__).parent.joinpath('data/output/zips')
    gdf = read_data(root.joinpath('apa_corumbatai_limite.7z'))
    gdf = gdf.to_crs(epsg=4326)

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Limite APA',
        style_function=lambda x: {
            'fillColor': '#E1E1E1',
            'color': '#E1E1E1',
            'weight': 3,
            'fillOpacity': 0.0
        },
        highlight_function=lambda x: {
            'weight': 3
        },
        embed=False,
        zoom_on_click=False,
        control=True,
        show=True,
    )


def limite_zpa():
    # Input
    root = Path(__file__).parent.joinpath('data/output/zips')
    gdf = read_data(root.joinpath('apa_corumbatai_zpa.7z'))
    gdf = gdf.to_crs(epsg=4326)

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Zona de Proteção Aquífera (ZPA)',
        style_function=lambda x: {
            'fillColor': '#ff8080',
            'color': '#ff8080',
            'weight': 1,
            'fillOpacity': 0.5
        },
        highlight_function=lambda x: {
            'weight': 3
        },
        embed=False,
        zoom_on_click=False,
        control=True,
        show=False,
    )


def limite_zph():
    # Input
    root = Path(__file__).parent.joinpath('data/output/zips')
    gdf = read_data(root.joinpath('apa_corumbatai_zph.7z'))
    gdf = gdf.to_crs(epsg=4326)

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Zona de Proteção Hídrica (ZPH)',
        style_function=lambda x: {
            'fillColor': '#8080ff',
            'color': '#8080ff',
            'weight': 1,
            'fillOpacity': 0.5
        },
        highlight_function=lambda x: {
            'weight': 3
        },
        embed=False,
        zoom_on_click=False,
        control=True,
        show=False,
    )


def limite_zvs():
    # Input
    root = Path(__file__).parent.joinpath('data/output/zips')
    gdf = read_data(root.joinpath('apa_corumbatai_zvs.7z'))
    gdf = gdf.to_crs(epsg=4326)

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Zona de Vida Silvestre (ZVS)',
        style_function=lambda x: {
            'fillColor': '#009933',
            'color': '#009933',
            'weight': 1,
            'fillOpacity': 0.5
        },
        highlight_function=lambda x: {
            'weight': 3
        },
        embed=False,
        zoom_on_click=False,
        control=True,
        show=False,
    )


def limite_hidro_simples():
    # Input
    root = Path(__file__).parent.joinpath('data/output/zips')
    gdf = read_data(root.joinpath('apa_corumbatai_hidro_simples.7z'))
    gdf = gdf.to_crs(epsg=4326)

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Hidrografia - Simples',
        style_function=lambda x: {
            'fillColor': '#0099ff',
            'color': '#0099ff',
            'weight': 1,
            'fillOpacity': 0.5
        },
        highlight_function=lambda x: {
            'weight': 3
        },
        embed=False,
        zoom_on_click=False,
        control=True,
        show=False,
    )


def limite_hidro_dupla():
    # Input
    root = Path(__file__).parent.joinpath('data/output/zips')
    gdf = read_data(root.joinpath('apa_corumbatai_hidro_dupla.7z'))
    gdf = gdf.to_crs(epsg=4326)

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Hidrografia - Dupla',
        style_function=lambda x: {
            'fillColor': '#0099ff',
            'color': '#0099ff',
            'weight': 1,
            'fillOpacity': 0.5
        },
        highlight_function=lambda x: {
            'weight': 3
        },
        embed=False,
        zoom_on_click=False,
        control=True,
        show=False,
    )


def limite_hidro_nascente():
    # Input
    root = Path(__file__).parent.joinpath('data/output/zips')
    gdf = read_data(root.joinpath('apa_corumbatai_hidro_nascente.7z'))
    gdf = gdf.to_crs(epsg=4326)

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Hidrografia - Nascente',
        style_function=lambda x: {
            'fillColor': '#0099ff',
            'color': '#0099ff',
            'weight': 1,
            'fillOpacity': 0.5
        },
        highlight_function=lambda x: {
            'weight': 3
        },
        embed=False,
        zoom_on_click=False,
        control=True,
        show=False,
    )


def limite_hidro_lakes():
    # Input
    root = Path(__file__).parent.joinpath('data/output/zips')
    gdf = read_data(root.joinpath('apa_corumbatai_hidro_represa.7z'))
    gdf = gdf.to_crs(epsg=4326)

    # Layer
    return folium.features.GeoJson(
        gdf,
        name='Hidrografia - Represas',
        style_function=lambda x: {
            'fillColor': '#0099ff',
            'color': '#0099ff',
            'weight': 1,
            'fillOpacity': 0.5
        },
        highlight_function=lambda x: {
            'weight': 3
        },
        embed=False,
        zoom_on_click=False,
        control=True,
        show=False,
    )


if __name__ == '__main__':
    # Create Maps
    def get_map(input_shp):
        # Input
        gdf = gpd.read_file(input_shp)
        gdf = gdf.to_crs(epsg=4326)
        sw = gdf.bounds[['miny', 'minx']].min().values.tolist()
        ne = gdf.bounds[['maxy', 'maxx']].max().values.tolist()
        bounds = [sw, ne]
        
        # Zoom
        min_zoom = 10
        max_zoom = 18

        # Create Map
        m = folium.Map(
            #location=list_centroid,
            #zoom_start=10,
            min_zoom=min_zoom,
            max_zoom=max_zoom,
            max_bounds=True,
            #zoom_delta=0.1,
            min_lat=bounds[0][0]*(101/100),
            min_lon=bounds[0][1]*(101/100),
            max_lat=bounds[1][0]*(99/100),
            max_lon=bounds[1][1]*(99/100),
            tiles=None,
        )
        
        # Add Base Layers
        m.add_child(lyr.base.google_hybrid(min_zoom, max_zoom))
        m.add_child(lyr.base.google_terrain(min_zoom, max_zoom))
        m.add_child(lyr.base.google_streets(min_zoom, max_zoom))
        m.add_child(lyr.base.google_satellite(min_zoom, max_zoom))
        
        # Plano Diretor
        m.add_child(limite_zpa())
        m.add_child(limite_zph())
        m.add_child(limite_zvs())
        m.add_child(limite())    
        #m.add_child(limite_mun())        
        
        hidro_group = folium.FeatureGroup('Hidrografia', show=False)
        hidro_group.add_child(limite_hidro_simples())
        hidro_group.add_child(limite_hidro_dupla())
        hidro_group.add_child(limite_hidro_lakes())
        #hidro_group.add_child(limite_hidro_nascente())
        #hidro_group.add_to(m)
        
        # Plugins
        m.fit_bounds(bounds)
        plugins.Fullscreen(
            position='topleft',
            title='Clique para Maximizar',
            title_cancel='Mininizar',
        ).add_to(m)
        folium.LayerControl(
            position='topright',
            collapsed=False
        ).add_to(m)
        return m
    
    # ddd    
    m = get_map(os.path.abspath(os.path.join('src', 'sp_ff_apa_corumbatai', 'data', 'output', 'gpkg', 'apa_corumbatai_limite.gpkg')))

    # Save/Open Map    
    map_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'map_example.html')
    m.save(map_file)
    webbrowser.open(map_file)
