import pandas as pd
import numpy as np
from dask.multiprocessing import get


def read_file(file):
    df =  pd.read_csv('airbnb.csv', low_memory=False)
    return df


def spcl_char(read_file):
    df = read_file
    df['extra_people'] = df['extra_people'].astype(str)
    df['extra_people'] = df['extra_people'].str.replace('$', '')
    df['extra_people'] = df['extra_people'].astype(float)

    # Remove the dollar signs and commas in the 'price' column
    df['price'] = df['price'].astype(str)
    df['price'] = df['price'].str.replace('$', '')
    df['price'] = df['price'].str.replace(',', '')
    df['price'] = df['price'].astype(float)

    # Remove the dollar signs in the 'cleaning_fee' column
    df['cleaning_fee'] = df['cleaning_fee'].astype(str)
    df['cleaning_fee'] = df['cleaning_fee'].str.replace('$', '')
    df['cleaning_fee'] = df['cleaning_fee'].astype(float)

    df['amenities'] = df['amenities'].str.replace('{', '')
    df['amenities'] = df['amenities'].str.replace('}', '')
    df['amenities'] = df['amenities'].str.replace('"', '')
    return df

def zip_code_clean(spcl_char):
    df = spcl_char
    df = df.dropna(axis = 0, subset = ['zipcode'])
    df.loc[df['zipcode']=='02134-1704','zipcode']= '02134'
    df.loc[df['zipcode'] == '02108 02111', 'zipcode'] = '02108'
    df = df[df.zipcode != "G4 0ET"]
    df['zipcode'] = df['zipcode'].astype(int)
    return df


def missing_values(zip_code_clean):
    df = zip_code_clean
    df = df.sort_values(by=['zipcode', 'property_type'])
    df.groupby(['zipcode', 'property_type']).mean()

    bool_bedrooms_na = df['bedrooms'].isna()
    bool_2121_bedrooms = df['zipcode'] == 2115
    bool_property_bedrooms = df['property_type'] == 'Serviced apartment'
    need_replacement = bool_2121_bedrooms & bool_bedrooms_na & bool_property_bedrooms
    df.loc[need_replacement, 'bedrooms'] = 2

    bool_bath_na = df['bathrooms'].isna()
    bool_2115_bath = df['zipcode'] == 2115
    bool_2130_bath = df['zipcode'] == 2130
    bool_2116_bath = df['zipcode'] == 2116

    bool_property_bath = df['property_type'] == 'Bed and breakfast'
    bool_property1_bath = df['property_type'] == 'House'
    bool_property2_bath = df['property_type'] == 'Bed and breakfast'

    need_replacement1 = bool_bath_na & bool_2115_bath & bool_property_bath
    need_replacement2 = bool_bath_na & bool_2130_bath & bool_property1_bath
    need_replacement3 = bool_bath_na & bool_2116_bath & bool_property2_bath
    need_replacement4 = bool_bath_na & bool_2116_bath & bool_property1_bath

    df.loc[need_replacement1, 'bathrooms'] = 0
    df.loc[need_replacement2, 'bathrooms'] = 2
    df.loc[need_replacement3, 'bathrooms'] = 2
    df['bathrooms'].fillna(1, inplace=True)

    bool_beds_na = df['beds'].isna()

    bool_property_beds = df['property_type'] == 'Other'
    bool_2026_beds = df['zipcode'] == 2026
    bool_2115_beds = df['zipcode'] == 2115
    bool_2121_beds = df['zipcode'] == 2121

    need_replacement4 = bool_beds_na & bool_2026_beds & bool_property1_bath
    need_replacement5 = bool_beds_na & bool_2115_beds & bool_property_beds
    need_replacement6 = bool_beds_na & bool_2121_beds & bool_property1_bath

    df.loc[need_replacement4, 'beds'] = 3
    df.loc[need_replacement5, 'beds'] = 1
    df.loc[need_replacement6, 'beds'] = 1
    return df


def fill_na(missing_values):
    df = missing_values
    df['bedrooms'].fillna(1, inplace=True)
    df['beds'].fillna(2, inplace=True)
    return df

def drop(fill_na):
    df=fill_na
    df.drop(columns=['xl_picture_url','thumbnail_url','square_feet','neighbourhood_group_cleansed','license',
                      'host_acceptance_rate','medium_url'],inplace = True)
    return df

def drop_again(drop):
    df=drop
    df = df.drop(columns=['Unnamed: 0', 'access', 'availability_30', 'availability_365', 'availability_60',
    'availability_90','calculated_host_listings_count', 'calculated_host_listings_count_entire_homes',
    'calculated_host_listings_count_private_rooms', 'calculated_host_listings_count_shared_rooms',
    'calendar_last_scraped', 'calendar_updated', 'city','country', 'country_code',  'experiences_offered',
    'first_review', 'has_availability', 'host_about', 'host_has_profile_pic', 'host_id',
    'host_identity_verified', 'host_is_superhost', 'host_listings_count', 'host_location', 'host_name',
    'host_neighbourhood', 'host_picture_url', 'host_response_rate', 'host_response_time', 'host_since',
    'host_thumbnail_url', 'host_total_listings_count', 'host_url', 'host_verifications', 'house_rules', 'id',
    'instant_bookable', 'interaction', 'is_location_exact', 'jurisdiction_names', 'last_review', 'last_scraped',
    'latitude', 'listing_url', 'longitude', 'market', 'maximum_maximum_nights', 'maximum_minimum_nights',
    'maximum_nights', 'maximum_nights_avg_ntm', 'minimum_maximum_nights', 'minimum_minimum_nights',
    'minimum_nights_avg_ntm', 'monthly_price', 'neighbourhood', 'notes', 'number_of_reviews',
    'number_of_reviews_ltm', 'picture_url', 'require_guest_phone_verification', 'extra_people','guests_included',
    'require_guest_profile_picture', 'requires_license', 'review_scores_accuracy', 'review_scores_checkin',
    'review_scores_cleanliness', 'review_scores_communication', 'review_scores_location','review_scores_value',
    'reviews_per_month','scrape_id','smart_location', 'state', 'street','transit', 'weekly_price'])
    return df

def mean(drop_again):
    df=drop_again
    mean_cleaning_fee = np.nanmean(df["cleaning_fee"])
    df["cleaning_fee"].fillna(value=mean_cleaning_fee, inplace=True)

    mean_review_scores_rating = np.nanmean(df["review_scores_rating"])
    df["review_scores_rating"].fillna(value=mean_review_scores_rating, inplace=True)
    return df

def amenities(mean):
    df=mean
    amen = df['amenities'].tolist()
    list = []
    ammenties_count = []
    for i in amen:
        list.append(i.split(','))
    for j in list:
        ammenties_count.append(len(j))
    df['ammenties_count'] = ammenties_count
    return df

def categorical(amenities):
    df = amenities
    df = df.reset_index(drop=True)
    df = pd.get_dummies(df, columns =['bed_type','room_type','neighbourhood_cleansed',
                                          'property_type'], prefix = ['Bed','Room','Neighborhood',
                                                                      'Property'], drop_first = True)
    df.drop(columns=['amenities','description','name','neighborhood_overview','cancellation_policy',
                       'space','summary','security_deposit','is_business_travel_ready'], inplace=True)
    return df

def price_limit(categorical):
    df = categorical
    df = df[~(df[['price']] == 0).any(axis=1)]
    df = df[~(df['price'] > 500)]
    df.to_csv('Pipeline_Cleansed_data.csv')

def dask():
    dask_file = {'step1':(read_file, 'default'),
                 'step2': (spcl_char, 'step1'),
                 'step3': (zip_code_clean, 'step2'),
                 'step4': (missing_values, 'step3'),
                 'step5': (fill_na, 'step4'),
                 'step6': (drop, 'step5'),
                 'step7': (drop_again,'step6'),
                 'step8':(mean, 'step7'),
                 'step9': (amenities,'step8'),
                 'step10': (categorical,'step9'),
                 'step11':(price_limit,'step10')}
    get(dask_file, 'step11')




if __name__ == '__main__':
    dask()

