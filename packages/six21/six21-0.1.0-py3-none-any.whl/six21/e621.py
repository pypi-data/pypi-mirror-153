import requests, json

base_url = "https://e621.net/"





def get_post(id):
    rec_link = base_url+"posts/"+str(id)+".json"
    req = make_req(rec_link)
    postl = json.loads(req.text)["post"]
    

    return Json_Post_to_Obj(postl)

def recent(limit=50):
    
    rec_link = base_url+"posts.json?limit="+str(limit)
    req = make_req(rec_link)
    data = json.loads(req.text)
    ReturnPosts = []
    for postl in data["posts"]:
        
            

        postobj = Json_Post_to_Obj(postl)
        ReturnPosts.append(postobj)

    return ReturnPosts
        

def search(tags, page = 1, limit = 10):
    tgadd = ''
    for tag in tags:
        tgadd = tgadd+str(tag)+'+'
    
    rec_link = base_url+"posts.json?"+"limit="+str(limit)+"&page="+str(page)+"&tags="+tgadd

    req = make_req(rec_link)
    data = json.loads(req.text)
    ReturnPosts = []
    for postl in data["posts"]:
        postobj = Json_Post_to_Obj(postl)
        ReturnPosts.append(postobj)

    return ReturnPosts



def random():
    rec_link = base_url+"posts/random.json"

    req = make_req(rec_link)
    postl = json.loads(req.text)["post"]

    return Json_Post_to_Obj(postl)



def make_req(url):
    
    req = requests.get(url,headers={'User-Agent':"ExaoGen/0.4 -WIP"})
    return req

def Json_Post_to_Obj(Json_Post):

    
    class post:
        id = Json_Post["id"]
        created_at = Json_Post["created_at"]
        updated_at = Json_Post["updated_at"]
        class file:
            width = Json_Post["file"]["width"]
            height = Json_Post["file"]["height"]
            ext = Json_Post["file"]["ext"]
            size = Json_Post["file"]["size"]
            md5 = Json_Post["file"]["md5"]
            url = Json_Post["file"]["url"]
        class preview:
            width = Json_Post["preview"]["width"]
            height = Json_Post["preview"]["height"]
            url = Json_Post["preview"]["height"]
        class sample:
            has = Json_Post["sample"]["has"]
            width = Json_Post["sample"]["width"]
            height = Json_Post["sample"]["height"]
            url = Json_Post["sample"]["url"]
            
        class score:
            up = Json_Post["score"]["up"]
            down = Json_Post["score"]["down"]
            total = Json_Post["score"]["total"]
        class tags:
            general = Json_Post["tags"]["general"]
            species = Json_Post["tags"]["species"]
            character = Json_Post["tags"]["character"]
            artist = Json_Post["tags"]["artist"]
            copyright = Json_Post["tags"]["copyright"]
            invalid = Json_Post["tags"]["invalid"]
            lore = Json_Post["tags"]["lore"]
            meta = Json_Post["tags"]["meta"]
            
        locked_tags = Json_Post["locked_tags"]
        change_seq = Json_Post["change_seq"]

        class flags:
            pending = Json_Post["flags"]["pending"]
            flagged = Json_Post["flags"]["flagged"]
            note_locked = Json_Post["flags"]["note_locked"]
            status_locked = Json_Post["flags"]["status_locked"]
            rating_locked = Json_Post["flags"]["rating_locked"]
            deleted  = Json_Post["flags"]["deleted"]
            
        rating = Json_Post["rating"]
        fav_count = Json_Post["fav_count"]
        sources = Json_Post["sources"]
        pools = Json_Post["pools"]

        class relationships:
            parent_id = Json_Post["relationships"]["parent_id"]
            has_children = Json_Post["relationships"]["has_children"]
            has_active_children = Json_Post["relationships"]["has_active_children"]
            children = Json_Post["relationships"]["children"]


        approver_id = Json_Post["approver_id"]
        uploader_id = Json_Post["uploader_id"]
        description = Json_Post["description"]
        comment_count = Json_Post["comment_count"]
        is_favorited = Json_Post["is_favorited"]

    return post

'''
while True:
    inp = input("What U want 2 do? \nS: Search \nR: Recent \nG: Get post by ID \n \n")
    if inp == "r":
        inp = input("What is the post limit?\n")
        
        print(recent(int(inp))[1].file.url)

    if inp == "s":
        tags = []
        while True:
            inp = input("What u wana do?\na: add tag\ns: search\nt: current tags\n")
            if inp == "a":
                inp = input("What tag u wana add?\n")
                tags.append(str(inp))
            if inp == "s":
                inp = input("what page do U want?\n")
                print("\n Searching...\n")
                print(search(tags, page=int(inp))[1].file.url)
                break
            if inp == "t":
                print(tags)
    if inp == "g":
        inp = input("what is post id?\n")
        print(get_post(str(inp)).file.url+'\n')'''
        
           
        




