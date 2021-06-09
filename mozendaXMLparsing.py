import bs4 as bs
import urllib.request
import requests
import io
import pandas as pd
import boto3
import lxml

s3 = boto3.client('s3')
reviewList = []

for x in range(0,9):
    sauce = urllib.request.urlopen(f'https://api.mozenda.com/rest?WebServiceKey=8E605009-BB28-4B99-B858-E1DA8345C0B8&Service=Mozenda10&Operation=View.GetItems&ViewID=1077&PageNumber={x}').read()
    soup = bs.BeautifulSoup(sauce, features='xml')
    for table in soup.find_all('Item'):
            result = {
                'ItemID': table.find('ItemID').text.replace('<ItemID>',''),
                'Title': table.find('Title').text.replace('<Title>',''),
                'Date': table.find('Date').text.replace('<Date>',''),
                'PLATFORM': table.find('PLATFORM').text.replace('<PLATFORM>',''),
                'ProductID': table.find('ProductID').text.replace('<ProductID>',''),
                'ProductTitle': table.find('ProductTitle').text.replace('<ProductTitle>',''),
                'Rating': table.find('Rating').text.replace('<Rating>',''),
                'RatingScale': table.find('RatingScale').text.replace('<RatingScale>',''),
                'ReviewID': table.find('ReviewID').text.replace('<ReviewID>',''),
                'Reviewer': table.find('Reviewer').text.replace('<Reviewer>',''),
                'ReviewText': table.find('ReviewText').text.replace('<ReviewText>',''),
                'VerifiedPurchaseIndicator': table.find('VerifiedPurchaseIndicator').text.replace('<VerifiedPurchaseIndicator>',''),
                'Created': table.find('Created').text.replace('<Created>',''),
                'Modified': table.find('Modified').text.replace('<Modified>',''),
                'OverallRating': table.find('OverallRating').text.replace('<OverallRating>',''),
                'TotalRatings': table.find('TotalRatings').text.replace('<TotalRatings>',''),
            }
            reviewList.append(result)

df = pd.DataFrame(reviewList)
df.to_csv('amazon-reviews.csv', index=False)
s3.upload_file('amazon-reviews.csv','idl-sales-analyst-uw2-sandbox-prd', 'Amazon_Reviews/scm_amazon_reviews_delta.csv')
