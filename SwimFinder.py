import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

if (len(sys.argv) == 1):
    print('Please specify a team code as an argument. For example run "python3 SwimFinder.py 313". Team codes can be found from the URL in a specific team page on www.collegeswimming.com. Here are some example team codes:')
    print('\tStevens: 313')
    print('\tTCNJ: 52')
    print('\tWPI: 372')
    print('\tNYU: 59')
    print('\tAlbright: 211')
    print('\tArcadia: 222')
    print('\tWidener: 308\n')

elif (len(sys.argv) > 2):
    print('Too many arguments. Please only specify team code.\n')

elif (str.isdigit(sys.argv[1]) == False):
    print('Given argument is not an integer. Team code must be as integer number.\n')

else:
    #if (int(sys.argv[1]) > 9826 or int(sys.argv[1]) < 1):
    if(int(sys.argv[1]) < 1):
        print('Team code out of range. Current range is [1, 9826]\n')

    else:
        Race_type = ['50 Free','100 Free','200 Free','500 Free','1000 Free','1650 Free','100 Back','200 Back','100 Breast','200 Breast','100 Fly','200 Fly','200 IM','400 IM']
        #team = '313'
        team = sys.argv[1]  #get specified team code
        People = ['M','F']
        event = ['150','1100','1200','1500','11000','11650','2100','2200','3100','3200','4100','4200','5200','5400']
        course = 'Y'
        season = '23'

        for gender in People:
            Events = []     #initialize each list to be empty
            Names = []
            Place = []
            Times = []
            for race in range(0,14):
                url = 'https://www.collegeswimming.com/team/'+team+'/times/?page=1&gender='+gender+'&event='+event[race]+'&course='+course+'&season='+season
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'html.parser')

                if(soup.find(class_='c-table-clean--responsive') is None):  #if there is no data on the page
                    print(gender, Race_type[race], 'has no data\n')
                    time.sleep(0.5)     #pause for half a second so we don't get flagged as a spammer
                
                else:
                    table = soup.find(class_='c-table-clean--responsive') #this is the table we want to extract data from
                    num_rows = table.find_all('tr')     #find all rows in table
                    num_swimmers = int(len(num_rows) - 1) #subtract 1 for title row

                    dataPoints = table.find_all('td')   #find all the data in the rows
                    total_dataPoints = int(len(dataPoints))

                    #Need to distinguish if there are 5 or 6 columns of data to determine which to remove
                    total_columns = total_dataPoints/num_swimmers
    
                    if (total_columns == 6):    #if 6 columns, then remove the first and last data point for each of the swimmers
                        for num in range(1, num_swimmers+1):
                            del dataPoints[total_dataPoints-(6*num)]    #first remove last of every 6

                        total_dataPoints = int(5 * num_swimmers)
                        for num in range(0, num_swimmers):
                            del dataPoints[(total_dataPoints - 1) - (5*num)]    #now remove first of every 5

                    else:           #else then 5 columns
                        for num in range(1, num_swimmers+1):
                            del dataPoints[total_dataPoints - (5*num)]       #only need to remove first of every 5

                    data = []
                    for item in dataPoints:
                        new_data = item.find('a')   #find all the a tags containing data we want 
                        data.append(new_data)
    
                    if(num_swimmers >= 10):     #only write the top 10 if more than 10 swimmers 
                        for swimmer in range(0, 10):
                            Events.append(Race_type[race])
                            Names.append(data[swimmer*4].contents[0])
                            Place.append(data[swimmer*4+2].contents[0].strip()) #strips extra white space and new lines
                            Times.append(data[swimmer*4+3].contents[0])

                    else:   #if less than 10, then write them all
                        for swimmer in range(0, num_swimmers):
                            Events.append(Race_type[race])
                            Names.append(data[swimmer*4].contents[0])
                            Place.append(data[swimmer*4+2].contents[0].strip()) #strips extra white space and new lines
                            Times.append(data[swimmer*4+3].contents[0])

                    print(gender, Race_type[race], 'finished\n')
                    time.sleep(0.5)     #pause for half a second so we don't get flagged as a spammer

            df = pd.DataFrame({'Event':Events,'Name':Names, 'Meet':Place, 'Time':Times})    #create data frame for all the data
            df.to_csv(team+ '_'+gender+'SwimData.csv', index=False, encoding='utf-8')       #write the data to csv file 
