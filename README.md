# CPE551
Engineering Programming Python
This repo contains the code for the final project for CPE-551, Engineering Programming Python. I chose to create a script that pulls data from www.collegeswimming.com. 
Specifically, the code pulls the top 10 times for swimmers on a specified team and updates the event, swimmer name, meet and time to a .csv file. Only individual yards events are pulled and separate .csv files are created for men's events and women's events, designated by "M" and "F", respectively.
Currently the script is written to pull data from the 2019-2020 swim season, specified in collegeswimming by season number '23'. This can easily be changed if another season is desired. 
The script must be run using python3 and it takes one argument, which is the code of the desired team to be pulled. An example command to run the program is "python3 SwimFinder.py 313".
Team codes can be found in the URL of the specified team's page on www.collegeswimming.com. Below are some example team codes:
  Stevens: 313
  TCNJ: 52
  WPI: 372
  NYU: 59
  Albright: 211
  Arcadia: 222
  Widener: 308
