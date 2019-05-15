from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd

model=pickle.load(open('DecisionTree.pkl','rb'))

surge=pickle.load(open('RFModelSurge.pkl','rb'))
app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def form():

    areacode = pd.read_csv('areacode.csv')
    areacode = areacode.to_dict(orient="records")
    bathrooms = pd.read_csv('bathrooms.csv')
    bathrooms = bathrooms.to_dict(orient="records")
    bedrooms = pd.read_csv('bedrooms.csv')
    bedrooms = bedrooms.to_dict(orient="records")
    beds = pd.read_csv('beds.csv')
    beds = beds.to_dict(orient="records")
    bed_type = pd.read_csv('bedtype.csv')
    bed_type = bed_type.to_dict(orient="records")
    accommodates = pd.read_csv('accomodates.csv')
    accommodates = accommodates.to_dict(orient="records")
    neighbourhood = pd.read_csv('neighbourhood.csv')
    neighbourhood = neighbourhood.to_dict(orient="records")
    propertytype = pd.read_csv('propertytype.csv')
    propertytype = propertytype.to_dict(orient="records")
    roomtype = pd.read_csv('roomtype.csv')
    roomtype = roomtype.to_dict(orient="records")

    return render_template('form.html', areacode=areacode, bathrooms=bathrooms, bedrooms=bedrooms,beds=beds,bed_type=bed_type, accommodates=accommodates,neighbourhood=neighbourhood,propertytype=propertytype,roomtype=roomtype)

@app.route('/result',methods=['POST','GET'])
def result():

  if request.method == 'POST':
      my_dict = {}
      # result = request.form['property']
      my_dict['zipcode'] = request.form['zipcode']
      my_dict['property_type'] = request.form['property_type']
      my_dict['accommodates'] = request.form['accommodates']
      my_dict['bedrooms'] = request.form['bedrooms']
      my_dict['bathrooms'] = request.form['bathrooms']
      my_dict['beds'] = request.form['beds']
      my_dict['cleaning_fee'] = request.form['cleaning_fee']
      my_dict['minimum_nights'] = request.form['minimum_nights']
      my_dict['review_scores_rating'] = request.form['review_scores_rating']
      my_dict['bed_type'] = request.form['bed_type']
      my_dict['room_type'] = request.form['room_type']
      my_dict['neighbourhood_cleansed'] = request.form['neighbourhood_cleansed']
      my_dict['ammenties_count'] = request.form['ammenties_count']

      my_df = pd.DataFrame([my_dict])

      list = ['accommodates','bathrooms','bedrooms','beds','cleaning_fee','minimum_nights','review_scores_rating','zipcode','ammenties_count','Bed_Couch','Bed_Futon','Bed_Pull-out Sofa','Bed_Real Bed','Room_Private room','Room_Shared room','Neighborhood_Back Bay','Neighborhood_Bay Village','Neighborhood_Beacon Hill','Neighborhood_Brighton','Neighborhood_Charlestown','Neighborhood_Chinatown','Neighborhood_Dorchester','Neighborhood_Downtown','Neighborhood_East Boston','Neighborhood_Fenway','Neighborhood_Harbor Islands','Neighborhood_Hyde Park','Neighborhood_Jamaica Plain','Neighborhood_Leather District','Neighborhood_Longwood Medical Area','Neighborhood_Mattapan','Neighborhood_Mission Hill','Neighborhood_North End','Neighborhood_Roslindale','Neighborhood_Roxbury','Neighborhood_South Boston','Neighborhood_South Boston Waterfront','Neighborhood_South End','Neighborhood_West End','Neighborhood_West Roxbury','Property_Apartment','Property_Barn','Property_Bed and breakfast','Property_Boat','Property_Boutique hotel','Property_Bungalow','Property_Bus','Property_Cabin','Property_Camper/RV','Property_Campsite','Property_Condominium','Property_Cottage','Property_Dorm','Property_Farm stay','Property_Guest suite','Property_Guesthouse','Property_Hostel','Property_Hotel','Property_House','Property_In-law','Property_Loft','Property_Other','Property_Resort','Property_Serviced apartment','Property_Timeshare','Property_Tiny house','Property_Townhouse','Property_Vacation home','Property_Villa']
      dataf = pd.DataFrame(columns=list)
      dataf = dataf.append(my_df, sort=False)
      dataf= dataf.fillna(0)  #use this to predict
      
      if request.form['bed_type']=='Bed_Pull-out Sofa':
          # dataf['Bed_Pull-out Sofa'].astype(float)
          dataf['Bed_Pull-out Sofa']= 1
      if request.form['bed_type']=='Bed_Real Bed':
          dataf['Bed_Real Bed']=1
      if request.form['bed_type']=='Bed_Couch':
          dataf['Bed_Couch']=1
      if request.form['bed_type']=='Bed_Futon':
          dataf['Bed_Futon']=1
          
      if request.form['neighbourhood_cleansed']=='Neighborhood_Back Bay':
          dataf['Neighborhood_Back Bay']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Bay Village':
          dataf['Neighborhood_Bay Village']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Beacon Hill':
          dataf['Neighborhood_Beacon Hill']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Brighton':
          dataf['Neighborhood_Brighton']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Charlestown':
          dataf['Neighborhood_Charlestown']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Chinatown':
          dataf['Neighborhood_Chinatown']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Dorchester':
          dataf['Neighborhood_Dorchester']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Downtown':
          dataf['Neighborhood_Downtown']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_East Boston':
          dataf['Neighborhood_East Boston']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Fenway':
          dataf['Neighborhood_Fenway']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Harbor Islands':
          dataf['Neighborhood_Harbor Islands']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Hyde Park':
          dataf['Neighborhood_Hyde Park']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Jamaica Plain':
          dataf['Neighborhood_Jamaica Plain']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Leather District':
          dataf['Neighborhood_Leather District']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Longwood Medical Area':
          dataf['Neighborhood_Longwood Medical Area']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Mattapan':
          dataf['Neighborhood_Mattapan']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Mission Hill':
          dataf['Neighborhood_Mission Hill']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_North End':
          dataf['Neighborhood_North End']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Roslindale':
          dataf['Neighborhood_Roslindale']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_Roxbury':
          dataf['Neighborhood_Roxbury']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_South Boston':
          dataf['Neighborhood_South Boston']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_South Boston Waterfront':
          dataf['Neighborhood_South Boston Waterfront']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_South End':
          dataf['Neighborhood_South End']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_West End':
          dataf['Neighborhood_West End']=1
      if request.form['neighbourhood_cleansed']=='Neighborhood_West Roxbury':
          dataf['Neighborhood_West Roxbury']=1
          
      if request.form['room_type']=='Room_Private room':
          dataf['Room_Private room']=1
      if request.form['room_type']=='Room_Shared room':
          dataf['Room_Shared room']=1
          
      if request.form['property_type']=='Property_Apartment':
          dataf['Property_Apartment']=1
      if request.form['property_type']=='Property_Barn':
          dataf['Property_Barn']=1
      if request.form['property_type']=='Property_Bed and breakfast':
          dataf['Property_Bed and breakfast']=1
      if request.form['property_type']=='Property_Boat':
          dataf['Property_Boat']=1
      if request.form['property_type']=='Property_Boutique hotel':
          dataf['Property_Boutique hotel']=1
      if request.form['property_type']=='Property_Bungalow':
          dataf['Property_Bungalow']=1
      if request.form['property_type']=='Property_Bus':
          dataf['Property_Bus']=1
      if request.form['property_type']=='Property_Cabin':
          dataf['Property_Cabin']=1
      if request.form['property_type']=='Property_Camper/RV':
          dataf['Property_Camper/RV']=1
      if request.form['property_type']=='Property_Campsite':
          dataf['Property_Campsite']=1
      if request.form['property_type']=='Property_Condominium':
          dataf['Property_Condominium']=1
      if request.form['property_type']=='Property_Cottage':
          dataf['Property_Cottage']=1
      if request.form['property_type']=='Property_Dorm':
          dataf['Property_Dorm']=1
      if request.form['property_type']=='Property_Farm stay':
          dataf['Property_Farm stay']=1
      if request.form['property_type']=='Property_Guest suite':
          dataf['Property_Guest suite']=1
      if request.form['property_type']=='Property_Guesthouse':
          dataf['Property_Guesthouse']=1
      if request.form['property_type']=='Property_Hostel':
          dataf['Property_Hostel']=1
      if request.form['property_type']=='Property_Hotel':
          dataf['Property_Hotel']=1
      if request.form['property_type']=='Property_House':
          dataf['Property_House']=1
      if request.form['property_type']=='Property_In-law':
          dataf['Property_In-law']=1
      if request.form['property_type']=='Property_Loft':
          dataf['Property_Loft']=1
      if request.form['property_type']=='Property_Other':
          dataf['Property_Other']=1
      if request.form['property_type']=='Property_Resort':
          dataf['Property_Resort']=1
      if request.form['property_type']=='Property_Serviced apartment':
          dataf['Property_Serviced apartment']=1
      if request.form['property_type']=='Property_Timeshare':
          dataf['Property_Timeshare']=1
      if request.form['property_type']=='Property_Tiny house':
          dataf['Property_Tiny house']=1
      if request.form['property_type']=='Property_Townhouse':
          dataf['Property_Townhouse']=1
      if request.form['property_type']=='Property_Vacation home':
          dataf['Property_Vacation home']=1
      if request.form['property_type']=='Property_Villa':
          dataf['Property_Villa']=1

   
      def categorical(data):
          data = data.reset_index(drop=True)
          data = pd.get_dummies(data, columns=['bed_type', 'room_type', 'neighbourhood_cleansed','property_type'], prefix=['Bed', 'Room', 'Neighborhood','Property'], drop_first=True)
          return data
      #df=categorical(df)

      dataf.drop(columns=['bed_type','neighbourhood_cleansed','property_type','room_type'], inplace=True)
      prediction = model.predict(dataf)
      
      # datetime = '2019-10-02'
      #
      # X = []
      # ts = pd.Timestamp(datetime)
      # dateNumber = ts.weekofyear
      # year = ts.year
      # day = ts.dayofweek
      # X.append(prediction)
      # X.append(dateNumber)
      # X.append(year)
      # X.append(day)
      # surgeoutput = surgemethod(prediction)


      return render_template("result.html",result = result, prediction=prediction,surgeoutput=surgeoutput)


# def surgemethod(prediction):
#     datetime = '2019-10-02'
#     X = []
#     ts = pd.Timestamp(datetime)
#     dateNumber = ts.weekofyear
#     year = ts.year
#     day = ts.dayofweek
#     X.append(prediction)
#     X.append(dateNumber)
#     X.append(year)
#     X.append(day)
#     surgeoutput = model.predict([X])
#     return surgeoutput
    
if __name__ == '__main__':
   app.run(debug = True)