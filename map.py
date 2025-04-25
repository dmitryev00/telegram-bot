import folium
from staticmap import StaticMap, CircleMarker
from io import BytesIO
import sql


def generate_static_map():
    context = StaticMap(
        width=1080,
        height=1080,
        url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png'
    )

    for lat, lon in sql.get_data():
        context.add_marker(
            CircleMarker(
                (lon, lat),
                color='black',
                width=10
            )
        )
        context.add_marker(
            CircleMarker(
                (lon, lat),
                color='red',
                width=9
            )
        )


    image = context.render(
        center=(33.906594, 58.390123),
        zoom=14
    )
    img_data = BytesIO()
    image.save(img_data, 'PNG')
    img_data.seek(0)
    return img_data


# def generate_map():
#     m = folium.Map(
#         location=[58.390123, 33.906594],
#         zoom_start=16,
#         tiles=None,
#         control_scale=True
#     )
#
#     folium.TileLayer(
#         'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
#         attr='OpenStreetMap',
#         name='Fast Tiles'
#     ).add_to(m)
#
#     for lat, lon in sql.get_data():
#         folium.Marker([lat, lon]).add_to(m)
#
#     img_data = m._to_png(delay=1)
#     return BytesIO(img_data)
