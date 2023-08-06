class LambdaAlreadyExist(Exception):
    def __init__(self, name):
        super(LambdaAlreadyExist, self).__init__(f"\nERROR: The lambda with the name -> {name} <- already exist.")
