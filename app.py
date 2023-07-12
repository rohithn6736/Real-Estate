import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle as pkl

app = Flask(__name__)
model = pkl.load(open('model.pkl','rb'))

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
  year_built = request.form.get('year_built')
  tx_year = request.form.get('tx_year')

  roof_list = ['Asphalt', 'Composition Shingle', 'Missing','Other', 'Shake Shingle']
  roof = np.zeros(len(roof_list))
  roof.tolist()

  exterior_walls_list = ['Brick','Brick veneer','Combination','Metal','Missing','Other','Siding (Alum/Vinyl)','Wood']
  exterior_walls = np.zeros(len(exterior_walls_list))
  exterior_walls.tolist()

  property_type_list = ['Apartment / Condo / Townhouse','Single-Family']
  property_type = np.zeros(len(property_type_list))
  property_type.tolist()

  index_roof = roof_list.index(request.form.get('roof'))
  roof[index_roof] = 1

  index_walls = exterior_walls_list.index(request.form.get('exterior_walls'))
  exterior_walls[index_walls] = 1
  
  index_property_type = property_type_list.index(request.form.get('property_type'))
  property_type[index_property_type] = 1

  a = [3,5,6,7,24]
  two_and_two = 0
  during_recession = 0
  
  property_age = int(tx_year) - int(year_built)
  school_score = int(request.form.get('num_schools'))*int(request.form.get('median_school'))
  if (int(request.form.get('beds')) == 2 & int(request.form.get('baths')) == 2):
   two_and_two = 1
  if (int(request.form.get('tx_year')) >= 2010 & int(request.form.get('tx_year')) <= 2013):
    during_recession = 1

  int_features = [x for x in request.form.values()]
  for x in sorted(a, reverse=True):
    del int_features[x]
  
  int_features.extend(exterior_walls)
  int_features.extend(roof)
  int_features.extend(property_type)
  int_features.insert(22,property_age)
  int_features.insert(23,school_score)
  int_features.insert(20,two_and_two)
  int_features.insert(21,during_recession)

  int_features = [int(x) for x in int_features]

  final_features = [np.array(int_features)]
  prediction = model.predict(final_features)

  output = round(prediction[0], 2)
  return render_template('index.html', prediction_text='House Price should be $ {}'.format(output))

if __name__ == '__main__':
  app.run(debug=True)
