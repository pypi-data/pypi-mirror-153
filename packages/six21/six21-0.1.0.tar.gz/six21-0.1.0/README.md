
# six21

A python api wrapper for e621.net




## Features

- Getting Recent Posts From e6
- Searching For Posts
- Getting Random Posts
- Getting An Post By Its Id


## Usage 
To use you need to have requests and json packages installed

First, import into your project
```python
from six21 import e621
```
[optional]
If needed set User to the name of your project
```python
e621.Set_User("NAME_OF_PROJECT")
```
<Searching>

Searching will return a list of posts that fit the criteria that the tags provide  
Usage:
```python
e621.search(tags, page, limit)
```
- ```tags``` Is what keywords you want to search for are and should be given in a list  
- ```page``` is what page you want to go to during the search and should be given in a int  
- ```limit``` is the limit to how many posts you want to retrieve  


<Recent Posts>

Getting recent posts will return a list of posts that have been most recently posted to e6  
Usage:
```python
e621.recent(limit)
```
- ```limit``` is the limit to how many posts you want to retrieve  

<Random>

Returns one random post from e6  
Usage
```python
e621.random()
```
<Get Post>

Returns the post from the given Id  
Usage:
```python
e621.get_post(Id)
```
- ```Id``` is the Id of the post you want it to return



## Post Object

<A single post object is as follows>  
id: The ID number of the post.  <br />
created_at: The time the post was created in the format of YYYY-MM-DDTHH:MM:SS.MS+00:00.  <br />
updated_at: The time the post was last updated in the format of YYYY-MM-DDTHH:MM:SS.MS+00:00.  <br />

file (subclass)

    width: The width of the post.
    height: The height of the post.
    ext: The file’s extension.
    size: The size of the file in bytes.
    md5: The md5 of the file.
    url: The URL where the file is hosted on E6

preview (subclass)

    width: The width of the post preview.
    height: The height of the post preview.
    url: The URL where the preview file is hosted on E6

sample (subclass)

    has: If the post has a sample/thumbnail or not. (True/False)
    width: The width of the post sample.
    height: The height of the post sample.
    url: The URL where the sample file is hosted on E6.

score (subclass)

    up: The number of times voted up.
    down: A negative number representing the number of times voted down.
    total: The total score (up + down).

tags (subclass)

    general: A list of all the general tags on the post.
    species: A list of all the species tags on the post.
    character: A list of all the character tags on the post.
    artist: A list of all the artist tags on the post.
    invalid: A list of all the invalid tags on the post.
    lore: A list of all the lore tags on the post.
    meta: A list of all the meta tags on the post.

locked_tags: A JSON array of tags that are locked on the post.  <br />
change_seq: An ID that increases for every post alteration on E6 (explained below)  <br />
flags (subclass)

    pending: If the post is pending approval. (True/False)
    flagged: If the post is flagged for deletion. (True/False)
    note_locked: If the post has it’s notes locked. (True/False)
    status_locked: If the post’s status has been locked. (True/False)
    rating_locked: If the post’s rating has been locked. (True/False)
    deleted: If the post has been deleted. (True/False)

rating: The post’s rating. Either s, q or e.  <br />
fav_count: How many people have favorited the post.  <br />
sources: The source field of the post.  <br />
pools: An array of Pool IDs that the post is a part of.  <br />
relationships (subclass) 

    parent_id: The ID of the post’s parent, if it has one.
    has_children: If the post has child posts (True/False)
    has_active_children: children A list of child post IDs that are linked to the post, if it has any.

approver_id: The ID of the user that approved the post, if available.  <br />
uploader_id: The ID of the user that uploaded the post.  <br />
description: The post’s description.  <br />
comment_count: The count of comments on the post.  <br />
## Usage Example

Below is a script that will grab a random post then print the post id, allong with the raw file url:
```python
from six21 import e621 #Import Package

random_post = e621.random() #Get a random post

post_id = random_post.id #From the post get its Id

post_file_url = random_post.file.url #From the post get its Url

print("Post Id: {Id} \nFile Url: {Url}".format(Id = post_id,Url = post_file_url )) #Print Id and Url
```
