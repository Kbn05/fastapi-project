from fastapi import Response, status, HTTPException, APIRouter, Depends
from database.conn import cursor, mydbConnect
from app.schema.locate import ResponseLocation, Location
from .. import oauth2

router = APIRouter(
    tags=["locations"]
)

# Create a route to handle GET requests sent to the /location path
@router.post("/location", response_model=list[ResponseLocation])
async def location(locate: Location, limit: int = 10, search: str = ""):
    # cursor.execute("SELECT id, latitude, longitude FROM locations WHERE ACOS(SIN(RADIANS(latitude)) * SIN(RADIANS(%s)) +COS(RADIANS(latitude)) * COS(RADIANS(%s)) *COS(RADIANS(longitude) - RADIANS(%s))* 6371 <= %s)",
    #                (latitude, latitude, longitude, radius_in_km))
    # cursor.execute("select latitude, longitude, ( 3959 * acos(  cos( radians(37) ) * cos( radians( latitude ) ) * cos( radians( longitude ) - radians(%s) ) + sin( radians(%s) ) * sin( radians( latitude ) ))) AS distance FROM locations HAVING distance < 10000 ORDER BY distance LIMIT 0 , 50", (my_latitude, my_longitude))
    cursor.execute("SELECT id, latitude, longitude , (ACOS(SIN(RADIANS(latitude)) * SIN(RADIANS(%s)) +COS(RADIANS(latitude)) * COS(RADIANS(%s)) *COS(RADIANS(longitude) - RADIANS(%s)))* 6371) AS distance FROM locations HAVING distance < 5 ORDER BY id DESC LIMIT 0 , 50",
                   (float(locate.latitude), float(locate.latitude), float(locate.longitude)))
    my_location = cursor.fetchall()
    location_list = []
    post_list = []
    post_lists = []
    if my_location:
        for location in my_location:
            location_dict = {
                "id": location[0],
                "latitude": location[1],
                "longitude": location[2],
                "distance": location[3]
            }
            location_list.append(location_dict)
        for i in location_list:
            cursor.execute(
                "SELECT posts.*, users.id, users.username, users.email, users.created_at FROM posts INNER JOIN users ON posts.author_id = users.id WHERE posts.content LIKE %s AND posts.id LIKE %s ORDER BY posts.id DESC LIMIT %s", ('%' + search + '%', i["id"], limit,))
            my_posts = cursor.fetchone()
            post_list.append(my_posts)
        if post_list:
            for i in range(0, len(location_list)):
                post_dict = {
                    "id": location_list[i]["id"],
                    "latitude": location_list[i]["latitude"],
                    "longitude": location_list[i]["longitude"],
                    "distance": location_list[i]["distance"],
                    "post": {
                        "id": post_list[i][0],
                        "title": post_list[i][1],
                        "content": post_list[i][2],
                        "published": post_list[i][3],
                        "likes": post_list[i][4],
                        "created_at": post_list[i][5],
                        "author": {
                            "id": post_list[i][7],
                            "username": post_list[i][8],
                            "email": post_list[i][9],
                            "created_at": post_list[i][10]
                        }
                    }
                }
                post_lists.append(post_dict)
        return post_lists

    raise HTTPException(status_code=404, detail="No location found")
