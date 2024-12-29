from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise

class inputClass:
    def input_engine(key, player):
        if key == "escape":
            quit()
        if key == "f3":
            window.collider_counter.enabled = not window.collider_counter.enabled
            window.entity_counter.enabled = not window.entity_counter.enabled
            window.fps_counter.enabled = not window.fps_counter.enabled
        if key == "f1":
            player.Crosshair.enabled = not player.Crosshair.enabled

class Controller(FirstPersonController):
    def __init__(self, gamemode, default_fov=85, **kwargs):
        super().__init__(**kwargs)
        if gamemode not in [0, 1, 3]:
            print("Invalid Gamemode Found In Code.")
            quit()
        self.gamemode = gamemode
        self.walk_speed = 4
        self.sprint_speed = 6
        self.default_fov = default_fov
        self.gravity = 0.5
        self.is_flying = False
        self.last_space_tap = 0
        self.space_pressed = False  # Tracks if space is currently being held
        self.crosshair_texture = load_texture("assets/gui/crosshair.png")

        self.Crosshair = Entity(
            model="quad",
            texture=self.crosshair_texture,
            scale=(0.026, 0.026),
            position=(0, 0),
            parent=camera.ui
        )

    def update(self):
        super().update()
        current_time = time.time()

        if self.gamemode == 1:  # Gamemode Creative
            # Handle double-tap space to toggle flight
            if held_keys["space"]:
                if not self.space_pressed:  # Trigger on key press only
                    if current_time - self.last_space_tap < 0.3:
                        self.is_flying = not self.is_flying  # Toggle flying state
                        self.gravity = 0 if self.is_flying else 0.5
                    self.last_space_tap = current_time
                self.space_pressed = True  # Space is being held
            else:
                self.space_pressed = False  # Reset when space is released

            if self.is_flying:
                self.speed = (self.speed * 4) / (time.dt + 1)
                if held_keys["space"]:
                    self.y += 0.1  # Ascend while flying
                elif held_keys["control"]:
                    self.y -= 0.1  # Descend while flying
            else:
                self.speed = (self.speed * 1.2) / (time.dt + 1)
                if held_keys["space"]:
                    self.jump()  # Normal jump when not flying

        elif self.gamemode == 0:  # Gamemode Survival
            self.speed = (self.speed * 1.2) / (time.dt + 1)
        elif self.gamemode == 3:  # Gamemode Spectator
            self.speed = (self.speed * 4) / (time.dt + 1)
            self.gravity = 0
            if held_keys["space"]:
                self.y += 0.1
            elif held_keys["control"]:
                self.y -= 0.1

        # Sprinting logic
        if held_keys["shift"]:
            self.speed = self.sprint_speed
            camera.fov = self.default_fov + 1
        else:
            self.speed = self.walk_speed
            camera.fov = self.default_fov

        self.jump_height = 1.2
        self.height = 2
        self.cursor.enabled = False

class Engine:
    def __init__(self):
        self.player = None
        self.prev_z = 0
        self.prev_x = 0
        self.noise = PerlinNoise(octaves=2, seed=2024)
        self.amp = 24
        self.freq = 100
        self.shell = None
        self.subset = None
        self.background_music = None

    def start(self):
        window.exit_button.enabled = False
        window.cog_button.enabled = False
        window.collider_counter.enabled = False
        window.entity_counter.enabled = False
        window.fps_counter.enabled = False
        window.vsync = False
        window.fullscreen = True

        self.player = Controller(1)
        self.player.x = self.player.z = 75
        self.player.y = 25
        self.prev_z = self.player.z
        self.prev_x = self.player.x

        self.shell = Shell(self.noise, self.amp, self.freq)
        self.subset = Subset(self.noise, self.amp, self.freq, 256, 0)
        self.background_music = Audio("assets/sound/minecraft.ogg", autoplay=True, loop=True)

    def update_engine(self):
        if abs(self.player.z - self.prev_z) > 1 or abs(self.player.x - self.prev_x) > 1:
            self.shell.generateShell(self.player)

        if self.player.y < -20:
            self.player.y = 20

        self.subset.generateSubset()



class Subset:
    def __init__(self, noise, amp, freq, TerrainWidth, WorldGEN = 0):
        self.tw = TerrainWidth
        self.sw = self.tw
        self.subsets = []
        self.subCubes = []
        self.sci = 0
        self.currentSubset = 0
        self.noise = noise
        self.amp = amp
        self.freq = freq
        self.groundTexture = load_texture("assets/block/stroke_mono.png")
        self.WorldGEN = WorldGEN

        if WorldGEN == 0:
            bud = Entity(model = "plane", color = color.rgba(0, 0, 255, 0.2))
            bud.y = -2.6
            bud.x = self.tw / 2 - .5
            bud.z = self.tw / 2 - .5
            bud.scale = (self.tw, 1, self.tw)
            bud.double_sided = True
            scene.fog_color = color.rgb(0, 222, 222)
            scene.fog_density = .001
            Sky()
        elif WorldGEN == 1:
            bud = Entity(model = "plane", color = color.rgba(255, 0, 0, 0.9))
            bud.y = -2.6
            bud.x = self.tw / 2 - .5
            bud.z = self.tw / 2 - .5
            bud.scale = (self.tw, 1, self.tw)
            bud.double_sided = True
            scene.fog_color = color.rgb(255, 0, 0)
            scene.fog_density = .02
            window.color = color.rgb(255, 0, 0)
        elif WorldGEN == 2:
            scene.fog_color = color.rgb(0, 222, 222)
            scene.fog_density = .01
            window.color = color.rgb(0, 0, 0)
        elif WorldGEN == 3:
            bud = Entity(model = "plane", color = color.rgba(0, 0, 255, 0.6))
            bud.y = -2.6
            bud.x = self.tw / 2 - .5
            bud.z = self.tw / 2 - .5
            bud.scale = (self.tw, 1, self.tw)
            bud.double_sided = True
            scene.fog_color = color.rgb(0, 0, 255)
            scene.fog_density = .004
            Sky()

        for i in range(self.sw):
            bud = Entity(model = "cube")
            self.subCubes.append(bud)

        for i in range(int((self.tw * self.tw) / self.sw)):
            bud = Entity(model = None)
            self.subsets.append(bud)

    def generateSubset(self):
        if self.currentSubset >= len(self.subsets): 
            return
    
        for i in range(self.sw):
            x = self.subCubes[i].x = floor((i + self.sci) / self.tw)
            z = self.subCubes[i].z = floor((i + self.sci) % self.tw)
            y = self.subCubes[i].y = floor((self.noise([x / self.freq, z / self.freq])) * self.amp)
            self.subCubes[i].parent = self.subsets[self.currentSubset]
            if y < -2:
                if self.WorldGEN == 0:
                    self.subCubes[i].color = color.gray
                    self.subCubes[i].model = 'cube'  # Full cube for ground blocks
                elif self.WorldGEN == 1:
                    self.subCubes[i].color = color.red
                    self.subCubes[i].model = 'cube'  # Full cube for ground blocks
                elif self.WorldGEN == 2:
                    self.subCubes[i].color = color.white
                    self.subCubes[i].model = 'cube'  # Full cube for ground blocks
                elif self.WorldGEN == 3:
                    self.subCubes[i].color = color.blue
                    self.subCubes[i].model = 'cube'  # Full cube for ground blocks
            else:
                if self.WorldGEN == 0:
                    self.subCubes[i].color = color.green  # Ground block color
                    self.subCubes[i].model = 'cube'  # Full cube for ground blocks
                elif self.WorldGEN == 1:
                    self.subCubes[i].color = color.red
                    self.subCubes[i].model = 'cube'  # Full cube for ground blocks
                elif self.WorldGEN == 2:
                    self.subCubes[i].color = color.white
                    self.subCubes[i].model = 'cube'  # Full cube for ground blocks
                elif self.WorldGEN == 3:
                    self.subCubes[i].color = color.white
                    self.subCubes[i].model = 'cube'  # Full cube for ground blocks
        
            self.subCubes[i].visible = False  # Set to invisible before combining
    
        self.subsets[self.currentSubset].combine(auto_destroy=False)
        for cube in self.subCubes:
            cube.visible = False
        self.subsets[self.currentSubset].texture = self.groundTexture
        self.sci += self.sw
        self.currentSubset += 1
class Shell:
    def __init__(self, noise, amp, freq):
        self.shellies = []
        self.sw = 6
        self.noise = noise
        self.amp = amp
        self.freq = freq

        for i in range(self.sw * self.sw):
            bud = Entity(model="cube", collider="mesh")
            bud.visible = False
            self.shellies.append(bud)

    def generateShell(self, player):
        for i in range(len(self.shellies)):
            x = self.shellies[i].x = floor((i / self.sw) + player.x - self.sw / 2)
            z = self.shellies[i].z = floor((i % self.sw) + player.z - self.sw / 2)
            self.shellies[i].y = floor((self.noise([x / self.freq, z / self.freq])) * self.amp)