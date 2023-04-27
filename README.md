# Coding Website

![Image showing Website on different devices](assets/readme.images/camocode-am-i-responsive.png)

[View the live site here](https://camocode.herokuapp.com/)

A social media website for developers that allows people to create simple text posts as well as share code, or ask for help!

## Table of Contents


## Project Goals

The main aim is to give users a platform to post code snippets and get help/feedback from other users.

The target audience is developers or anyone who enjoys coding.

### User goals

* Enjoyable experiance on the site.
* To be able to create an account.
* To be able to customize my account.
* To be able to create posts.
* To be able to edit posts.
* To be able to view posts.
* To be able to delete posts.
* To be able to comment on posts.
* To be able to view list of comments.

### Developer goals

* Create a clean responsive interactive website for milestone project.
* An easy to navigate site.
* A project that would be good enough to go in a portfolio.
* To offer a social media network specifically designed for developers.
* To allow users to create posts or comment on posts, both of which provide an option to include code content.
* To allow users to view posts or assist others with comments.
* To allow users to edit their own posts.
* To allow users to delete their own posts.

## User Experience - UX

### Scope

#### Potential/Existing User Stories

* I want to know the site's purpose from the first page.
* I want to be able to register for a new account.
* I want to be able to log in to my newly created account.
* I want to be able to view my profile.
* I want to be able to view my posts.
* I want to be able to view other people's posts.
* I want to be able to create a new posts.
* I want to be able to edit my posts.
* I want to be able to delete my posts.
* I want to be able to create new comments/reply to posts.
* I want to be able to view all comments on a post.
* I want to be able to edit my account.
* I want to be able to delete my account.

#### Site Owner User Stories

* I want potential users to know from the start what the site's purpose is.
* I want potential users to be able to register for an account.
* I want existing users to be able to be able to login.
* I want logged in users to be able to create new posts.
* I want logged in users to be able to view other people's posts.
* I want logged in users to be able to edit their posts.
* I want logged in users to be able to delete their own posts.
* I want logged in users to be able to add comments.
* I want logged in users to be able to view other people's as well as their own comments.
* I want logged in users to be able to edit profile info.

### Design Choices

#### Fonts

* The fonts used were taken from [Google Fonts](https://fonts.google.com/)
* The fonts Roboto and Lato were used because they are popular and therefore more recognisable.
* The font sans-serif was put in as a back up.

#### Icons

* Icons used were taken from [Font awesome](https://fontawesome.com/)
* All icons used were chosen because they are easily recognisable to clients.

#### Colours

![Colour Palette image](assets/readme.images/camocode-colours.png)

* The primary colour choices of onyx and timberwolf were chosen for the navbar and background because they have a clean clear aspect while contrasting well with each other.
* Taupe was used for the code block background and light sea green for buttons.
* Black, grey and white were chosen to make the writing stand out against the background.

#### Styling

* I have used Materialize throughout the site primarily to assist with design and responsiveness and added my own custom styling.
* PrismJS was used to provide styling and colour for the code area.

#### Images

* The only images I used were for the social media links, credited in the credits section.

## Wireframes

## Features

The coding website is designed to strictly adhere to accessibility guidelines across all pages, with easy navigation between them. Device responsiveness approach taken throughout project.

### Front-End Structure

#### Navbar and Footer

* The navbr and footer were taken from materialize and styled to suit needs. The same navbar and footer used on every page for easy navigation. Added social media links to the footer.

![Navbar Image](assets/readme.images/camocode-navbar.png)

![Footer Image](assets/readme.images/camocode-footer.png)

The website is split into 9 pages, stored in 12 html files. 

1. Home - home.html
- Landing page, and first page user encounters when they visit the website, includes a list of the most recent posts.

![Home Image](assets/readme.images/camocode-home.png)

2. Register - register.html
- The user is able to register an account to the website.

![Register Image](assets/readme.images/camocode-register.png)

3. Log In - login.html
- The user is able to log in to the website using an existing account, otherwise they are invited to create a new one. Once logged in they are redirected to the home page.

![Login Image](assets/readme.images/camocode-login.png)

4. Profile - profile.html
- Available only to the user logged in via which they can view their account info, provides links via which user can change their profile info, and logout or delete their account.

![Profile Image](assets/readme.images/camocode-profile.png)

5. Update Profile - update_profile.html 
- Available only to the user logged in, allows user to change edit their account details.

![Update Profile Image](assets/readme.images/camocode-updateprofile.png)

6. New Post - new_post.html
- Providers a form which users can populate to create a new post. In addition to the standard text input fields, this also contains a dropdown box which the user can select the type of language to post code into the code window.

![New Post Image](assets/readme.images/camocode-newpost.png)

7. Post - post.html 
- View of a single post and it's comments. If the current user is the owner of the post then a edit and delete button appear under the post.

![Post Image](assets/readme.images/camocode-post.png)

8. Update Post - update_post.html
- Utilizes similar code to the New Post page, but instead the form presented is populated with the post's current content that can be changed and reposted.

![Update Post Image](assets/readme.images/camocode-updatepost.png)

9. Comment - comment.html
- Utilizes similar code to the New Post page, but instead the form presented is populated with the a body element and a dropdownbox if the user wants to add a code snippet with there comment.

![Comment Image](assets/readme.images/camocode-comment.png)

### Back-End Structure

* Built with Flask using Postgresql for the database.
The application structure is as follows:
* routes.py - contains all routes for the website.
* models.py - contains all schemas for the website.
* init.py - contains all database info for the website.
* env.py - contains secret password and other info for the website.
* forms.py - contains all forms for the website.
* templates - contains all .html files for the website.
* static - contains all css, js and images for the website.
* Application is created and setup by running app.py.

Additional gadgets used in back-end:

* Flask login - For all login/logout capabilities.
* Flask wtf/wtforms - For all form functions.
* werkzeug.security - For password checks.
* datetime - For date and time stamps.
* UglifyJS - For JS files minificatin and compression.
