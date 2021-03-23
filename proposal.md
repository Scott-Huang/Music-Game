# A Music Rhythm Game
Mingwei Huang (mingwei6) | Moderator: Zifan Feng (zifanf2)
This is a music game using python for CS242

### Abstract

#### Project Purpose
This is a music game that is able to import any music files and generate games to be played.

#### Project Motivation
One of the kinds of games that I usually play is a music game and it is comparably simple to be implemented as an individual project. Since it is difficult to find some good and copyright-free music as the major part of gameplay, I decided to add the functionality to automatically generate a game for any imported music files so that I do not need to take care of copyright problems.

### Technical Specification
 - Platform: PC (anything that runs python)
 - Programming Languages: Python
 - Stylistic Conventions: PEP 8 -- Style Guide for Python Code
 - SDK: Pygame
 - IDE: Visual Studio Code
 - Tools/Interfaces: Computers
 - Target Audience: Music game players

### Functional Specification

#### Features
This is a very normal music game, players should press corresponding keys at the exact time as
the shown in the graphics. In this game, circles (or some other small piece of shapes) will flow
toward where representing certain keys, and players are expected to press the keys exactly when
they overlap. And the rhythm of the circles flowing down should follow the rhythm of the music playing.

The game does not have any music installed, instead, it reads input music files and generates playable game
based on the rhythm of the input music. There are only few games supporting this function and all mainstream
music game do not. (I guess that it is because of copyright issues, even though I choose to implement this
function in order to avoid copyright problems lol.)

The game scores the accuracy of users' gameplay and display the score when games end.
(I decide not to do a history record since the game is auto-generated.)

The game also supports multiple interfaces, each has unique set of keys and ways that circles flow.

(Optional (Undecided)) Customized settings, i.e. customized keys, circles' falling speed, and background.

(Optional) Dynamic background that can also swinging with the rhythm.

#### Scope of the project
###### Limitations:
 * The game should running purely on memory besides reading music files, so I will not consider
 any functions regarding to histories or user info from scratch.
 * This is a very small project and I may not consider extensibility beyond a music game.

###### Assumptions:
 * Players should be familiar with music games, or at least they can play it without tutorials
 because I won't provide any tutorial anyway.
 * The game will only be run by Python.
 * The game should be proporly used and only for gaming.

### Brief Timeline
Week 1: 
 * Learn Pygame tutorials
 * Design and construct game interface layouts
 * Complete rendering motions of circles flowing
 * Complete detection of accuracy of key pressing
 * Complete rendering the effects of key pressed
 * Test basic functionality with fixed circles flows patterns

Week 2:
 * Read and preprocess input music file
 * Find available beat detection libraries
 * Complete rendering feedback of key pressing
 * Integrate everything into a playable game
 * Test the game functionality with a full song and fixed circles flows patterns

Week 3:
 * Refactor previous codes
 * Implement beat detection on input music
 * Prepare a library of circles flowing patterns
 * Auto generate circles flowing patterns based on detected rhythm

Week 4:
 * Catch up any fall-behind progress
 * Refactor previous code
 * Any optional functionalies if time allows
 * Integrate and fully test the game setup

## Rubrics

###### Week 1
| Category | Total Scores Allocated |           Detailed Rubrics            |
| -------- | ---------------------- | ------------------------------------- |
| Interface Sketch | 1 | -1pt for no sketch |
| Game Layout View | 5 | -1pt for the layout is not resizable <br />
                          -1pt for each missing components (circles, keys, background, music, ..., up to 3 pt) <br />
                          -1 pt for game interface cannot be displayed normally |
| Circle Rendering | 2 | -2pt for circles flowing not rendered <br /> 
                         -1pt for circles not moving correctly |
| Game Effects | 2 | -2pt for no read from keyboard <br /> -1pt for no effect on key pressed |
| Accuracy Detection | 1 | -1pt for no accuracy detection |
| Game Model Design | 3 | -2pt for no clear model design <br />
                          -1pt for there is no clear seperation between the view and model |
| Error Handling | 1 | -1pt for no error handling |
| Unit Test | 4 | +0.5pt for each unit test |
| Mannual Test | 6 | +0.5pt for each manual test |

###### Week 2
| Category | Total Scores Allocated |           Detailed Rubrics            |
| -------- | ---------------------- | ------------------------------------- |
| Read Music File | 1 | -1pt music file cannot be read into correct format |
| Key Press Rendering | 3 | -3pt for no effects shown <br /> 
                            -1pt for effects are misformatted (not behave normally) |
| Game Play | 5 | -5pt for game not integrated at all <br /> 
                  -4pt for game cannot run at all <br />
                  -3pt for game cannot run normally <br />
                  -1pt for each small errors (up to 2pt) |
| Result Display | 2 | -2pt for no result desplaying <br />
                       -1pt for result not shown proporly |
| Game Setting | 3 | -2pt for no setting view before game starts <br />
                     -1pt for settings cannot be proporly set for games |
| Error Handling | 1 | +1pt for handling invalid music file |
| Unit Test | 2 | +0.5pt for every unit test |
| Mannual Test | 8 | +0.5pt for each manual test (up to 6pt) <br />
                     +2pt for test an entire game with a song playing |

###### Week 3
| Category | Total Scores Allocated |           Detailed Rubrics            |
| -------- | ---------------------- | ------------------------------------- |
| Beat Detection | 4 | -4pt for no beat detection <br />
                       -2pt for not using detected beats |
| Circles Falling Patterns | 6 | +0.1pt for each pattern (up to 3) <br />
                                 +2pt for auto-generate patterns <br />
                                 +1pt for the format of patterns can be used for generating games |
| Generating Game | 5 | -5pt for game not generated at all <br /> 
                        -3pt for game randomly generated without considering rhythm |
| Unit Test | 3 | +0.5pt for each unit test |
| Mannual Test | 7 | +1pt for each autogenerated games tested |

###### Week 4
(I feel that this will likely to be changed.)
| Category | Total Scores Allocated |           Detailed Rubrics            |
| -------- | ---------------------- | ------------------------------------- |
| Additional Functions <br />
  (Can be used if the previous section<br />
  takes more time than expected) | 5 | +2pt for each customized settings (keys, speed, input backgrounds) <br />
                                       +3pt for dynamic background (incompatible with input backgrounds) |
| Background | 4 | -4pt for no background <br />
                   -2pt for no background selection |
| Actual Game | 6 | -6pt for game not playable at all <br /> 
                    -4pt for game is not behaving normally <br />
                    -3pt for game does not have rhythm <br />
                    -1pt for small bugs |
| Mannual Test | 3 | +0.5pt for each manual test (or unit test if possible) |
| Actual Test | 7 | +1pt for each game with different songs played <br />
                    -2pt for only testing one or two styles of songs |

Here is the [google form link](https://docs.google.com/spreadsheets/d/1v8WOnIgNw6RBgZI1ymYYLdBXQK9f2KFGjnUTNihLy04/edit?usp=sharing) to my rubric.