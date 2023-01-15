**Video**: https://www.youtube.com/watch?v=1xOBL7T6BxQ


## Overview
My project is a website made using Flask, HTML, CSS, and Python. To run my website, type "cd 'folder_name'" in your terminal where 'folder_name' is a folder containing all files and folders in this project and then execute the command "flask run" into your terminal. A link will then display in your terminal. Copy and paste or click on this link and you should be able to see the website.

## Registration
The first thing you'll notice upon entering the website is that you must make an account. Click "Register" in the top right corner of the website. Make a username and enter a password with at least eight characters, then confirm that password. Note that you will receive an error message if your username is already taken or if your password isn't at least eight characters or is extremely common (i.e. passwords like "password" or "12345678"). In this case, please enter another username or password that fits the complexity rules.

After registering for an account, you will be automatically logged in and be brought to a page letting you know your registration was successful. You can click the SCOTUSchat icon in the top left or any of the other items in the navbar to navigate to another page.

## Welcome Page
If you click the "SCOTUSchat" icon in the top left, you'll be brought to the welcome page, titled "home.html". This page welcomes users to the website and has a photo of the current Supreme Court.

## Forum Page
Clicking the "Forum" item in the navbar directs you to a list of current posts on the forum. On this page, you can see the title of all posts currently made, the user who made them, the time the post was made, and the number of comments for each post. Any navigable links here are highlighted in blue. Note that you can navigate to any user's profile by clicking on their username. You can also navigate to a more in-depth view of a particular post by clicking that post's title.

## Viewing a Post and Submitting Replies
If you click a post's title, you will be put on the view page for that particular post. Here, you can see more details about the post including the message of the post and any replies on the post. On this page, you can also click the username of any user to take you to their profile. You can also make a comment to a post on this page. At the bottom of the page is a textbox. Insert your desired message and press the blue "Submit Reply" button. If your reply was successful, you will be directed to a page letting you know that your reply was successful. If not, please enter a reply that isn't empty. This is a measure to prevent spam.

## Viewing Reply and Deleting Comments
You can view your reply by going back to the forum page in the navbar and clicking the title of the post you made a reply on. At the bottom of the page, you will see the reply you made. Note that you can also delete your own comment by clicking the blue "Delete Comment" button underneath your comment. This will remove the comment from our database and the post. If your deletion was successful, you will be brought to a page letting you know that it was successful. If you go back to the forum page in the navbar and click that particular post again where you deleted the reply, then you will no longer see the reply on that post.

## Making and Deleting a Post
To make your own post, click "Make a Post" in the navbar. This will direct you to a page where you can enter a Title, Message, and Image for your post. Note that you are required to submit a non-empty title and message for your post for the submission to be successful. If you do not do so, you will receive an error message. You can also optionally upload an image from your computer to be embedded in the post. Note that you may only enter an image that is a .png, .jpg, or .jpeg format and there is a 2 MB file limit on uploads. If you wish to enter an image, upload it here and press the Submit Post button. If not, simply press the Submit Post button. If your post submission was successful, you will be directed to a page letting you know that your post was submitted. To view your post, click the "Forum" item in the navbar and your post will appear at the bottom of the page. You can click on your post's title to view your post's message or any replies made on the post. You can also delete the post by clicking the blue "Delete Post" button under your post in this page.


## Calendar Page
Click the "Calendar" item in the navbar to go to the calendar page. Here, you can view a calendar of upcoming Supreme Court Cases. Note that this calendar is only updated for the current month and the month in advance. The data this calendar is based off of can be found at SCOTUSblog.com/events.


## News Page
Click the "News" item in the navbar to go to the news page. Here, you will see a variety of links to recent articles about the Supreme Court sourced from various news sources and compiled by Google News. Click any blue link to read the article.


## Feedback Page
Click the "Feedback" item in the navbar to go to a page where you can submit feedback on SCOTUSchat to me. Type your feedback into the text box and press the "Submit" button in order to send feedback.


## Search Page
Click the "Search Forum" item in the navbar to go to a page where you can search the forum for a specific post. Input a search term and you will be redirected to a page with all posts where the title or message of the post contains your search term.


## About Page
Click the "About Website" item in the navbar to go to a page where you can learn more about the Supreme Court, the creator of the website, and the website.


## Logging Out
Click "Log Out" on the navbar to log out of your current account. You can log back in when logged out by inputting your username and password in the log-in page, which you can find by clicking "Log-In" on the navbar when logged out. Note: when logged out, you cannot access most of the website's features.

## Changing Your Password
Click "Change Password" on the navbar to change the password of your account. Input your old password in the first textbox, your new password in the second textbox, and then confirm your new password by typing it again in the third textbox. Note that your new password must match the password complexity rules by being at least eight characters long. If your password change is successful, you will be redirected to a page saying that your password change was successful.

## Viewing Your Profile
Click "My Profile" on the navbar to access your profile. Here, you can see your username, user id, profile picture, moderator status, and biography. Type in the textbox below "Update Bio" to update your biography. Your biography can be seen by any other users on the forum. Once you are done, click the blue "Save Bio" button to change your changes. If your biography change was successful, a page will display saying as such. You can click "My Profile" again in the navbar to view your new biography. You can also change your profile picture at the bottom of your profile page. Click the "Update Profile Picture" button and you will be redirected to a page where you can upload a profile picture. Upload an image file within the constraints provided (meaning that it must have a .jpg, .jpeg, or .png file extension and be under 2 MB). If your change was successful, you will be redirected to a page saying as such. You can view your new profile picture by going to "My Profile" again in the navbar.


## Moderator Functionality
Note that certain users on the website are designated as moderators. They can only be designated by someone with backend access to the database. Users who have this designation will show as such on their profile pages. On the "moderator" column, the value will display "Yes" if they are a moderator. Moderators can delete any user's post or comment at their discretion. This means that the forum is moderated, so do not enter any inappropriate content or content that is irrelevant to the discussion.


## Citations
I partially use code from a source in two different sections. First is in my file uploading for when uploading images to embed in posts or uploading images to be a user's profile picture. This code is partially derived from the Flask documentation found here: https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/. I modify this code to fit the specific needs of this project. This includes renaming the file the user uploads and storing the path to the file in my SQL database, two elements which are not present in the original documentation.

 I also use the Bootstrap template found at this website: https://www.bootdey.com/snippets/view/bs4-beta-comment-list for the CSS and format of the HTML of my "view.html" template in order to produce the particular appearance of the website when viewing a post. I modify this template in order to remove elements that I'm not using in my own project, such as the likes and dislikes, and add elements such as incorporating an image into the post if a user uploaded an image.

