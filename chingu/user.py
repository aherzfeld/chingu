# User class for persistant data tracking


class User():
    """ Create user object for persistant data tracking """

    # TODO: add restrictions for username
    # TODO: upon init, query db for user, if none, create_user(Database method)
    def __init__(self, username):
        self.username = username
        self.date_created = None

    @property
    def quizzes_taken(self):
        pass

    @property
    def num_correct(self):
        pass

    @property
    def num_wrong(self):
        pass
