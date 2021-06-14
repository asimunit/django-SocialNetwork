##Project
Create a clone of social media in Django. The site should be interactive and smooth.
 
Features:
(Django and Python)
1.Login Page where users can log in.
2.Sign Up page where a new user can enter details.
3.After the user is authenticated it can add or update its profile picture, password, and its personal details(Age, Gender, DOB, profile pic etc.).
4.Admin page where superuser can access all the details.
5.Can add or remove friends(other users) and also search any user by its name or email address.

NLP:
1.After the user is logged in, give an option to create or edit a post. A user can enter a maximum of 300 words in the text box. 
2.When a user submits the post, check if that post is a duplicate of any other post or not. If a user has already posted a similar post, mark the new post as a duplicate of that post.
a.Similarity should only be checked with the original post, not the post which is already marked as duplicate.
b.Give an option to the user to view all posts or only root/original posts.
c.Also, give an option to sort the post by update date.
3.A user can see its friend post in the feed. Although he/she can’t edit or delete the post. It will be in read-only mode.
4.Use a pre-trained NER model to predict the companies/people/locations present in the post.
5.After the similarity task is done, use a model to predict if the post is obscene/vulgar. (Will provide you with the required data)
