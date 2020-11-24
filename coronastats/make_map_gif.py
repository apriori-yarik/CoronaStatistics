import pandas as pd
import geopandas as gpd
from PIL import Image
import io

# Извличане и обработка на данните
url = "https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv"
data = pd.read_csv(url)
data = data.groupby('Country/Region').sum()
data = data.drop(columns = ['Lat', 'Long'])
data_transposed = data.T

# Извличане на геоданните
world = gpd.read_file('../static/coronastats/map_shapes/World_Map.shp')

# Промяна на имената на някои държави
world.replace('Viet Nam', 'Vietnam', inplace=True)
world.replace('Brunei Darussalam', 'Brunei', inplace=True)
world.replace('Cape Verde', 'Cabo Verde', inplace=True)
world.replace('Democratic Republic of the Congo', 'Congo (Kinshasa)', inplace=True)
world.replace('Congo', 'Congo (Brazzaville)', inplace=True)
world.replace('Czech Republic', 'Czechia', inplace=True)
world.replace('Swaziland', 'Eswatini', inplace=True)
world.replace('Iran (Islamic Republic of)', 'Iran', inplace=True)
world.replace('Korea, Republic of', 'Korea, South', inplace=True)
world.replace("Lao People's Democratic Republic", 'Laos', inplace=True)
world.replace('Libyan Arab Jamahiriya', 'Libya', inplace=True)
world.replace('Republic of Moldova', 'Moldova', inplace=True)
world.replace('The former Yugoslav Republic of Macedonia', 'North Macedonia', inplace=True)
world.replace('Syrian Arab Republic', 'Syria', inplace=True)
world.replace('Taiwan', 'Taiwan*', inplace=True)
world.replace('United Republic of Tanzania', 'Tanzania', inplace=True)
world.replace('United States', 'US', inplace=True)
world.replace('Palestine', 'West Bank and Gaza', inplace=True)

# Обединяване на числовите данни и геоданните
merge = world.join(data, on='NAME', how='right')

image_frames = []

# Създаване на GIF-картата
for dates in merge.columns.to_list()[2:]:
    ax = merge.plot(column=dates, cmap='OrRd', figsize=(14, 14), legend=True, scheme='user_defined', classification_kwds={'bins': [10, 50, 100, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]},edgecolor='black', linewidth=0.4)
    ax.set_title('Total Confirmed Coronavirus Cases ' + dates, fontdict={'fontsize': 20}, pad=12.5)
    ax.set_axis_off()
    ax.get_legend().set_bbox_to_anchor((0.18, 0.6))
    img = ax.get_figure()
    f = io.BytesIO()
    img.savefig(f, format='png', bbox_inches='tight')
    f.seek(0)
    image_frames.append(Image.open(f))

# Запаметяване на GIF-картата
image_frames[0].save('../static/coronastats/gif/Dynamic Covid-19 progression.gif', format='GIF', append_images=image_frames[1:], save_all=True, duration=300, loop = 0)