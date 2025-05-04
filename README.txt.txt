For this coursework, I chose to design and develop a game. I wanted to work on something classic and enjoyable, so I decided to recreate the iconic arcade game Space Invaders. To run the program open the file Main.py. Make sure you have Python and Pygame installed.
Use the left and right arrow keys to move the player spaceship. Press the spacebar to shoot lasers. Avoid enemy projectiles and try to eliminate all alien invaders. The game ends when you lose all your lives or defeat all aliens.

Polymorphism

Polymorphism allows objects of different classes to be treated as objects of a common superclass. In the game, different alien types (Enemy_1, Enemy_2, Enemy_3) are all subclasses of the Alien class but can behave differently based on their type. The update method in Alien allows all alien objects to move horizontally, but the behavior of each alien can differ based on its subclass.
Example:
class Alien(pygame.sprite.Sprite):
    def update(self, direction):
        self.rect.x += direction

Abstraction

Abstraction hides the complex implementation details from the user and exposes only essential features. The Player class, for example, manages the player's movement, shooting, and laser recharging in a way that hides the low-level details from the game loop. Players can interact with the spaceship by simply using input keys (left, right, space) without needing to worry about how movement or shooting is implemented.
Example:
class Player(pygame.sprite.Sprite):
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

Inheritance

Inheritance allows new classes to take on properties and methods of existing classes. The Alien and Player classes inherit from pygame.sprite.Sprite, which gives them access to common sprite functionality like image handling and collision detection.
Example:
class Alien(pygame.sprite.Sprite):
    def __init__(self, alien_type, x, y):
        super().__init__()

Encapsulation

Encapsulation restricts direct access to certain details and allows controlled access through methods. For instance, the Player class encapsulates the player's laser shooting logic, so lasers are added to the player's laser group and not directly manipulated outside the class.
Example:
class Player(pygame.sprite.Sprite):
    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

Design Pattern: Singleton

The Singleton design pattern ensures that only one instance of the SoundManager class is created. The SoundManager handles all sound effects, and using the Singleton pattern prevents multiple instances of this class, saving resources and maintaining consistent sound playback.
Example:
class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
Here, __new__ ensures that only one SoundManager instance exists throughout the game.

Composition and Aggregation

Composition and aggregation are demonstrated by the way objects are composed of other objects. For example, the Game class has an instance of Player, SoundManager, and Alien classes. Additionally, the Player has a group of Laser objects (composition).
Example:
class Game:
    def __init__(self):
        self.player = pygame.sprite.GroupSingle(Player(...))
        self.aliens = pygame.sprite.Group()

Data Export/Import

I implemented a simple file system to store and retrieve the highscore. This is done using the read_highscore and write_highscore methods. The highscore is saved to a file (Highscore.txt) to retain the player's progress.
Example:
def read_highscore(self):
    try:
        with open("Highscore.txt", "r") as file:
            highscore = int(file.read().strip())
    except FileNotFoundError:
        highscore = 0
    return highscore

Results

The implementation of the Singleton design pattern for the sound manager was a bit tricky at first, but it effectively ensured that only one instance of the sound manager was used across the game.
A significant hurdle was managing game states (like victory and game over) and ensuring that the game's logic, such as handling lives, score, and penalties, remained consistent throughout.
Debugging the interactions between components like the laser class, obstacles, and the alien lasers was challenging, but it helped refine the game's mechanics and collision handling.

Conclusions

Overall, I am not fully satisfied with my finished work and I definitely could have made improvements or fun additions to the game. There have been unexpected difficulties, such as slow loading when trying to run my code or change its features. I did, however, learnt a bit more about coding in Python and gained experience in creating games. I guess the most fun part is that I can share my work with others.





