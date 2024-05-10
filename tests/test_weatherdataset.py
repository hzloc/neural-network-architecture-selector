import unittest
from data.weather_dataset import WeatherDataset


class TestWeatherDataset(unittest.TestCase):
    def test_data_exists(self):
        df = WeatherDataset(horizon=3, input_size=20)
        super().assertIsNotNone(df.weather)

    def test_batching(self):
        df = WeatherDataset(horizon=3, input_size=20, step_size=1)
