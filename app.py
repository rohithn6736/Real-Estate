import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle as pkl

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
  year_built = request.form.get('year_built')
  tx_year = request.form.get('tx_year')

  roof_list = ['roof_Asphalt', 'roof_Composition Shingle', 'roof_Missing','roof_Other', 'roof_Shake Shingle']
  roof = [np.zeros(len(roof_list))]

  exterior_walls_list = ['Brick','Brick veneer','Combination','Metal','Missing','Other','Siding (Alum/Vinyl)','Wood']
  exterior_walls = [np.zeros(len(exterior_walls_list))]

  property_type_list = ['property_type_Apartment / Condo / Townhouse','property_type_Single-Family']
  property_type = [np.zeros(len(property_type_list))]

  index_roof = roof_list.index(request.form.get('roof'))
  roof[index_roof] = 1

  index_walls = exterior_walls_list.index(request.form.get('exterior_walls'))
  exterior_walls_list[index_walls] = 1
  
  index_property_type = property_type_list.index(request.form.get('property_type'))
  property_type_list[index_property_type] = 1

  a = [3,5,6,7,24]

  
  property_age = tx_year - year_built
  school_score = request.form.get(num_schools)*request.form.get(median_school)
  (two_and_two := 1) if (request.form.get(beds) == 2 & request.form.get(baths) == 2) else (two_and_two := 0)
  (during_recession := 1) if (request.form.get(tx_year) >= 2010 & request.form.get(tx_year) <= 2013) else (during_recession := 0)

  int_features = [int(x) for x in request.form.values()]
  for x in a:
    del int_features[x]
  
  int_features.extend(exterior_walls_list)
  int_features.extend(roof_list)
  int_features.extend(property_type_list)
  

  final_features = [np.array(int_features)]
  prediction = model.predict(final_features)

  output = round(prediction[0], 2)
  return render_template('index.html', prediction_text='House Price should be $ {}'.format(output))

if __name__ == '__main__':
  app.run(debug=True)