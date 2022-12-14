class Animation:
    def __init__(self, frames, frame_rate, name = None):
        self.name = name
        self.frames = frames
        self.frame_rate = frame_rate
        self.frame_time = 1000 / frame_rate
        self.current_frame = 0
        self.last_frame_update = millis()
        self.loop = True
        self.paused = False
    
    
    def update(self):
        if self.paused: return
        if millis() >= self.last_frame_update + self.frame_time:
            if self.current_frame < len(self.frames) - 1:
                self.current_frame += 1
                # self.current_frame = (self.current_frame + 1) % len(self.frames)
            elif self.loop:
                self.current_frame = 0
            else:
                self.paused = True
            self.last_frame_update = millis()
            
    
    def get_current_frame(self):
        return self.frames[self.current_frame]


    def display(self, pos):
        image(self.frames[self.current_frame], pos.x, pos.y)
    
    
    def first_frame(self):
        return self.current_frame == 0

    def no_loop(self):
        self.loop = False

    def finished(self):
        return self.loop and self.current_frame == len(self.frames)-1


class StateMachine:
    def __init__(self):
        self.current_state = None
        self.transitions = {}
    
    
    def add_state(self, state):
        if state in self.transitions:
            return
        if self.current_state is None:
            self.current_state = state
        self.transitions[state] = []
    
    
    def add_transition(self, state, new_state, condition_func):
        self.add_state(state)
        self.add_state(new_state)
        self.transitions[state].append((new_state, condition_func))
    
    
    def update(self):
        if self.current_state is None: return
        for new_state, condition_func in self.transitions[self.current_state]:
            if condition_func():
                self.current_state = new_state
                return True # state changed
        return False # state didn't change


class Animator:
    def __init__(self):
        self.state_machine = StateMachine()
        self.animations = []
        self.current_animation = None
    
    
    def add_animation(self, animation):
        self.state_machine.add_state(len(self.animations))
        self.animations.append(animation)
        if self.current_animation is None:
            self.current_animation = animation
        return self
    
    
    def update(self):
        if self.state_machine.update():
            self.current_animation = self.animations[self.state_machine.current_state]
            self.current_animation.current_frame = 0
        if self.current_animation is not None:
            self.current_animation.update()
            

    def get_current_frame(self):
        if self.current_animation is not None:
            return self.current_animation.get_current_frame()
    
    def display(self, pos):
        if self.current_animation is not None:
            self.current_animation.display(pos)
