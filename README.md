# Bibliogram
This is an implementation of analytics system for Innopolis University bibliometrics on Python 3. The system gets bibliometric information about Innopolis publications and authors, which was taken by web-scrapping, and provides user-friendly web-application for displaying it.

### Video-demonstration of the application:


https://user-images.githubusercontent.com/95312480/176891253-8be20905-8c63-4187-9d0f-6f4c1d7bc298.mp4


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

Now you are on the welcome page. 
On the top you can click on IU logo to return on main page. On the right part of the header you can choose one of four other pages: Publications, Authors, About IU, Refresh. The detailed description look in 2-5.
Scroll down and you will see a list of the existing **features** of our application.
After features list, you can see **general statistics** of Innopolis University (you will be here by clicking the field "About IU" in the header).
The arrow in the bottom right corner will return you back to the welcome page.

![image](https://user-images.githubusercontent.com/95312480/176883379-6c1d980b-5849-408a-9d7d-9dcc2809d265.png)


2. **General statistics of publications** (by clicking on Publications in header)

The header works identically to the main page. 
Here you can see general statistics of publications in Innopolis University.
Clicking on "All Publications" will take you to a page with a complete list of the university's publications.

![image](https://user-images.githubusercontent.com/95312480/176883637-2e92102a-94f6-47fc-a040-ac8347de733f.png)


3. **Publications of IU**

The main part of this page is a table with the data about the publications of IU selected by some criteria.
The middle of the page contains 4 buttons. Clicking on one of them will open a modal window. Using "Show parameters" you can choose which fields of the table to show. "Sort by" will sort by selected parameters in the chosen order. "Filter by" helps to specify year, source type, amount of citations and quartile. The "Download statistics" button suggest to choose a type of the file with information on publications you would like to download.
At the footer you can switch by the different pages with publications.

4. **Find author** (by clicking on Authors in header)

Here you can select the author whose profile you want to view. Just scroll down to find appropriate one. 
Also you can use search bar to find suitable author faster. Just write a name of the researcher in the searching field and press button "Search" or Enter. Then just click on the field corresponding to the person you are looking for.

![image](https://user-images.githubusercontent.com/71354878/176884400-d6424cf8-44a8-4cef-abe1-e0daf1a37abf.png)

5. **Author's profile**

This page contains the full name of the researcher, his/her photo, department, scientific fields and general statistics (amount of publications and citations, h-index and research beginning year).
In the lower header you can choose the type of information about the selected author (Profile, Co-authors, Publications).

![image](https://user-images.githubusercontent.com/95312480/176887670-c900eec6-1dba-436b-9c60-a45b0945cddb.png)


6. **Co-authors**

This page contains the information about researches who have ever conducted a joint study with the selected author. The information about co-authors could be downloades.

7. **Author's publications**

This page contains the information about the studies of the selected researcher. The usage possibilities are similar to the publications page. 

8. **Refresh**

If you want to choose a version of the statistical data, select one of the displayed. Also, you can call a new version by pressing "Refresh now" button.

## List of features

+ Easy navigation - everything is in the page header
+ Convenient search of the researcher
+ Ability to sort, filter and select display parameters in the tables
+ Up-to-date statistics
+ Ability to update data by request

## Requrements

```
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
```

## Project installation

1. Clone this repository
  
2. Install dependencies
```
pip3 install -r requirements.txt
```
3. Run app.py

4. Open the WEB application by the given link in the console


## Badges

[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_B21-02_Bibliogram&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=InnoSWP_B21-02_Bibliogram)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_B21-02_Bibliogram&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=InnoSWP_B21-02_Bibliogram)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_B21-02_Bibliogram&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=InnoSWP_B21-02_Bibliogram)

[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_B21-02_Bibliogram&metric=bugs)](https://sonarcloud.io/summary/new_code?id=InnoSWP_B21-02_Bibliogram)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_B21-02_Bibliogram&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=InnoSWP_B21-02_Bibliogram)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=InnoSWP_B21-02_Bibliogram&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=InnoSWP_B21-02_Bibliogram)


## MIT License

Our team chose the MIT license because we want a simple and permissive one. We do not care about working in the community or sharing improvements as much as about simplicity and understandability of the license for our team. The license is needed because our team wants to work on a project together, and share the solution with the client. Probably, developers may want to improve or expand our program. In summary, the MIT license is the most appropriate protection for us and possible users.

Copyright (c) 2022 Shulepin D.A.
              2022 Zaitseva S.A.
              2022 Sokolov Y.I.
              2022 Urzhumov V.A.

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
