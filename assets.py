from animation import Animation

class AssetManager:
    def __init__(self):
        self.anim_explode = AssetManager.load_animation("./images/effects/Explosion_{}.png", 8, "explosion")
        self.anim_explode.set_fps(20)

        self.turrets = [loadImage("./images/Gun_{}.png".format(chr(i))) for i in range(ord('A'), ord('A')+4)]
        self.hulls = [loadImage("./images/Hull_{}.png".format(chr(i))) for i in range(ord('A'), ord('A')+4)]

    @staticmethod
    def load_animation(path, num_frames, name = None):
        frames = [loadImage(path.format(chr(i))) for i in range(ord('A'), ord('A')+num_frames)]
        anim = Animation(frames, name)
        return anim
