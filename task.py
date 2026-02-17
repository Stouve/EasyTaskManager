
class Task():

    def __init__(self,title, done=False):
        self.title = title
        self.done = done

    def end_taks(self):
        self.done = True

    def __str__(self):

        return(self.title + " : " + self.done)



