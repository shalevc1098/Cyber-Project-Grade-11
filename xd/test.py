import requests
import urllib
import os
arr1 = [1, 2, 3, 4]
arr2 = [2, 1, 4, 3]

def has_same_elements_as_arr1(arr1, arr2):
    if len(arr1) != len(arr2):
        return False

    for element in arr1:
        if element not in arr2:
            return False
    return True

r = requests.get(f"https://vsco.co/api/3.0/medias/profile?site_id=79302988", 
headers={'Content-Type':'application/json', 'Authorization': 'Bearer 7356455548d0a1d886db010883388d08be84d0c9'})

for image in r.json()['media']:
    url = "https://" + image['image']['responsive_url']
    page = requests.get(url)
    f_ext = os.path.splitext(url)[-1]
    f_name = f"{image['image']['_id']}{f_ext}"
    with open(f_name, 'wb') as f:
        f.write(page.content)

cursor = r.json()['next_cursor']
cursors = []
cursors.append(cursor)
counter = 1
while True:
    try:
        r = requests.get(f"https://vsco.co/api/3.0/medias/profile?site_id=79302988&cursor={cursor}", 
        headers={'Content-Type':'application/json', 'Authorization': 'Bearer 7356455548d0a1d886db010883388d08be84d0c9'})
        for image in r.json()['media']:
            url = "https://" + image['image']['responsive_url']
            page = requests.get(url)
            f_ext = os.path.splitext(url)[-1]
            f_name = f"{image['image']['_id']}{f_ext}"
            with open(f_name, 'wb') as f:
                f.write(page.content)
        cursor = r.json()['next_cursor']
        print(cursor)
        if cursor in cursors:
            break
        counter += 1
    except:
        break