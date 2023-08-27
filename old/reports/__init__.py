from abc import ABC, abstractmethod


class ReportFactory:
    report_generators = {}

    @classmethod
    def register_generator(cls, output_type):
        def wrapper(generator_cls):
            cls.report_generators[output_type] = generator_cls
            return generator_cls

        return wrapper

    @classmethod
    def get_generator(cls, output_type):
        return cls.report_generators[output_type]()


class ReportGenerator(ABC):
    @abstractmethod
    def write(self, path):
        raise NotImplementedError


@ReportFactory.register_generator("csv")
class CsvReport(ReportGenerator):
    def write(self, data):
        print("Successfully wrote to CSV!")


@ReportFactory.register_generator("excel")
class ExcelReport(ReportGenerator):
    def write(self, data):
        print("Successfully wrote to Excel!")


generator = ReportFactory.get_generator("csv")
generator.write("dummy-data")
