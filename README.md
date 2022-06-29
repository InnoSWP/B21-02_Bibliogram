# Bibliogram
This is an implementation of analytics system for Innopolis University bibliometrics on Python 3. The system gets bibliometric information about Innopolis publications and authors, which was taken by web-scrapping, and provides user-friendly web-application for displaying it.

### Video-demonstration of the application:

https://user-images.githubusercontent.com/95312480/176200658-9a06f215-f2eb-4df3-bfa9-3027577a4c0d.mp4

The repository includes:

- Data Parser (data.py)
- Filtration System (data.py)
- Search System (data.py)
- Refreshing System (data.py)
- Flask web-application (app.py)
- HTML and CSS files
- Unit and Functional Tests (on PyTest and PyTest-Cov)
- Database of publications and researches

## How to use the application:
Run the app.py or go on the webpage. The application will open on the main page. 

1. **Main page**

Now you are on the welcome page. On the top you can click on IU logo to return on this page. On the right part of the header you can choose one of four other pages: Publications, Authors, About IU, Refresh. The detailed description look in 2-5.
After the welcome part, you can know more about the goals that you can achive using our application. 
At the end of main page, you can see general statistics of Innopolis University (you will be here by clicking the field "About IU" in the header).
The arrow at the right bottom will open welcome part of the main page.

2. **General statistics of publications** (by clicking on Publications in header)

The header works identically to the main page. 
Here you can see general statistics of publications in Innopolis University. 

3. **Publications of IU**

The main part of this page is a table with the data about the publications of IU selected by some criteria.
The middle of the page contains 4 buttons. Clicking on one of them will open a modal window. Using "Show parameters" you can choose which fields of the table to show. "Sort by" will sort by selected parameters in the chosen order. "Filter by" helps to specify year, source and work type, amount of citations and quartile. The "Download statistics" button suggest to choose a type of the file.

4. **Find author** (by clicking on Authors in header)

Here you can select the author whose profile you want to view. Just scroll down. Also you can write a name of the researcher in the searching field and press button "Search" or Enter. Then just click on the field corresponding to the person you are looking for.

5. **Author's profile**

This page contains the full name of the researcher, his/her photo, department, scientific fields and general statistics (amount of publications and citations, h-index and research beginning year).
In the lower header you can choose the type of information about the selected author (Profile, Co-authors, Publications).

6. **Co-authors**

This page contains the information about people who have ever conducted a joint study with the selected researcher. The usage possibilities are similar to the publications page. 

7. **Author's publications**

This page contains the information about the studies of the selected researcher. The usage possibilities are similar to the publications page. 

8. **Refresh**

If you want to choose a version of the data, select one of the displayed. Also, you can call a new version by pressing "Refresh now" button.

## List of features

+ Easy navigation - everything is in the page header
+ Convenient search of the researcher
+ Ability to sort, filter and select display parameters in the tables
+ Interesting statistics with graphic and word cloud
+ Ability to update data by request
+ Refreshing system

## Requrements

idna>=2.10                    
requests>=2.25.1
six>=1.15.0
tornado>=6.1
urllib3>=1.26.4
Flask>=2.1.2
matplotlib==3.5.2
matplotlib-inline==0.1.2
numpy>=1.21.2
pandas>=1.4.3
image>=1.5.33

## Project installation

1. Clone this repository
  
2. Install dependencies
```
pip3 install -r requirements.txt
```
5. Run app.py
6. Open the WEB application by the given link in the console


## Badges

## MIT License

Our team choose MIT license because we want a simple and permissive one. We do not care about working in the community or sharing improvements as much as about simplicity and understandability of the license for out team. The license is needed because our team want to work on a project together, and share the solution with the client. Probably, developers may want to improve or expand our program. In summary, MIT license is the most appropriate protection for us and possible users.

Copyright (c) 2022 Shulepin D.A.
              2022 Sokolov Y.I.
              2022 Urzhumov V.A.
              2022 Zaitseva S.A.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
