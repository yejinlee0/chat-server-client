# Client overview

### "client.py" : Chat client program
This client program is a full-function client matched with "server.py". Users can chat with each other with this client program and the server. It is a Python file and text-based program that is easy to set up and run right from a clone of the repository. It can be run using the appropriate method for each operating system or environment.
This application client is "Multiple Chat Client". Multiple people can chat using this program.
Each participant set their own nickname. Spaces are not accepted as nicknames like "". Users will know the current number of people in the chat room when they first enter the chat room. This chat program allows participants to perform certain functions by typing in words with a slash symbol(/). 

---

# Client execution and /or URL

- client.py : This client file is made of Python. It is a command-line client using a regular socket. 
- For Windows users : It can be executed by following the sequence described below.
1. Open a cmd prompt and move to the folder location where this file is located.
2. Enter "py client.py" at the command line.
3. Enter a name of the user.
4. Chat.
- For other users : Using a command prompt, navigate to the folder of this client file and run this Python file.

---

# Client Usuage

### Key application concepts
If users enter that words below... <br>

1. "/quit" : If participants enter this, they can leave the chat room. <br>
2. "/help" : If participants enter this, they can see the instructions again. This manual appears the first time you enter the chat room. If you type this word, you can see the description over and over again. <br>
3. "/ch" : If participants enter this, they can change their nickname. Users can't use spaces as nicknames. Also, they can't use their own name or other user's name as a nickname at this time. If an incorrect input is received, the server will print out the relevant instructions and ask if they want to continue changing their nicknames. <br>
4. "/p" : If participants enter this, they can see the number of chat room participants and the nicknames of all users participating in the chat room. This feature lets you whisper to specific nicknames. Whispering is introduced in the following topic. <br>
5. "/w" : If participants enter this, they can use a function called "whispering". Whispering is a function of sending messages to only one person in a chat room. Only the sender and recipient of the message can see the message. The other person can't see the message. Emoji is not available in the Whisper function. Whispering can be sent to users in chat rooms other than an user who wants to sent the secret message. If the server receive an incorrect input, it will print out the relevant instructions and ask the users if they want to re-enter.
6. "/(word)" : (Word) can be "candy or smile or good or love or amaze or sad or angry or sleepy". If participants enter this, they can send emoji related to specific words to chat rooms.


### User Interface

- Input
  * KeyboardInterrupt : It is the key "Ctrl + C". If users press this key, the client program will be terminated. It can be used all the time starting from receiving the name of an user.
  * /quit : It is same as KeyboardInterrupt. Bur it can be used only after the chatting starts.
  * The sentences or words users enter can be used for the chatting. And users can use the emoji by entering some specific words with '/' (slash).
  
- Output
  * Messages from the program : Messages that are appropriate for the situation are printed. The situation can be a error like connection error, EOF error, KeyboardInterrupt error, etc.
  * The messages that users enter are printed out as they are. The messages include a message from you.
