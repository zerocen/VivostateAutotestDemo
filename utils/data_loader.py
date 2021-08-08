import yaml


class DataLoader:

    @classmethod
    def load_test_case_data(cls, path):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if data:
            return data
        else:
            raise Exception("Failed load test case data!")
