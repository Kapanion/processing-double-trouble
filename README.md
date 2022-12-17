## Todo
- [x] Maze generation.
- [x] Rectangle collision detection.
- [x] Tank movement.
- [x] Tanks should spawn in the biggest connected component.
- [x] Tank hull.
- [x] Turret.
- [x] Sphere collision detection.
- [x] Bullet.
- [x] Shooting bullets.
- [x] Tanks destroying each other.
- [x] Tank explosion animation.
- [x] Adjust the maze for different screen sizes.
- [x] Different colors of the tank for different players.
- [x] Wining & losing the game.
- [x] Player scores.
- [x] Limit the number of bullets.
- [x] Bullet should not destroy the shooter for a short amount of time after being fired.
- [x] Menu.
- [X] Input field UI.
- [ ] Leaderboard.
- [ ] Sound design.
- [ ] Automatically manage buttons from the `Scene` class.

## Bugs
- [x] Optimize checking for collisions with the maze.
- [x] Fix weird behavior when the tanks collide (one tank has priority).
- [x] Wall's collider is displayed even though the `display_debug` method is not called. _Fix: the walls were just being drawn with stroke on._
- [x] If a tank us pushing back to the wall and fires a bullet, it will be destroyed.
- [x] Many bullets can be fired by holding down the shoot button.
- [x] It's possible to shoot bullets to the other side of a wall.
- [ ] If one player wins but destroys themselves right before the game restarts, their score might still increase.
- [ ] Player 1 can push explosion of player 2.
- [ ] Player 2 is drawn over player 1's explosion.


### Fix these if there's enough time:
- [x] Do not apply a push vector after checking the bullet collision.
- [x] Only use half the number of axes in `CirclePolyCollider` if its number of vertices is even.
- [ ] Optimize bullet-to-tank collision.
- [ ] In the `Maze` class, rows and columns should be inverted.
- [ ] If one tank pushes another one to a wall, the other tank will slightly overlap with the wall.
- [ ] Adjust tank's rotation when it pushes against the wall.
- [ ] One bullet cannot destroy two tanks during the same frame.
- [ ] A bullet may bounce off from a corner in a weird way (as if its going around the corner). 
- [ ] `PolygonCollider` class doesn't have a proper constructor and proper attributes.

## Notes
- Right now, the tanks cannot be spawned in the same cell. It might be better to have that possibility.
- A bullet may bounce off from a corner in a weird way (as if its going around the corner). The reason for this is that the MPV pushes the bullet on the other side of the corner, not taking into account where it comes from.