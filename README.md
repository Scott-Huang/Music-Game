CS 242 Final Project
# Music Game

### Introduction
This is a music game. Users are expected to press the corresponding key when the circles
falls to the keys in the screen. The game will be auto-generated based on the input music file.

### Progess
All components in the game interface are built, including background, keys, circles, tracks, and so on.
Also the key pressing effect is added. --4/5/21

Add a menu screen for starting the game and set the game parameters. Circles will be canceled
and give feedback after corresponding keys are pressed. --4/12/21

The game can now be auto-generated given the chosen music file. It can extract the on-set strength
of the music and generate circle patterns to fit the rhythm of the music. --4/19/21

### Environment set up
The game is built by only python. Here is a list of packages used:

 - Pygame
 - NumPy
 - Unittest
 - Librosa
 - FFmpeg

Also, users are expected to put music files into the res/music folder.

### Design Structure
The game program will be started by index.py, and then call the main game function in game.py 
while the graphics will be rendered in render.py. The game models and 
other funcalities are all in the model folder.

### Credit
The game icon is a free non-commercial resource from ©<a href='https://pngtree.com/so/music'>pngtree.com</a>.

The key image is a free resource from 
©<a href='http://clipart-library.com/clip-art/black-circle-png-transparent-23.htm'>clipart-library.com</a>.

The circles image is from 
©<a href='https://pngimg.com/image/87349'>pngimg.com</a>
with CC 4.0 BY-NC License.
