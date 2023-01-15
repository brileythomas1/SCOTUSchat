import os
import datetime

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from werkzeug.utils import secure_filename

# Configures folder for uploaded files to path static/images/ (used for post images and profile pictures)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/images')

# Sets the allowed file extensions for file uploads to image formats .png, .jpg, and .jpeg
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Configure application
app = Flask(__name__)

# Sets upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Sets maximum size of files to 2 MB
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///scotus.db")

# Function that determines whether a file has a valid format and extension by checking if the extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Returns user to home/splash page when they click on "SCOTUSchat" icon
@app.route("/")
@login_required
def index():
    return render_template("home.html")


# Allows user to make a new post on the forum
@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    if request.method == "POST":

        # Takes title from the user
        title = request.form.get("title")

        # If the user didn't input a title, return apology
        if title == "":
            return apology("Please enter a non-empty title")

        # Takes post from what user inputed
        message = request.form.get("message")

        # If the post is blank, return apology
        if message == "":
            return apology("Please enter a non-empty message")

        # Large portion of code below taken from this source: https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
        # Gets file from what user uploaded
        file = request.files['post_file']

        # If user inputed a file and it is of a valid format
        if file and allowed_file(file.filename):

            # Renames file to be in the format "post_<post_id>.<file extension>"
            file.filename = "post_" + str(int(db.execute("SELECT COUNT(post_id) FROM posts")[0]["COUNT(post_id)"]) + 1) + "." + file.filename.rsplit('.', 1)[1].lower()

            # Saves file to server
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

            # Adds new info about new post (title, message, time, id of the user who submitted it, and image path) to database
            db.execute("INSERT INTO posts (title, message, timestamp, user_id, image) VALUES(?,?,?,?,?)", title, message, datetime.datetime.now(), session["user_id"], "static/images/" + file.filename)

            # Lets user know their post submission was successful
            return render_template("posted.html")

        # If the user inputed a file but of an invalid format, return apology
        if file and not allowed_file(file.filename):
            return apology("Invalid file extension")

        # If the user didn't input a file, insert their post into the database but set image value to "0"
        db.execute("INSERT INTO posts (title, message, timestamp, user_id, image) VALUES(?,?,?,?,?)", title, message, datetime.datetime.now(), session["user_id"], "0")
        return render_template("posted.html")

    else:

        # If method is GET, loads the page for the user to submit their post
        return render_template("post.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Loads feedback form for user
@app.route("/feedback")
@login_required
def feedback():
    return render_template("feedback.html")


# Loads news page for user
@app.route("/news")
@login_required
def news():
    return render_template("news.html")


# Loads about page for user
@app.route("/about")
@login_required
def about():
    return render_template("about.html")


# Loads calendar page for user
@app.route("/calendar")
@login_required
def calendar():
    return render_template("calendar.html")


# Lets user register for a new account
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Takes username from what user inputed
        username = request.form.get("username")

        # If the username is blank, return apology
        if username == "":
            return apology("Please enter a username")

        # If there is already an existing username in the database, return apology
        duplicates = db.execute("SELECT username FROM users WHERE username = ?", username)
        if len(duplicates) != 0:
            return apology("Username already taken. Please try again")

        # Takes password from what user inputed
        password = request.form.get("password")

        # If the password is empty, return apology
        if password == "":
            return apology("Please enter a password")

        # If the password is less than eight characters, return an apology
        if len(password) < 8:
            return apology("Please enter a password with at least 8 characters")

        # Prevents user from entering very common passwords
        if password == "12345678" or password == "01234567" or password == "password" or password == "abcdefgh":
            return apology("Please enter a more secure password")

        # Takes confirmation from what user inputed
        confirmation = request.form.get("confirmation")

        # If user didn't enter confirmation, return apology
        if confirmation == "":
            return apology("Please confirm your password")

        # If the confirmation doesn't match password, return apology
        if confirmation != password:
            return apology("Passwords do not match")

        # Insert new user's info into table users in the database
        # User is automatically set to not being a moderator by default; only someone with backend access to the database can decide moderators
        # Note: user_id is not seen below but is an autoincrementing value
        db.execute("INSERT INTO users (username, hash, moderator) VALUES(?,?,?)", username, generate_password_hash(password), False)

        # Get the new id from the user and store it in the existing session
        newid = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = newid[0]["id"]

        # Redirect user to page telling them that they registered successfully
        return render_template("registered.html")

    else:

        # If method is GET, loads the page for the user to register
        return render_template("register.html")

# Loads all current posts to the user
@app.route("/forum")
@login_required
def forum():

    # Stores info about every post
    posts = db.execute("SELECT * FROM posts")

    # display_posts stores dicts of data pertaining to each post
    display_posts = []

    # Every post has its relevant data stored in a dict that is then appended to display_posts
    for post in posts:
        temp = {}

        # Data about the post stored in key value pairs in a dict for each post
        temp["title"] = post["title"]
        temp["message"] = post["message"]
        temp["username"] = db.execute("SELECT username FROM users WHERE id = ?", post["user_id"])[0]["username"]
        temp["timestamp"] = post["timestamp"]
        temp["post_id"] = post["post_id"]
        temp["user_id"] = post["user_id"]
        temp["count_comments"] = db.execute("SELECT COUNT(comment_id) FROM comments WHERE post_id = ?", post["post_id"])[0]["COUNT(comment_id)"]

        display_posts.append(temp)
    return render_template("forum.html", display_posts=display_posts)


# Allows more in-depth information about a specific post (shows the message, comments, and post image if available)
# Also controls a user making a comment when sent a POST request
@app.route("/view/<id>", methods=["GET", "POST"])
@login_required
def view(id):
    if request.method == "GET":

        # Get the info about the specific post the user is viewing using the post_id
        post = db.execute("SELECT * FROM posts where post_id = ?", id)
        username = db.execute("SELECT username FROM users WHERE id = (SELECT user_id FROM posts WHERE post_id = ?)", id)[0]["username"]
        pfp = db.execute("SELECT pfp FROM users WHERE id = (SELECT user_id FROM posts WHERE post_id = ?)", id)[0]["pfp"]
        time = post[0]["timestamp"]
        title = post[0]["title"]
        message = post[0]["message"]
        user_id = post[0]["user_id"]
        image = post[0]["image"]

        # If the user in the current session made the post or is a moderator, they are able to delete the post (denoted by del_check being True)
        if session["user_id"] == post[0]["user_id"] or db.execute("SELECT moderator FROM users WHERE id = ?", session["user_id"])[0]["moderator"] == True:
            del_check = True
        else:
            del_check = False


        # Gets comments for the post
        comments = db.execute("SELECT * FROM comments WHERE post_id = ?", id)

        # List of dicts to store all comment info
        post_comments = []

        # Creates a dict of relevant info for each comment (the message, user who made it, and timestamp)
        for comment in comments:
            display_comments = {}
            display_comments["message"] = comment["message"]
            display_comments["username"] = db.execute("SELECT username FROM users WHERE id = (SELECT user_id FROM comments WHERE comment_id = ?)", comment["comment_id"])[0]["username"]
            display_comments["timestamp"] = comment["timestamp"]
            display_comments["comment_id"] = comment["comment_id"]
            display_comments["user_id"] = comment["user_id"]
            display_comments["pfp"] = db.execute("SELECT pfp FROM users WHERE id = (SELECT user_id FROM comments WHERE comment_id = ?)", comment["comment_id"])[0]["pfp"]

            # If the comment was made by the user in the current session or the user is a moderator, they can delete their own comment
            if comment["user_id"] == session["user_id"] or db.execute("SELECT moderator FROM users WHERE id = ?", session["user_id"])[0]["moderator"] == True:
                display_comments["del_c_check"] = True
            else:
                display_comments["del_c_check"] = False

            post_comments.append(display_comments)

        return render_template("view.html", post_comments=post_comments, username=username, time=time, title=title, message=message, id=id, del_check=del_check, user_id=user_id, image=image, pfp=pfp)
    else:
        # Store the user's comment
        comment = request.form.get("reply")

        # Checks if the comment is empty and sends apology if it is
        if comment == "":
            return apology("Please enter a non-empty comment")

        # Inserts contents of new comment into table comments
        db.execute("INSERT INTO comments (message, user_id, post_id, timestamp) VALUES(?,?,?,?)", comment, session["user_id"], id, datetime.datetime.now())

        # Lets user know their comment submission was a success
        return render_template("reply_success.html")

# Controls post deletion
@app.route("/delete/<id>", methods=["POST"])
@login_required
def delete(id):

    # Checks if the post the user is trying to delete exists; returns apology if not
    check = db.execute("SELECT user_id FROM posts WHERE post_id = ?", id)
    if len(check) == 0:
        return apology("You can't delete a post that hasn't been made!")

    # If the user in the current session is a moderator or made the post, the post and its comments are deleted from the database
    if db.execute("SELECT moderator FROM users WHERE id = ?", session["user_id"])[0]["moderator"] == True or db.execute("SELECT id FROM users WHERE id = (SELECT user_id FROM posts WHERE post_id = ?)", id)[0]["id"] == session["user_id"]:
        db.execute("DELETE FROM posts WHERE post_id = ?", id)
        db.execute("DELETE FROM comments WHERE post_id = ?", id)
        return render_template("delete_success.html")

    # If the user attempts to delete a post that isn't theirs and they aren't a moderator, return apology
    else:
        return apology("You can't delete a post you haven't made if you aren't a moderator!")

# Controls comment deletion
@app.route("/delete/comment/<id>", methods=["POST"])
@login_required
def delete_comment(id):

    # Checks if the comment exists; returns apology if not
    check = db.execute("SELECT user_id FROM comments WHERE comment_id = ?", id)
    if len(check) == 0:
        return apology("You can't delete a comment that hasn't been made!")

    # If the user is a moderator or made the comment, the comment is deleted
    if db.execute("SELECT moderator FROM users WHERE id = ?", session["user_id"])[0]["moderator"] == True or db.execute("SELECT id FROM users WHERE id = (SELECT user_id FROM comments WHERE comment_id = ?)", id)[0]["id"] == session["user_id"]:
        db.execute("DELETE FROM comments WHERE comment_id = ?", id)
        return render_template("delete_success.html")

    # If the user tries to delete a comment they haven't made and they aren't a moderator, return apology
    else:
        return apology("You can't delete a comment you haven't made if you aren't a moderator!")


# Allows user to change password
@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":

        # Gets user's current password hash
        rows = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

        # Gets user's input for old password
        old = request.form.get("old_password")

        # Compares current password hash and user's input for old password
        if not check_password_hash(rows[0]["hash"], old):
            return apology("Your old password is incorrect. Please try again")

        # Gets user's input for new password
        new = request.form.get("new_password")

        # If no new password was entered, return apology
        if new == "":
            return apology("Please enter a new password")

        # Checks if the new password is at least eight characters; returns apology if not
        if len(new) < 8:
            return apology("Please enter a new password of at least eight characters")

        # Checks if the new password is very common; returns apology if so
        if new == "12345678" or new == "01234567" or new == "password" or new =="abcdefgh":
            return apology("Please enter a more secure password")

        # Gets user's confirmation of their new password
        confirm = request.form.get("new_confirmation")

        # If their new password and confirmation aren't equal, return apology
        if confirm != new:
            return apology("New password does not match confirmation")

        # Update user's password hash with the hash of the new password
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new), session["user_id"])

        # Lets user know their password update was successful
        return render_template("success.html")

    # If submitted by GET request, display the page allowing user to change their password
    else:
        return render_template("change.html")


# Allows user to log-in
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# I used this guide for much of the code below: https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
# However, it is modified to fit the unique needs of this project and the SQL database
@app.route("/update_pfp", methods=["GET", "POST"])
@login_required
def update():

    # If submitted by GET request, display page for user to update their profile picture
    if request.method == "GET":
        return render_template("profile_pic.html")

    # If submitted by POST request, change user profile picture
    else:

        # Checks if the post request has the file part
        if 'file' not in request.files:
            return apology("No file part")
        file = request.files['file']

        # If user does not select a file, browser submits an empty part without filename
        if file.filename == '':
            return apology("No requested file")

        # If the user submitted a file and the file has a valid format and extension
        if file and allowed_file(file.filename):

            # Rename image to the user in the current session's id plus the existing file extension
            file.filename = str(session["user_id"]) + "." + file.filename.rsplit('.', 1)[1].lower()

            # Save image to server
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Update the database to set path of user's profile picture
            db.execute("UPDATE users SET pfp = ? WHERE id = ?", "static/images/" + file.filename, session["user_id"])

            # Let user know their profile picture update was successful
            return render_template("pfp_success.html")

        # If the user submitted a file but the extension or format is invalid, return apology
        if file and not allowed_file(file.filename):
            return apology("Invalid file extension")


# Used to handle linking in the layout; redirects user to the page for their profile
@app.route("/me", methods=["GET", "POST"])
@login_required
def me():
    return redirect("/profile/" + str(session["user_id"]))


# Displays profile info of every user and handles updating biography
@app.route("/profile/<id>", methods=["GET", "POST"])
@login_required
def profile(id):

    # Flag stores whether the profile is the user in the current session's own profile
    flag = False

    # If the profile id the user is trying to view is their own, set flag to true
    if str(id) == str(session["user_id"]):
        flag = True

    # If GET request was submitted, get all the info about the user with this specific profile id
    if request.method == "GET":
        user_info = db.execute("SELECT * from users WHERE id = ?", id)
        username = user_info[0]["username"]
        id = user_info[0]["id"]
        moderator = user_info[0]["moderator"]
        bio = user_info[0]["bio"]
        pfp = user_info[0]["pfp"]


        # Gets all the posts this specific user has made
        user_posts = []
        posts = db.execute("SELECT * FROM posts WHERE user_id = ?", id)
        for post in posts:
            temp = {}
            temp["title"] = post["title"]
            temp["message"] = post["message"]
            temp["username"] = db.execute("SELECT username FROM users WHERE id = ?", post["user_id"])[0]["username"]
            temp["timestamp"] = post["timestamp"]
            temp["post_id"] = post["post_id"]
            temp["user_id"] = post["user_id"]
            temp["count_comments"] = db.execute("SELECT COUNT(comment_id) FROM comments WHERE post_id = ?", post["post_id"])[0]["COUNT(comment_id)"]
            user_posts.append(temp)

        # Displays profile info to user
        return render_template("profile.html", username=username, moderator=moderator, bio=bio, id=id, pfp=pfp, user_posts=user_posts, flag=flag)
    else:

        # If user somehow attempts to modify profile info of a profile that isn't their own, return apology
        if flag == False:
            return apology("You cannot edit someone else's profile!")

        # Get biography from user input
        biography = request.form.get("bio")

        # If biography is blank, return apology
        if biography == "":
            return apology("Please enter a non-empty biography")

        # Update user in the current session's biography
        db.execute("UPDATE users SET bio = ? WHERE id = ?", biography, session["user_id"])

        # Let user know their update was successful
        return render_template("bio_success.html")


# Handles searching posts on the forum
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():

    # If GET request submitted, display page for user to search forum
    if request.method == "GET":
        return render_template("search.html")

    # If POST request submitted, display all posts matching what the user inputed
    else:

        # Gets what the user wanted to search for
        search = request.form.get("search")

        # Finds all posts where the title or message is similar to what the user wants to search for
        posts = db.execute("SELECT * FROM posts WHERE title LIKE ? OR message LIKE ?", "%" + search + "%", "%" + search + "%")

        # display_posts stores dicts of data pertaining to each post
        display_posts = []
        # Every post has its relevant data (title, message, timestamp) stored in a dict that is then appended to display_posts
        for post in posts:
            temp = {}
            temp["title"] = post["title"]
            temp["message"] = post["message"]
            temp["username"] = db.execute("SELECT username FROM users WHERE id = ?", post["user_id"])[0]["username"]
            temp["timestamp"] = post["timestamp"]
            temp["post_id"] = post["post_id"]
            temp["user_id"] = post["user_id"]
            temp["count_comments"] = db.execute("SELECT COUNT(comment_id) FROM comments WHERE post_id = ?", post["post_id"])[0]["COUNT(comment_id)"]

            display_posts.append(temp)

    return render_template("result.html", search=search, display_posts=display_posts)