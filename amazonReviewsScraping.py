import requests
from bs4 import BeautifulSoup
import io
import pandas as pd
import boto3

s3 = boto3.client('s3')
reviewlist = []

def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 1})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup
    
def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
                'ASIN': ASIN,
                'Product': soup.title.text.replace('Amazon.com: Customer reviews: ', '').strip(),
                'Title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                'ReviewID': item.find('a', {'data-hook': 'review-title'}),
                'Rating': float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                'RatingScale': "out of 5 stars",
                'ReviewText': item.find('span', {'data-hook': 'review-body'}).text.strip(),
                'Date': item.find('span', {'data-hook': 'review-date'}).text.replace('Reviewed in the United States on ', '').strip(),
                'Reviewer': item.find('span', {'class': 'a-profile-name'}).text.strip(),
                'VPI': item.find('span', {'data-hook': 'avp-badge'}).text.strip(),
            }
            reviewlist.append(review)
    except:
        pass
        
require_cols = [1]
obj = s3.get_object(Bucket='sbsegops-work', Key='Intuit Amazon PRODUCT MAPOct27th 2020.xlsx')
dff = pd.read_excel(io.BytesIO(obj['Body'].read()), index_col=None, na_values=['NA'], usecols = "B")
for index, row in dff.iterrows():
    ASIN = (row["ASIN"])
    u = ('https://www.amazon.com/product-reviews/'+ ASIN +'/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&pageNumber=')
    for x in range(0,2):
        soup = get_soup(f'{u}{x}')
        print(f'Getting page: {u}{x}')
        get_reviews(soup)
        print(len(reviewlist))
        if not soup.find('li', {'class': 'a-disabled a-last'}):
            pass
        else:
            break
            
df = pd.DataFrame(reviewlist)
df.to_csv('amazon-reviews.csv', index=False)
s3.upload_file('amazon-reviews.csv','sbsegops-work','amazon-reviews-target.csv')
