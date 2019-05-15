airbnb.csv.zip - This is the zipped file of the raw Airbnb data. As the file was too large to commit, it has been zipped and can be used by unzipping the file.

pipeline.py - This python file contains pipelining using Dask where it takes the raw file as input and returns the clean data as the output.

Pipeline_Cleansed_data.csv - This is the file returned after the docker image is being run.

Steps to run the docker:

Run the below command on terminal:

docker run nidhi1993/pipeline
