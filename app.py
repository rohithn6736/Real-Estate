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
  if (int(request.form.get('beds')) == 2 and int(request.form.get('baths')) == 2):
   two_and_two = 1
  if (int(request.form.get('tx_year')) >= 2010 and int(request.form.get('tx_year')) <= 2013):
    during_recession = 1

  int_features = [x for x in request.form.values()]
  for x in sorted(a, reverse=True):
    del int_features[x]

  int_features.insert(20,two_and_two)
  int_features.insert(21,during_recession)
  int_features.insert(22,property_age)
  int_features.insert(23,school_score)
  int_features.extend(exterior_walls)
  int_features.extend(roof)
  int_features.extend(property_type)


  int_features = np.array([int(x) for x in int_features])

  mean = np.array([3.43422819e+00, 2.57919463e+00, 2.32278523e+03, 1.27466597e+04,
       8.78523490e-01, 3.94959732e+01, 4.38859060e+00, 5.00469799e+00,
       5.18590604e+00, 3.95610738e+01, 3.36174497e+00, 2.29093960e+01,
       1.57704698e+01, 3.85087248e+01, 6.94711409e+01, 6.50127517e+01,
       4.64265772e+02, 1.39610067e+02, 6.51006711e+00, 2.77919463e+00,
       9.26174497e-02, 2.65771812e-01, 2.43436242e+01, 1.79402685e+01,
       3.59731544e-01, 2.41610738e-02, 5.90604027e-02, 6.57718121e-02,
       1.19463087e-01, 3.75838926e-02, 2.68456376e-01, 6.57718121e-02,
       7.31543624e-02, 6.43624161e-01, 1.89261745e-01, 6.04026846e-02,
       3.35570470e-02, 4.19463087e-01, 5.80536913e-01])
  std = np.array([1.07291409e+00, 9.30476107e-01, 1.29710168e+03, 3.48055450e+04,
       3.26789902e-01, 4.69858621e+01, 4.49833982e+00, 8.44199452e+00,
       7.44270725e+00, 5.23348529e+01, 4.69370922e+00, 2.57244630e+01,
       1.79992818e+01, 6.61522282e+00, 1.98650798e+01, 1.70925415e+01,
       2.27249819e+02, 7.15109052e+01, 1.97522414e+00, 5.17234882e-01,
       2.89992927e-01, 4.41891625e-01, 2.12090250e+01, 6.45205929e+00,
       4.80082747e-01, 1.53600621e-01, 2.35816864e-01, 2.47966021e-01,
       3.24441526e-01, 1.90251507e-01, 4.43305135e-01, 2.47966021e-01,
       2.60477134e-01, 4.79088869e-01, 3.91847913e-01, 2.38311384e-01,
       1.80146474e-01, 4.93636858e-01, 4.93636858e-01])

  int_features = (int_features-mean)/std  
  final_features = [int_features]
  prediction = model.predict(final_features)

  output = round(prediction[0], 2)
  return render_template('index.html', prediction_text='House Price should be $ {}'.format(output))

if __name__ == '__main__':
  app.run(debug=True)
