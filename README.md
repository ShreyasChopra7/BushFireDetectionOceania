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


### Automatic Segmented Masks Generation

I have made use of three popular fire detection algorithms and consolidated the results by forming combinations of them.
I have written my own scripts to carry out this process. Though the inspired research also utilizes these three fire algorithms for performing image segmented masks.
I have fetched the appropriate masks using the coincidence of occurrence of these fire algorithm results.
The processed image patches along with these created masks will serve the role of an input for training our model.

### Model 

Model Architecture  (Refer main.py file)

The U-Net architecture which I have implemented as a part of my research majorly comprises of two paths. The left side of the architecture represents the first path, which is the contraction path. Its also known as the encoder and is used to capture the context in the image. The encoder refers to a traditional stack of convolutional and max pooling layers. The right part of the architecture depicts the second path which is the symmetric expanding path. It’s also referredas the decoder. Decoder is utilized for enablement of precise localization using transposed convolutions [10]. So, this structure implies that it’s built on top of an end-to-end fully convolutional network (FCN). Our UNET implementation only comprises of Convolutional layers and doesn’t contains any sort of Dense layer which supports that the model can accept image of any size.

Model Training (Refer train.py)

• Model is compiled with Adam optimizer, and we use binary cross entropy loss function since there are only two classes (fire pixel and no fire pixel).

• Note that for each pixel we get a value between 0 to 1.

• 0 represents no fire and 1 represents fire.

• We have maintained 0.5 as the threshold to decide whether to classify a pixel as 0 or 1.

• our U-net model converts the active fire pixels to RGB (255,255,255) and the rest to RGB (0,0,0).

• I have run model for 15000 epoch, and simultaneously calculated loss and accuracy. after 15000 epoch accuracy wasn't improving much. So, to avoid overfitting i stopped the training post 15000 epoch.

• All the necessary scripts will be well documented as a part of thesis.


Model Prediction

The ‘predict.py’ script consists of a function named detect in which we are inputting the image along with the model weights through the U-Net architecture so that it can calculate the confidences of each pixel across the image. If confidence > 0.5, then the respective pixel is Fire pixel. I have set this threshold by defining ‘out_threshold = 0.5’, as one of the arguments of this function. There is also a function 'out_files' for automating generation of output file names. Further, there is a function for plotting the resultant segmented mask image and a function for converting the pixels with confidence > 0.5 to RGB(255,255,255). 

This script utilizes two scripts, 'main.py' for implementation of UNET architecture and 'model_train.py' for obtaining the model weights as a pth file, 'unet_semantic.pth'.




### Additional Applications (Refer utils/)

Counting fire pixels

Our U-net model converts the active fire pixels to RGB (255,255,255) and the rest to RGB (0,0,0).
The script ‘countpixels.py’ is utilized to count the number of fire pixels present in the resultant segmented mask.

Transforming Masks

The segmented masks fetched comprises of two values, value 1 is for fire occurrence and its 0 when there is no fire. As a result, the masks produce won’t be displaying "white" and "black" colours on simply opening in an image view form. So, we are handling this using the script ‘plot.py’. This script results in conversion of the image into a PNG format displaying respective white and black pixels.
Though this functionality has been already handled in our ‘predict.py’ script. Still I have prepared a separate script for convenience of visualisation.
