# BushFireDetectionOceania

### Orginal Data

Landsat-8 Data

Some key features of LANDSAT-8 :

•	The satellite we are relying on orbits the Earth at an altitude of 705 km, with data which is segmented into scenes of 185 × 180 km coverage.

•	As per the second World-wide Reference System (WRS), it is defined in a 16-day revisit period. 

•	The satellite utilizes an Operational Land Imager (OLI) and Thermal Infrared Sensor (TIRS) sensors to acquire eleven channels of multi-spectral data {c1, . . . , c11}. 

Some features of LANDSAT-8 Raw data:

•	Format of images: TIFF format

•	Resolution of images ≈ 7, 600 × 7, 600 pixels, with 16 bits per pixel per channel. 

•	Spatial Resolution for each multispectral: 30 meters of spatial resolution.

•	Sources for downloading data: EarthExplorer, Google Earth Engine, Amazon S3 bucket (four years of Landsat-8 data is present in a specific bucket) 

•	S3 Bucket Link: https://landsat-pds.s3.amazonaws.com/index.html.


### Dataset and Preprocessing

Proposed Dataset

During the period of September 2019 to March 2020, the Oceania region witnessed a series of bushfire occurrences. It was a devastating period for the whole world and our ecosystem. 
I have limited my scope of research to Oceania. Initially, I extracted Landsat-8 raw data for the month of Dec 2019. I carried out the whole procedure and fetched the optimum results.
Then I successfully incorporated four months of data in total ranging from Dec’19 – March’20. 
The proposed dataset has range of four months and only concerns Oceania.  Raw data comprised of around 30 Landsat-8 scenes of 7600 * 7600 pixels. Post that I have processed this consolidated dataset. 


Downloading and Processing Raw Data

I have made use of a csv file and a python script ‘download.py’ to download and process data in the desirable form [9].  
The csv file comprises of the following parameters:
Product Id; Entity Id; Acquisition Date; Cloud Cover; Processing Level; Path; Row; Min_lat; Min_lon; Max_lat; Max_lon; Download_url; PR; tipo
The choice of parameters is similar to as in [9], though the csv is entirely modified according to the needs and period of our dataset. Data falling in the period December 2019 – March 2020 has been documented in the csv along with the associated details regarding its parameters. 
The data fetched from Landsat-8 is in raw form and needs to be processed. So, the task was to convert those images into 256*256-pixel patches.
For this particular task, I have incorporated a script similar to the which is publicly available in the research [9]. Though, I have gained complete understanding of what’s being done and changed the parameters and made necessary amendments to process my data and prepare a processed image patches dataset.  
The raw data covered all the continents data, so I also had to narrow it down to Oceania region.  I used ‘Rasterio.wrap.transform_geom function’ and python code to do this task [16]. 


Creating Masks



Model 



Additional Applications

