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
