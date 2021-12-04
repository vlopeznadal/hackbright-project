![Cafetastic logo](https://github.com/vlopeznadal/hackbright-project/blob/main/logo.png?raw=true "Cafetastic")

Cafetastic makes finding an enjoyable cafe near you easier. This app provides a way to see reviews and ratings from Yelp and Google in one place. Users are also able to write up their own reviews and favorite cafes for quick view on their profile page.

## Table of Contents ☕️
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Installation](#installation)
* [Attributions](#attributions)
* [About Me](#about-me)

## <a name="tech-stack"></a>Tech Stack 🖥

**Backend**:  Flask, PostgreSQL, Python, SQLAlchemy <br/>
**Frontend**:  AJAX, Bootstrap, CSS, HTML, Jinja2, JavaScript, jQuery <br/>
**APIs**:  Cloudinary, Google Maps JavaScript, Google Places, Yelp

## <a name="features"></a>Features 🔎

Register for an account and login to use any app features.

![Registration and Login](/static/img/gifs/register-login.gif)

Search for a cafe by zipcode and radius.

![Cafe Search](/static/img/gifs/search-cafes.gif)

View the cafe results of a search on map and listed out.

![View Cafe Results](/static/img/gifs/see-results.gif)

View a particular cafe's details, including reviews from Google and Yelp.

![View Cafe Details](/static/img/gifs/view-details.gif)

Write your own review and pick a rating for a cafe.

![Write Cafe Review](/static/img/gifs/write-review.gif)

Edit your cafe review.

![Edit Cafe Review](/static/img/gifs/edit-review.gif)

Favorite a cafe.

![Favorite a Cafe](/static/img/gifs/fav-cafe.gif)

Upload your own profile picture.

![Upload Profile Picture](/static/img/gifs/upload-pic.gif)

View your favorited and reviewed cafes.

![View User Content](/static/img/gifs/view-favs-reviews.gif)


## <a name="installation"></a>Set Up 🛠

* Install [Python](https://www.python.org/downloads/) <br/>
* Install [PostgreSQL](https://www.postgresql.org/download/)

Clone repository:
```
git clone https://github.com/vlopeznadal/hackbright-project.git
```

Create and activate virtual environment:
```
virtualenv env
source env/bin/activate
```

Install the dependencies:
```
pip3 install -r requirements.txt
```
* Sign up to use the [Cloudinary API](https://cloudinary.com), [Google Places API](https://developers.google.com/maps), [Google Maps Javascript API](https://developers.google.com/maps), and [Yelp API](https://www.yelp.com/developers).

Save your Yelp and Cloudinary API keys to a file `secrets.sh`. The file should resemble this:
```
export YELP_KEY='***'
export CLOUDINARY_KEY='***'
export CLOUDINARY_SECRET='***'
```
Restrict your Google Maps key and create two map IDs. Replace the asteriks in the following locations:

`results.html` and `details.html` - one map ID for each page
```html
<!-- Create Google map with API key, map ID, and function -->
  <script
    async defer
    src="https://maps.googleapis.com/maps/api/js?key=***&map_ids=***&callback=initMap">
  </script>
```
`results-map.js` and `cafe-map.js` - one map ID for each file
```javascript
// Setting center to cafe's coordinates, zoom
                center: {
                    lat: coordinates['latitude'],
                    lng: coordinates['longitude'],
                  },
				zoom: 13,
                mapId: '***'
            });
```
Restrict your Google Places key. Replace the asteriks in the following locations:

`crud.py`
```python
def get_google_cafe_id():
    """Using the cafe name in session to do a Google Places API request for the cafe's ID.
    Returns the cafe ID from API call."""

    # Parameters for Google Places API request, including the cafe name from session
    location = {'fields': 'place_id', 'input': session["cafe_name"], 'inputtype': 'textquery', 'key': '***'} 
```

```python
def get_google_cafe(cafe_id):
    """Using the cafe ID to do a Google Places API request for the cafe information.
    Returns the cafe information from API call."""

    # Parameters for Google Places API request, including the cafe ID
    location = {'place_id': cafe_id, 'key': '***'} 
```

Source your keys:
```
source secrets.sh
```
Set up the database:
```
createdb cafes
psql cafes < cafes.sql
```

Run the app:
```
python3 server.py
```

* Go to 'localhost:5000' in your browser to view application locally.

## <a name="attributions"></a>Attributions 🙏🏻

**Icon used as logo**: <br/>
`logo.png` and `static/img/svgs/logo.svg`: Icon by [constantino co](https://freeicons.io/profile/3156) on [freeicons.io](https://freeicons.io) - [Direct link](https://freeicons.io/download-free-35-nz-coffee-icons-for-commercial-use/top-view-coffee-cup-icon-icon-34767#)

**Map marker icons**: <br/>
`static/img/markers/marker-0.svg` through `static/img/markers/marker-5.svg`: Icons by [ColourCreatype](https://freeicons.io/profile/5790) on [freeicons.io](https://freeicons.io) - Part of the [coffee-shop-4](https://freeicons.io/icon-list/coffe-shop-4) icon set

**Background Images**: <br/>
`static/img/background/background-1.jpg`: Photo by [Petr Sevcovic](https://unsplash.com/@sevcovic23?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) - [Direct Link](https://unsplash.com/photos/qE1jxYXiwOA) <br/>
`static/img/background/background-2.jpg`: Photo by [daan evers](https://unsplash.com/@daanelise?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) - [Direct Link](https://unsplash.com/photos/tKN1WXrzQ3s) <br/>
`static/img/background/background-3.jpg`: Photo by [Qiming Chen](https://unsplash.com/@acming92?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) - [Direct Link](https://unsplash.com/photos/lzCH2_8qRH8) <br/>
`static/img/background/background-4.jpg`: Photo by [RR Abrot](https://unsplash.com/@rr_abrot?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) - [Direct Link](https://unsplash.com/photos/pNIgH0y3upM) <br/>
`static/img/background/background-5.jpg`: Photo by [@shawnanggg](https://unsplash.com/@shawnanggg?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) - [Direct Link](https://unsplash.com/photos/nmpW_WwwVSc)
  
## <a name="about-me"></a>About Me 👩🏻‍💻
Virginia Lopez Nadal is a software engineer in Minneapolis, MN. Find her on [LinkedIn](https://www.linkedin.com/in/vlopeznadal).