import pandas as pd
data = {'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'age': [25, 32, 18, 47],
        'gender': ['F', 'M', 'M', 'M']}
df = pd.DataFrame(data)

# Export DataFrame thành file CSV
df.to_csv('https://drive.google.com/drive/folders/1ED3NKHhWSda9K0GsApRnC9OPG8F7yidO/data_crawl.csv', index=False)