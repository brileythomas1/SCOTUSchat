## SQL Database
The most important aspect of this project I should first discuss is my SQL database, titled scotus.db. It is a step up in complexity from Finance, now sporting three tables when my implementation in Pset 9 only had one. These tables are "users", "comments", and "posts" respectively. Users store information about users on the website, containing their username (string), password hash (string), id (integer), and moderator status (boolean). Throughout my implementation, I always reference users by their id, which is set to autoincrement in the settings of my database and is thus unique for each and every user. Username and password hash are fairly self-explanatory, sporting the same purpose as in Finance. The moderator column is something I will explain more in a later paragraph.

Next are the comments and posts tables. These are fairly similar, both sporting columns to store message (string), user_id (integer). Comments contains post_id to reference the post that they are replying to. The posts table also contains an additional title (string) column to store a title, an image (string) column to store the path to an image for each post that has one, and both posts and comments contain their own unique ids for referencing specific posts and comments in the database. Full information on this database can be seen by accessing scotus.db through phpLiteAdmin (done by right-clicking scotus.db in VS Code)

## Account System
The first feature to mention (and one I will gloss over) is the account system. Users can register, log-in, log-out, and change their password. Most of this is ripped straight from my implementation of Finance, so I don't believe full explanation is necessary. There are two notable differences, however. First is a new password complexity requirement. If a user tries to input a password less than eight characters, they will receive an apology (error message). I do this in order to preserve the security of the userbase. Although there is certainly more that could be done here, such as requiring a certain amount of uppercase, lowercase, numerical, or special characters, I felt that, for a simple forum with no sensitive personal information, eight characters was a sufficient solution. I also prevent common non-sense passwords including "password" and "12345678". Considering just how common these passwords are, I felt it was in the best interest of user security to prevent their usage, but it is by no means an exhaustive list. This is not a website for your bank or your Amazon account, and at the end of the day, the user is ultimately responsible for their own security. If a user decides to re-use their password across multiple websites, for instance, there is no way to prevent that. Requiring eight characters and preventing common passwords is a compromise that gives users the choice of not having to memorize something potentially confusing or extraordinarily random (at the cost of being less secure for them) but still forces them to keep their account relatively secure.

The second notable difference regarding my account system is being able to change your password. I implemented this as my personal touch in Finance, but I felt it was worth mentioning regardless since it isn't included in the base code. Again, the same complexity rules apply when a user sets a new password. I require a user to input their old password, input a new password, and then confirm the new password. This is fairly basic and simply updates the user's password hash in the database assuming they enter their old password correctly, input the confirmation of their new password correctly, and follow the password complexity rules. I decided to port this feature over from Finance for a few reasons. Firstly, allowing a user to change their password is a fundamental aspect of just about any modern website with an account system. Secondly, many experts recommend changing your password frequently to maintain account security. And third, I already had it done, so there was no reason not to just copy it over when it can only be a positive on my account system by giving the user more options to work with.

## Making a Post
Now moving on to the standout feature of my website, which is the forum section. First, I will discuss how posts are actually made on the forum. This is contained in the "/post" route starting in line 58 of app.py. Making a post requires two parts with one optional part: uploading an image. If a user doesn't put in a required part, an apology is returned. This helps keep the forum organized to a bare minimum. If the forum was full of blank posts, there is more potential for spam. This also helps makes my search feature more useful by requiring a user to have more words in their post and thus making it more searchable, and I will discuss this later. Notably, users can upload an image to their post. I notably limit users to just one image. I do this for a few reasons. Firstly, this forum should mostly be based around discussion. Unlike a forum dedicated to say, photography, images should not be an essential component, but I believe it can still be helpful in specific circumstances (i.e. trying to explain the aspects of a case).


## Display of Posts
There are two different ways in which posts are displayed. First is what I will call the "overview" of the forum, which is contained in the "/forum" app route in app.py starting on line 209. This route works pretty similar to how I implemented the index route in Finance. I first pull all data from the posts table, create a list which will store a dict for each post, and then store relevant information about each post in the key value pairs of each dict. Each dict is then appended to the list. I pass this list into the HTML template for forum.html and then display the contents of each dict in a table. This displays a table of each post to the user where they can see the user who made the post, the number of comments, the title, and the time the post was made. I implemented it in this way because I was already familiar with how to do so from Finance and a table provides a clean and consistent way to display every post. Additionally, users can click on the title of a post to get a more in-depth view of that particular post, and they can also click on the name of the user who made the post to view that user's profile, which I will get to later.


## In-Depth View of Posts
The more in-depth view of a post is contained in the "/view/id" app route starting on line 238 of app.py, where "id" is the post_id of the post the user wants to view. This is another step up from Finance by allowing dynamic links based on the post_id. The link varies depending on which post the user is viewing, and the post_id in the link is what determines what information to pull in the database for that particular post. The route works similarly to "/forum". All the data for the particular post is stored into their own variables. There is another variable, del_check, which is used for deleting posts which I will get to later. In view, users have the ability to delete their own post. Then, each comment for that specific post is stored in a dict of key-value pairs for all the relevant information of that comment (message, username, timestamp, etc.). All of these dicts are appended to the list "post_comments". Another aspect worth mentioning is the key "del_c_check" which determines whether the user in the current session can delete the comment depending on if they made the post or if they are a moderator. This is implemented in the HTML, where there is an if statement which checks whether this variable is set to true for each comment. If so, a "Delete Comment" button will appear to the user.

The view route also handles making new comments on a post through its POST request. At the bottom of the page in the view.html, there is a place for any user to make a reply. This reply is fed into the POST request and stored in variable "comment". After checking if the comment is empty and returning an apology if it is, then the new comment is inserted into the comments database with all its relevant info (the message, user_id of the user who made it, post_id, and timestamp). It then returns a page letting the user know their reply was successful.

## Deleting Posts and Comments
The next thing to discuss are the "/delete/id" and "/delete/comment/id" routes. Although these two routes share similar code, I choose to separate them to differentiate between post ids and comment ids. In these routes, I first check if the post or comment actually exists, and if it doesn't, I return an apology. Next, I check whether the user has the ability to actually delete the post or comment. This means that they must be a moderator or they made the post or comment. The del_check and del_c_check variables in my view.html are what control whether the buttons to delete a post or comment are actually displayed to the user depending on this status. Nevertheless, this route still double checks whether a user should be able to delete the post or comment in question so a can't just change the URL to delete a specific post or comment. If a user tries to do this, an apology is returned. Otherwise, the post (and all its accompanying comments) or comment is deleted from the database. This would also be a good time to discuss the moderator functionality on my site.

## Moderator System
One of the less visible but more important features of my website is the use of content policing through moderators. Moderators are specially designated users by someone with backend access to the database (i.e. me). This is designated by a boolean value for each user in the database. There is no way for a user to make themselves a moderator without backend access (assuming no SQL injection attack, which is prevented using placeholders). Moderators have the ability to delete any post and any comment as they wish.

I made several considerations in using a human form of moderation. I originally intended to develop an automated filter. This would supposedly operate similar to what we did in the psets Recover and DNA where we were reading data from a file. Presumably, you could make a text file of curse words and then scan the entire post or comment looking for matches with words in that file. This presented a personal problem when thinking about this. Firstly, I didn't feel entirely comfortable having a file in this project full of as many curse words as I could think of. Although I think an automated filter is absolutely valuable in real world applications, for the purposes of this project, I don't think it is entirely necessary on a smaller-scale forum rather than a massive, more difficult to moderate website. Plus, there are numerous problems an automated filter has. Consider when a user uses characters like '_', ' ', '.', or others to attempt to bypass the filter while still leaving the word easily visible. Additionally, there is the problem where words or phrases that have a curse word coincidentally embedded in them will be caught by the filter. Consider a situation where a user is named "Dick" (as in, Richard) and someone else is attempting to refer to them in a post. Or where a Supreme Court case about a particularly sensitive topic (say, whether hate speech should be permitted under the First Amendment) comes up and users want to discuss examples. An automated filter simply lacks the context to handle these situations. A human method is more foolproof at the expense of being slower to respond. This is a trade-off I'm willing to make for a forum with a smaller and likely more tight-knit community that is more likely to be specifically engaged and interested in the topic compared to a large, visible website with much more traffic. The audience of this website is also naturally going to be older by virtue of what it is about, so an older audience being exposed to adult/inappropriate content is generally less of an issue than on a website for kids for instance. Therefore, a curse word here and there is unlikely to have a substantial impact on the way it operates or the user base. Additionally, an automated filter would be unable to catch inappropriate images without a serious upgrade (as in, AI-driven image detection), while a moderator would easily be able to catch this.

This is not to say that the human-driven moderation approach is flawless. For one, there is the problem of subjectivity. What one user finds abhorrent may be fine to another user. There is also the potential for abuse of power. A moderator who I appoint Additionally, I, as the site owner, am always in complete control at the end of the day. I have complete privilege to remove or add moderators as I see fit, so a particular moderator causing problems could be easily replaced. I feel like this is where the feedback form comes in. If a user is having a problem where their posts are being removed for what they believe to be no reason, I can easily investigate. I also notably prevent a moderator from having the ability to delete or ban a user. For a small forum focused on a niche topic, I believe that instances where a user should be banned should be handled carefully.

## Profile Section
The profile section has several features. A user can view the profile of any other user. Here, they can see the user's profile picture, username, id, whether they are a moderator or not, and bio. You can update your bio on your own profile and read others' bios. I chose to implement this feature in order to foster more community in the forum. In this way, users can learn about each other and help to develop a tight-knit community. I feel this to be extremely important in a forum that is inherently political. If users are in the middle of a heated political debate, the biography is still a reminder that there is a human on the other side of the screen and to treat each other with respect. This is what I believe makes my website different from other places of political discourse online. It is anonymous enough where anyone can make their own username and discuss topics without fear of personal reproach or judgement, but there still exists reminders through the profile picture and biography where users can show a more human side instead of simply being a screen that is easier to attack. The profile section also shows all posts made by that user. I implement this in a very similar way to how I implement the "/forum" route, but this time, I only pull the posts where the user_id matches that of the profile's id.

## Image Upload
The most challenging aspect of this project for me was likely the image upload system. This is used for uploading images to posts and for users to set their profile pictures. This uses file uploading features from Flask, of which I borrowed code from Flask's documentation website here: https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/. Very importantly, I set a file upload limit of 2 MB, done on line 25 of app.py. Not having this could be disastrous: a user could upload an absolutely massive image that could be larger than the server could support, potentially shutting down my whole website. I also only allow .png, .jpeg, and .jpg file extensions. This is done in two places: first in the HTML implementation of the file upload, where the user's browser will only allow them to upload files of this extension (line 20 on post.html and line 12 on profile_pic.html), and I also check the extension once again when it is passed into my code (lines 82 and 450 in app.py). I do not want the user uploading all kinds of random files to my website and taking up server space, so I double check to prevent this occurrence in case a user is able to bypass the browser restriction.

I originally intended to have users simply paste a link to an image in a textbox, store that in my database, and then pass that link into my HTML in the image tag. However, this led to several problems. First of all, there was no way to verify that the link a user inputted was actually a valid image. A user could input any link they want. I solve this with an upload feature that specifically only permits image files while also accounting for the contingency where a user simply doesn't want to upload an image. This is much more specific in terms of what I'm permitting the user to do and takes more control out of the user's hands, which is better for me because it limits the number of possibilities I have to account for. The second problem with this link implementation is that image links are often temporary. If the site storing the image goes down or deletes the image from their server, it is gone and the user is left without an image that was once there. I solve this problem by storing images on the server. You can see all images stored in the "static/images" directory in my project. I rename files by the id of the user or post id of the post (lines 85 and 454 in app.py). The difference is denoted by the file name of posts being "post_id" while the filename for users is simply the user's id. This keeps my filebase organized and alows a consistent way to pass files into my HTML. It also prevents accidentally overwriting previously uploaded images with the same file name. The one exception to this is when a user wants to change their profile picture if they've previously set it, and this helps to conserve server space by overwriting data that is no longer in use. The way that I'm able to call images through HTML is by storing the path to the image in my database and then putting that path in the "src" attribute of an image tag.

## Searching Forum
After this, I have the search forum page, contained in the "/search" route. This allows the user to search through the forum for a particular post. If a GET request is sent, the page to search for a post is displayed. If a POST request is sent, then the user's search is stored in a variable. After this, it works very similar to the "/forum" route where I make a dict for each post and then store each dict in a list, with the only difference being the posts that we pull. Instead of pulling all posts, we only pull those where the title or message is "LIKE" (in SQL) the search term the user inputed. It checks for any occurrence of the phrase the user inputed in any title or message and displays all posts that match.

## News Page
The last section of note is my news page. I implement this using something called RSS 2 HTML via the website rss.bloople.net. This website converts the RSS feed of a source into embedded HTML. An RSS feed is basically just a format for content that is updated frequently where content distributors can push new content out to the feed. This allows my news page page to be dynamically updated.

Something else that was very important to consider when making this page was bias. I originally considered an approach where moderators would be able to upload news posts for every other user to see and delete them at will. This has two main problems. First of all, it isn't as dynamic, so news could be updated slowly if moderators aren't as active. Secondly, there adds the potential for bias. In the modern political climate, I want to avoid this problem as much as possible. My RSS feed is derived from Google News, which is a news aggregator that tends to provide an array of diverse sources, so this helps to limit bias. I don't want users to think that moderators of the site are attempting to spin a particular narrative, so I felt that sourcing news out to a third party was the safest option in terms of maintaining trust of the userbase.

## Miscellaneous Pages
Moving on to the more miscellaneous, less technical aspects of my website. First of all is the home page, which is what users are first greeted to when they log-in. This page is just static HTML with an introduction to the website and also has a photo of the justices. I also have an about page. Not much to see here either, just a bunch of static HTML text that is a place for users to learn more about the Supreme Court, the website, and myself. I also have a feedback page, which is simply an embedded Google form for users to provide feedback on the site. I chose not to implement this directly into the website because Google has (in my opinion) more user-friendly tools for organizing data compared to SQL with things like Google Sheets. There is also my calendar page. This is an embedded Google Calendar with dates of oral arguments, conferences, and other important events of the Supreme Court. The data here is sourced from SCOTUSblog.com/events, but I importantly insert this data manually into my own Google Calendar. In case SCOTUSblog.com ever goes down for any purpose, I still effectively have a backup of that data which my userbase can rely on. This makes my website more self-sufficient and independent.