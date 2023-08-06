import os
import json


class Scenario:
    def __init__(self, scenario_dir):
        self.scenario_dir = scenario_dir
        self.data = dict()
        self.__load()
        self.steps = []

    def __load(self):
        for root, dirs, files in os.walk(self.scenario_dir):
            for filename in files:
                if filename.endswith(".json"):
                    with open(os.path.join(root, filename), 'r', encoding="UTF-8") as f:
                        self.data[os.path.splitext(filename)[0]] = json.loads(f.read())

    def append_sub_scenario(self, sub_scenario):
        self.steps.append(sub_scenario)

    def append_step(self, step_class, service):
        self.steps.append(step_class(service, self))

    def run(self):
        for step in self.steps:
            step.run()

    def get(self, key):
        return self.data.get(key)


if __name__ == '__main__':
    scenario = Scenario("D:\\github\\eclinical\\eclinical\\standard\\scenarios\\new_study")
    print(scenario.data)
