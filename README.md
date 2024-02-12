TODO - 

Add compatibility for the following devices - 
 1. Neware battery cycler
 2. Linux workstation 1 (I think)

Develop publish functions for each 
So in total there should be a python script for each that contain connection and publish info
Make a separate login for each device


Battery cycler - 
- data stored in ndax files
- sample data is in one drive under data/Neware

Linux 1 -
- data stored in json files
- Sam is optimizing the data collection. When that is done, make sure that we are sending and receiving data faster than we record 
!THIS IS REALLY IMPORTANT. IT WONT GIVE US AN ERROR MESSAGE IF WE DONT DO THIS BUT WE WILL LOSE DATA!
- Access test data on the one drive
- Potential solutions if transfer is too slow - 
  - publish line by line while recording instead of in one go after
  - break up the file when sending