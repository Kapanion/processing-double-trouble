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
- [ ] Tank explosion animation.

## Bugs
- [x] Optimize checking for collisions with the maze.
- [x] Fix weird behavior when the tanks collide (one tank has priority).
- [x] Wall's collider is displayed even though the `display_debug` method is not called. _Fix: the walls were just being drawn with stroke on._
- [ ] Bullets bounce off weirdly when hitting corners. 

### Fix these if there's enough time:
- [x] Do not apply a push vector after checking the bullet collision.
- [ ] Optimize bullet-to-tank collision.
- [ ] In the `Maze` class, rows and columns should be inverted.
- [ ] If one tank pushes another one to a wall, the other tank will slightly overlap with the wall.
- [ ] Adjust tank's rotation when it pushes against the wall.
- [ ] Only use half the number of axes in `CirclePolyCollider` if its number of vertices is even.
- [ ] One bullet cannot destroy two tanks during the same frame.

## Notes
- Right now, the tanks cannot be spawned in the same cell. It might be better to have that possibility.