# Racing Game

A fun and exciting racing game built using Pygame. Players can race against a computer-controlled car on a track, avoid obstacles, and try to finish the race in the shortest time possible. It is a term project of Game Programming lecture.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [How to Play](#how-to-play)

## Description

This project is a 2D racing game where the player controls a car on a racetrack and competes against a computer-controlled car. The game features sound effects for collisions and engine sounds, as well as levels that increase in difficulty. The game is designed to be easily extensible and customizable.

## Installation

To install and run the game on your local machine, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/atayiilmaz/nfs2d.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd racing-game
    ```

3. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the game, simply run the following command:

```bash
python main.py
```

## How to Play

### Controls

- W: Move forward
- S: Move backward
- A: Turn left
- D: Turn right

### Game Flow

- Start the game by pressing any key.
- Control the car using the w,a,s,d keys to navigate through the track.
- Avoid crashing into the borders or obstacles.
- Reach the finish line to progress to the next level.
- The game ends when all levels are completed or the player car crashes.