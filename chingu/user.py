# User class for persistant data tracking


class User():
    """ Create user object for persistant data tracking """

    # TODO: add restrictions for username
    def __init__(self, username):
        self.username = username
        self.date_created = None
        # these might be properties that query DB
        self.quizzes_taken = None
        self.num_correct = None
        self.num_wrong = None
