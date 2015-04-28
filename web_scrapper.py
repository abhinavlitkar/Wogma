##load the required libraries
import urllib2
from unidecode import unidecode
from bs4 import BeautifulSoup
import re

##load the html of webpage
page = urllib2.urlopen('http://wogma.com/movies/basic/').read() 
soup = BeautifulSoup(page)

##function to remove html tags
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
	

##find the divs containing the links to review page	
review_link_Divs = soup.findAll('div', attrs={'class' : 'button related_pages review '})

##extract the reviews from the webpage
reviews=[]
for div in review_link_Divs:
	x=div.find('a')['href'] ##link to review page
	url = "http://wogma.com"+ x ##complete url of the review page	
	##load the html of review webpage
	page = urllib2.urlopen(url).read()
	soup2 = BeautifulSoup(page)
		
	##find the div class containing review
	revDivs = soup2.findAll('div', attrs={'class' : 'review large-first-letter'})
		
	##remove unwanted character
	z=re.sub("\n","",striphtml(str(revDivs)))
	reviews.append(unidecode(z.decode('utf8')))
    
	
##convert the reviews list to a data frame	
import pandas
reviews_df=pandas.DataFrame(reviews)
reviews_df.columns=["Reviews"]

##ask user to select the directory where the file is to be saved
import tkFileDialog
x = tkFileDialog.askdirectory(title=['Select where to save the reviws file'])
filename = str(x) + '/Reviews.csv'

##write the reviews csv
reviews_df.to_csv(filename, sep=',')