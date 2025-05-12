#####Step 1: Load packages and list of restaurants
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import time
import random
import os

# set the working directory
Workdirectorya = '/Users/'

current_directory = Workdirectorya
csv_filename = "Washington.csv" 
csv_path = os.path.join(current_directory, csv_filename)
df_restaurants = pd.read_csv(csv_path)


#####Step 2: Scrape the first restaurant
# Add a new column 'not_recommended_url' based on the existing 'url' column
df_restaurants['not_recommended_url'] = df_restaurants['url'].apply(
    lambda x: x.replace('/biz/', '/not_recommended_reviews/') + '?not_recommended_start=0' if '/biz/' in x else x)

# Collect variables for restaurants
url = df_restaurants['not_recommended_url'][0]
name_business = df_restaurants['name'][0]

html = requests.get(url)
soup = BeautifulSoup(html.content, 'lxml')

# Initialize some necessary lists 
username = []
rating = []
date_review = []
html_text = []
url_list = []
reviewer_locations = []
reviewer_friends = []
reviewer_review_count = []
review_char_count = []
review_word_count = []
reviewer_profile_photo = []
reviewer_uploaded_photos = []

# Getting the number of subpages
Page_numbers = soup.select('.review-list-wide .page-of-pages')
if Page_numbers:  
    page_text = Page_numbers[0].get_text(strip=True)
    total_pages = int(re.sub(r'Page \d+ of ', '', page_text))
else:
    total_pages = 1 

 
for j in range(total_pages):
    url_yelp = url.replace('not_recommended_start=0', f'not_recommended_start={j * 10}')
    html = requests.get(url_yelp)
    soup = BeautifulSoup(html.content, 'lxml')
   

    # Get usernames
    soup_username = soup.select('.review-list-wide .user-display-name')
    for name in soup_username:
        username.append(name.string)
        url_list.append(url_yelp)
        

    # Get ratings
    soup_stars = soup.select('.review-list-wide .review-content .rating-large')
    for stars in soup_stars:
        rating.append(stars.attrs['title'])

    # Clean ratings
    rating = [re.sub(' star rating', '', str(r)) for r in rating]
    rating = [float(r) for r in rating if r.replace('.', '', 1).isdigit()]  

    # Get review dates
    soup_date = soup.select('.review-list-wide .review-content .rating-qualifier')
    for date in soup_date:
        date_review.append(date.text.strip())

    # Clean review dates
    date_review = [re.sub('Updated review|Previous review|\n|\s+', '', dr) for dr in date_review]

    # Get review texts
    html_texts = soup.select('.review-list-wide p')
    for t in html_texts:
        html_text.append(t.get_text())

    # Remove unwanted characters
    html_text = [re.sub('\xa0', '', ht) for ht in html_text]
    
    # Get reviewer_location
    soup_reviewer_location = soup.select('.review-list-wide .responsive-hidden-small b')
    for loc in soup_reviewer_location:
        reviewer_locations.append(loc.text.strip())
    
    # Get reviewer_friends
    soup_review_friends = soup.select('.review-list-wide .friend-count')
    for friend in soup_review_friends:
        friend_number = re.sub(r'\D', '', friend.text.strip())
        reviewer_friends.append(int(friend_number) if friend_number != "" else 0)
    
    # Get reviewer_review_count
    soup_reviewer_review_count = soup.select('.review-list-wide .review-count')
    for count in soup_reviewer_review_count:
        count= re.sub(r'\D', '', count.text.strip())
        reviewer_review_count.append(int(count) if count != "" else 0)
    
    # Get review length
    soup_reviewer_lengths = soup.select('.review-list-wide p')
    for review in soup_reviewer_lengths:
        review_text = review.text.strip()
        review_char_count.append(len(review_text))
        review_word_count.append(len(review_text.split()))
    
    # Get reviewer profile photo
    soup_reviewer_profile_photo = soup.select('.review-list-wide .pb-60s .photo-box-img')
    for img in soup_reviewer_profile_photo:
        if img and 'src' in img.attrs:
            img_src = img['src']
            if 'default_avatar' in img_src:
                reviewer_profile_photo.append(0)
            else:
                reviewer_profile_photo.append(1)
        else:
            reviewer_profile_photo.append(0)
    
    # Get reviewer photos that they have posted
    soup_reviews = soup.select('.review-list-wide .review--with-sidebar')
    for rev in soup_reviews:
        soup_photo_count = rev.select('.photo-count')
        if soup_photo_count:
            count = re.sub(r'\D', '', soup_photo_count[0].text.strip())
            reviewer_uploaded_photos.append(int(count) if count != "" else 0)
        else:
            reviewer_uploaded_photos.append(0)
   
    print(f"Usernames count: {len(username)}")
    print(f"Locations count: {len(reviewer_locations)}")
    print(f"Profile photos count: {len(reviewer_profile_photo)}")
    print(f"Friends count: {len(reviewer_friends)}")
    print(f"Review character count: {len(review_char_count)}")
    print(f"Review word count: {len(review_word_count)}")
    print(f"Reviews count: {len(reviewer_review_count)}")
    print(f"Uploaded photos count: {len(reviewer_uploaded_photos)}")
    
    sleep_time1 = random.uniform(1, 5)
    time.sleep(sleep_time1)

# Combine everything into a dataset
name_business_mult = [name_business] * len(username)
url_restaurant_mult = url_list[:len(username)] 

RatingDataSet = list(zip(name_business_mult, url_restaurant_mult, username, rating, date_review, html_text,reviewer_locations,reviewer_friends,reviewer_review_count,review_char_count,review_word_count,reviewer_profile_photo,reviewer_uploaded_photos))

df_rating = pd.DataFrame(data=RatingDataSet, columns=['name_business', 'url', 'username', 'rating', 'date_review', 'text', 'location', 'friends', 'reviews', 'Char length', 'word length', 'Profile', 'Posted photoes'])

# Save to CSV
output_filename = "Washington_ratings_fixed.csv"
output_path = os.path.join(current_directory, output_filename)
df_rating.to_csv(output_path, index=False, encoding='utf-8')


#####Step 3: Putting Step 2 in a loop


for u in range(1,100):
    try:
        #collect variables for restaurants
        url = df_restaurants['not_recommended_url'][u]
        name_business = df_restaurants['name'][u]
        
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')
        
        # Initialize lists outside the loop
        username = []
        rating = []
        date_review = []
        html_text = []
        url_list = []
        reviewer_locations = []
        reviewer_friends = []
        reviewer_review_count = []
        review_char_count = []
        review_word_count = []
        reviewer_profile_photo = []
        reviewer_uploaded_photos = []
        
        # Getting the number of subpages
        Page_numbers = soup.select('.review-list-wide .page-of-pages')
        if Page_numbers:  
            page_text = Page_numbers[0].get_text(strip=True)
            total_pages = int(re.sub(r'Page \d+ of ', '', page_text))
        else:
            total_pages = 1 


        for j in range(total_pages):
            url_yelp = url.replace('not_recommended_start=0', f'not_recommended_start={j * 10}')
            html = requests.get(url_yelp)
            soup = BeautifulSoup(html.content, 'lxml')

            # Get usernames
            soup_username = soup.select('.review-list-wide .user-display-name')
            for name in soup_username:
                username.append(name.string)
                url_list.append(url_yelp)

            # Get ratings
            soup_stars = soup.select('.review-list-wide .review-content .rating-large')
            for stars in soup_stars:
                rating.append(stars.attrs['title'])

            # Clean ratings
            rating = [re.sub(' star rating', '', str(r)) for r in rating]
            rating = [float(r) for r in rating if r.replace('.', '', 1).isdigit()]  

            # Get review dates
            soup_date = soup.select('.review-list-wide .review-content .rating-qualifier')
            for date in soup_date:
                date_review.append(date.text.strip())

            # Clean review dates
            date_review = [re.sub('Updated review|Previous review|\n|\s+', '', dr) for dr in date_review]

            # Get review texts
            html_texts = soup.select('.review-list-wide p')
            for t in html_texts:
                html_text.append(t.get_text())

            # Remove unwanted characters
            html_text = [re.sub('\xa0', '', ht) for ht in html_text]
            
            # Get reviewer_location
            soup_reviewer_location = soup.select('.review-list-wide .responsive-hidden-small b')
            for loc in soup_reviewer_location:
                reviewer_locations.append(loc.text.strip())
            
            # Get reviewer_friends
            soup_review_friends = soup.select('.review-list-wide .friend-count')
            for friend in soup_review_friends:
                friend_number = re.sub(r'\D', '', friend.text.strip())
                reviewer_friends.append(int(friend_number) if friend_number else 0)
            
            # Get reviewer_review_count
            soup_reviewer_review_count = soup.select('.review-list-wide .review-count')
            for count in soup_reviewer_review_count:
                count= re.sub(r'\D', '', count.text.strip())
                reviewer_review_count.append(int(count) if count else 0)
            
            # Get review length
            soup_reviewer_lengths = soup.select('.review-list-wide p')
            for review in soup_reviewer_lengths:
                review_text = review.text.strip()
                review_char_count.append(len(review_text))
                review_word_count.append(len(review_text.split()))
            
            
            # Get reviewer profile photo
            soup_reviewer_profile_photo = soup.select('.review-list-wide .pb-60s .photo-box-img')
            for img in soup_reviewer_profile_photo:
                if img and 'src' in img.attrs:
                    img_src = img['src']
                    if 'default_avatar' in img_src:
                        reviewer_profile_photo.append(0)
                    else:
                        reviewer_profile_photo.append(1)
                else:
                    reviewer_profile_photo.append(0)
            
            
            # Get reviewer photos that they have posted
            soup_reviews = soup.select('.review-list-wide .review--with-sidebar')
            for rev in soup_reviews:
                soup_photo_count = rev.select('.photo-count')
                if soup_photo_count:
                    count = re.sub(r'\D', '', soup_photo_count[0].text.strip())
                    reviewer_uploaded_photos.append(int(count) if count != "" else 0)
                else:
                    reviewer_uploaded_photos.append(0)
            
            sleep_time2 = random.uniform(1, 5)
            time.sleep(sleep_time2)
        
        
        name_business_mult = [name_business] * len(username)
        url_restaurant_mult = url_list[:len(username)] 

        RatingDataSet = list(zip(name_business_mult, url_restaurant_mult, username, rating, date_review, html_text,reviewer_locations,reviewer_friends,reviewer_review_count,review_char_count,review_word_count,reviewer_profile_photo,reviewer_uploaded_photos))

        df_rating = pd.DataFrame(data = RatingDataSet, columns=['name_business', 'url', 'username', 'rating', 'date_review', 'text', 'location', 'friends', 'reviews', 'Char length', 'word length','Profile', 'Posted photoes'])

        output_filename = "Washington_ratings_fixed.csv"
        output_path = os.path.join(current_directory, output_filename)
        with open(output_path, 'a', newline='', encoding='utf-8') as f:
            df_rating.to_csv(f, index=False, header=False, encoding='utf-8')

                
        print(u)
        print(f"Usernames count: {len(username)}")
        print(f"Locations count: {len(reviewer_locations)}")
        print(f"Profile photos count: {len(reviewer_profile_photo)}")
        print(f"Friends count: {len(reviewer_friends)}")
        print(f"Review character count: {len(review_char_count)}")
        print(f"Review word count: {len(review_word_count)}")
        print(f"Reviews count: {len(reviewer_review_count)}")
        print(f"Uploaded photos count: {len(reviewer_uploaded_photos)}")
        
        sleep_time3 = random.uniform(1, 5)
        time.sleep(sleep_time3)
        
    except:
        print("A page was not loaded correctly")
