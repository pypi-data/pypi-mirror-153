class StepDefinitions(dict):

    def call_back(self, step_name: str, **kwargs):
        step = self.get(step_name)
        if step:
            step.call_back(**kwargs)