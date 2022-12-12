## Todo
- [x] Maze generation.
- [x] Rectangle collision detection.
- [x] Tank movement.
- [ ] Tank hull.
- [ ] Turret.
- [ ] Sphere collision detection.
- [ ] Bullet.
- [ ] Shooting bullets.
- [ ] Tanks destroying each other.

## Bugs
- [x] Optimize checking for collisions with the maze.
- [x] Fix weird behavior when the tanks collide (one tank has priority).
- [x] Wall's collider is displayed even though the `display_debug` method is not called. _Fix: the walls were just being drawn with stroke on._
- [x] Tanks should spawn in the biggest connected component.

### Fix these if there's enough time:
- [ ] In the `Maze` class, rows and columns should be inverted.
- [ ] If one tank pushes another one to a wall, the other tank will slightly overlap with the wall.
- [ ] Adjust tank's rotation when it pushes against the wall.
- [ ] Do not apply a push vector after checking the bullet collision.

## Notes
- Right now, the tanks cannot be spawned in the same cell. It might be better to have that possibility.