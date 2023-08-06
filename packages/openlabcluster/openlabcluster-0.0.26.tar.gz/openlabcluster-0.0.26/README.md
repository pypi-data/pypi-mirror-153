# OpenLabCluster

## Usage
### Installation
#### Install from pip
Create a new enviornment with conda enviornment and install the package


For **Linux** start the environment with [spec-file.txt](./spec-file.txt)

	conda create --name OpenLabCluster --file spec-file.txt
	conda activate OpenLabCluster
	pip install openlabcluster
	
for **Mac OS** and **Windows**

	conda create --name OpenLabCluster python=3.7
	conda activate OpenLabCluster
	pip install 'openlabcluster[gui]'
	 
	
<!---##### Troubleshooting for Linux installation
If, for some reason, `wxPython` fails to install on Linux, run `sudo apt install libsdl2-dev build-essential libgtk-3-dev make gcc libgtk-3-dev libwebkitgtk-dev libwebkitgtk-3.0-dev libgstreamer-gl1.0-0 freeglut3 freeglut3-dev python-gst-1.0 python3-gst-1.0 libglib2.0-dev ubuntu-restricted-extras libgstreamer-plugins-base1.0-dev`. Then, use `pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/<your operating system>  wxPython` to install it. To determine your exact link, go to https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ and select the right folder (copy the link from the search bar). 
	
#### Install the Required Package from Enviornment File	
Git clone the entire package
Create a new  enviornment.yml file
If you are using **Linux**
	
	conda env create -f environment.yml
	
if you are using **Mac-os**
	
	conda env create -f env-mac2.yml
--->
	
	
### Execution

Run the following for **Linux**
	
	python -m openlabcluster

Run the following for **Mac-OS**

	conda install python.app
	pythonw -m openlabcluster

Run the following for **Windows**

	pythonw.exe -m openlabcluster
		
### Run a Demo

#### Create Demo Project
1. Download the *openlabcluster_example* folder from [here](https://drive.google.com/file/d/1UYtgbnTRrTQOtSAQUC0otix6RMpDvfYs/view?usp=sharing)
1. Go to *your_download-dir/openlabcluster_example* folder run 
		
		python3 prepare_video_list.py
2. Launch OpenLabCluster GUI (see Execution above)
3. Set Project Name: e.g., demo
4. Click *Load Preprocessed Keypoints*, choose datafile: your_download_dir/openlabcluster_example/demo_data.h5
5. Click *Choose Training Video List*, choose the file: your_download_dir/openlabcluster_example/video_name.text
6. Uncheck *Check to use GPU*, if GPU is not avaliable.
7. Set Feature Length = 16
8. Click *OK* to create the project

#### Start the Demo Project
1. Go to **Manage Project** panel, 
2. Choose *Load Project*
3. Select the config file as *filedirectory/IC_GUI/openlabcluster/gui/i-2021-02-16/config.yaml*
4. Click **OK**, then go to **Cluster Map**


#### Cluster Map
1. Performing unsupervised clustering
2. Click **Go to Classification**, then go to **Behavior Classification Map**.
3. *Troubleshooting:* You may see some updating issue of the Cluster Map on Mac-OS Monterey, please set the **Update Cluster Map Every (Epochs)** to be 1.

#### Behavior Classification Map: 
1. Selecting, annotating and training the classifier

### Manage Project (Start a New Project or Load Earlier Project) Detailed Description
#### Start a New Project
1. Project Name - name for the project
2.  If you have only videos, use markerless pose estimators (e.g. DeepLabCut) to extract keypoints. If you already have DeepLabCut-like formatted files, select them with "Load Keypoints Data".
3. Select your videos with "Choose Training Videos List". There should be one video for each keypoint file. Make sure the videos and keypoints files are of the same order.
4. Optional: Set a directory for the project (the default is the working directory of this project).
5. Keep the GPU box checked if you have a GPU on your computer and you would like to use it for training.
6. Enter the features length (number of body parts * number of dimensions per body part. For example, for 5 keypoints in 2D, this would be 5*2 =10).
7. Choose "OK" to create the project.
8. If you would like to edit the config (i.e. change class names, change video cropping), press "Edit Config File".

#### Loading a Project
1. Select config.yaml file, generated when you created that project.
2. Press "OK".


### Cluster Map (Unsupervised Learning)
#### Set the Training Parameters
1. The setting "Update Cluster Map Every (Epochs)": helps you to decide when to update the Cluster Map, e.g. set 1 to update Cluster Map every training epoch, or 5 to update every 5 epochs.
2. The setting "Save Cluster Map Every (Epochs)": specifies when to update and save Cluster Map.
3. The setting "Maximum Epochs": denotes the number of epoches to be performed in full training.
4. The setting "Cluster Map Dimension": allows to choose between "2D" or "3D". For "2D" the Cluster Map will be shown in 2-dimension, otherwise it is 3D dimension.
5. Dimension Reduction Methods: possible choices are "PCA", "tSNE", "UMAP". The GUI will use the choosen reduction method to perform dimension reduction and show results in Cluster Map.


#### Buttons
After setting the parameters you can perform analysis:

1. Start Clustering: perform unsupervised sequence regneration task.
2. Continue Clustering: if you stopped the clustering at some stage and want to perform clustering with ealier clustering results, click this button.
3. Stop clustering: usually the clustering will stop when it reaches the maximum epochs, but if you want to stop at itermediate stage, click this button.
4. Go to Classification: after the unsupervised clustering we go to the next step which includes: i) annotation suggestion, ii) sample annotating and iii) semi-supervised action classification with labeled samples.

### Behavior Classification Map
#### Set the Training Parameters
1. Seletction Method: In this part, your selection will decide which method GUI use to select samples for annotation. there are four possible choices ("Marginal Index (MI)", "Core Set (CS)", "Cluster Center (TOP)", "Cluster Random (Rand)", "Uniform").
2. \# Samples per Selection: how many samples you want to label in current selection stage.
3. Maimum Epochs: when perform the action recogntion, the maximum epoch the netwrok will be trained.
4. Cluster Map Dimension: you can choose "2d" or "3d", if it is "2d" the Cluster Map will be shown in 2D dimension, otherwise it is 3D dimension.
5. Dimension Reduction Methods: possible choices are "PCA", "tSNE", "UMAP". The GUI will use the choosen reduction method to perform dimension reduction and show results in Cluster Map.

#### Plots
1. Cluter Map Plot:
	
	* The will be dots in different color in the Cluter Map plot.
Red: current sample for labeling and its corresponding video is shown on the rigth.
Blue: the suggested samples for labling in this iteration.
Green: samples already been labeled.
	
	* Zoom: zoom in or zoom out the plot
	
	* Pan: move the plot around.
	
	* Update selection: save the suggeted sample id and start labeling
	
2. Plots:
	
	* left panal: show corresponding video for the sample in red color shown in Behavior Classification Map
	
	* right panel: the class name and class id, according to the video, select the class.
	
	* Previous: load the previous video
	
	* Play: paly the video
	
	* next: go to the next video 

3. Buttons:
	
	* Run Classification: save labeling results and train action recognition model.
	
	* Stop Classification: stop training
	
	* Next Selection: go the next iteration of label selection, labeling and training.
	
	* Get Results: get the Behavior Classification Map from trained model on unlabeled samples. 

