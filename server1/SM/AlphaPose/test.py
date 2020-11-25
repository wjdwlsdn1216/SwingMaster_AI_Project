import json
import numpy as np
with open("./examples/res/sep-json/0.json", "r") as json_file:

    data = json.load(json_file)


    data = data['bodies'][0]['joints']

    data = np.array(data).reshape(18,3)
    print(data)
