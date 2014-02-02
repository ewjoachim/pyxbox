import pygame


class Game(object):
    """
    Base game set : an inifinite loop
    This is to be inherited, with the methods
    prepare, loop and cleanup overridden
    """
    def __init__(self, fps=50):
        self.clock = pygame.time.Clock()
        self.fps = fps
        pygame.init()

    def prepare(self):
        """
        Called once at the beginning
        """
        raise NotImplementedError()

    def loop(self):
        """
        Called at every "frame"
        """
        raise NotImplementedError()

    def cleanup(self):
        """
        Called at the end.
        """
        raise NotImplementedError()

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

    def start(self):
        ended = False
        self.prepare()
        try:
            while not ended:
                self.loop()
                if self.check_quit():
                    break
                self.clock.tick(self.fps)
        except KeyboardInterrupt:
            pass
        self.cleanup()
        pygame.quit()


