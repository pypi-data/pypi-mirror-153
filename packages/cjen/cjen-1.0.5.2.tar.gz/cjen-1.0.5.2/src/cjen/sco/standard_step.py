class StandardStep:

    def data(self): ...

    def path_variable(self): ...

    def call_back(self, **kwargs): ...

    def _pre_processor(self): ...

    def _post_processor(self): ...

    def _execute(self): ...

    def ignore(self): return False

    def run(self):
        self._pre_processor()
        if not self.ignore():
            self._execute()
        self._post_processor()
