class Sirapob:
    """
    This class is mention about me(sirapob)
    user = Sirapob()
    user.show_name()
    user.play_game()
    user.about()
    user.show_art()
    """
    def __init__(self):
        self.name = 'Sirapob'
        self.game = 'Valorant,Ninokuni'

    def show_name(self):
        print('Hello my name is {}'.format(self.name))

    def play_game(self):
        print('My currently favourite game right now is {}'.format(self.game))

    def about(self):
        text = """
        Hello guys this me 

        """
        print(text)
    
    def show_art(self):
        text ="""

            _
            //\
            V  \
            \  \_
            \,'.`-.
            |\ `. `.       
            ( \  `. `-.                        _,.-:\
                \ \   `.  `-._             __..--' ,-';/
                \ `.   `-.   `-..___..---'   _.--' ,'/
                `. `.    `-._        __..--'    ,' /
                    `. `-_     ``--..''       _.-' ,'
                    `-_ `-.___        __,--'   ,'
                    `-.__  `----]  ---   __ --|


        """
        print(text)
if __name__ == '__main__':
    user = Sirapob()
    user.show_name()
    user.play_game()
    user.about()
    user.show_art()
