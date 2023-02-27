# groupchat-webapp
This is a web application that users can create groups or chat rooms and other users can join and have conversation and share file within a group
# Tech Stack 
Python Flask, HTML, CSS, JQuery, bootstrap
# what to install
All dependencie must installed Python,flask, bcrypt, mysql-connector.
# modules
The web application has the following modules
1: Register/sign up module
2: Login/ sign in module
3: Create group module
4: chat module
# Register module
New users must create an account to start using the web app.
The form is a multi-step form from personal details, country & profession, group sign data and a profile picture
sign in data is username and password. The password is hashed before stored in the database using Bcrypt
![registerfinish](https://user-images.githubusercontent.com/74295809/221579290-848c91a3-7599-4fa2-be91-84c3bbe68c62.png)
 
# Login module
One the user has an account can sign with email and password
Session is started
# Create group modules
After successful login user can create a group and he become the admin of the group or can join any of the group available
Create a group fill the create group form that is group icon, group name, and group description/ info
Join a group click button join or click group after searching group.
# chat area
To chat user can click the chat button of the group he/she want to chat/message
The type the message to send and if there is a file click plus(+) button and click send
User can see other group members

# User Interface
The web application is created on create UI fast loading environment achieved using jquery, bootstrap without much web browser reloading or refreshing and this is acheived using ajax
![chatarea](https://user-images.githubusercontent.com/74295809/221579173-b6f7fa0b-8351-4ee6-98a4-327332f65b57.png)


# created by 
Eric Gichuri
Website https://ericgichuri.github.io
