import unittest
from wtforms import StringField, FloatField, IntegerField
from wtforms.validators import ValidationError
from employee_app.website import valid_lat, valid_lng, valid_cph, valid_rego, valid_mac_address, valid_year, \
    valid_capacity, valid_weight, valid_length, valid_load_index, valid_engine_capacity, valid_ground_clearance


class TestFormValidation(unittest.TestCase):

    def test_lat(self):
        field = FloatField()
        field.data = 100
        self.assertRaises(ValidationError, valid_lat, None, field)
        field.data = -100
        self.assertRaises(ValidationError, valid_lat, None, field)

    def test_lng(self):
        field = FloatField()
        field.data = 200
        self.assertRaises(ValidationError, valid_lng, None, field)
        field.data = -200
        self.assertRaises(ValidationError, valid_lng, None, field)

    def test_cph(self):
        field = FloatField()
        field.data = -10
        self.assertRaises(ValidationError, valid_cph, None, field)

    def test_rego(self):
        field = StringField()
        field.data = "%$123as"
        self.assertRaises(ValidationError, valid_rego, None, field)

    def test_mac_address(self):
        field = StringField()
        field.data = "1234"
        self.assertRaises(ValidationError, valid_mac_address, None, field)
        field.data = "AA:AA:AA:AA:AA"
        self.assertRaises(ValidationError, valid_mac_address, None, field)
        field.data = "AA:AA:AA:GG:11:AA"
        self.assertRaises(ValidationError, valid_mac_address, None, field)
        field.data = "AA:AA:AA:AA:AA:AA:AA"
        self.assertRaises(ValidationError, valid_mac_address, None, field)

    def test_year(self):
        field = IntegerField()
        field.data = 1800
        self.assertRaises(ValidationError, valid_year, None, field)
        field.data = 3000
        self.assertRaises(ValidationError, valid_year, None, field)

    def test_capacity(self):
        field = IntegerField()
        field.data = 1
        self.assertRaises(ValidationError, valid_capacity, None, field)
        field.data = 7
        self.assertRaises(ValidationError, valid_capacity, None, field)

    def test_weight(self):
        field = FloatField()
        field.data = 900
        self.assertRaises(ValidationError, valid_weight, None, field)
        field.data = 2400
        self.assertRaises(ValidationError, valid_weight, None, field)

    def test_length(self):
        field = FloatField()
        field.data = 2
        self.assertRaises(ValidationError, valid_length, None, field)
        field.data = 6
        self.assertRaises(ValidationError, valid_length, None, field)

    def test_load(self):
        field = IntegerField()
        field.data = 70
        self.assertRaises(ValidationError, valid_load_index, None, field)
        field.data = 150
        self.assertRaises(ValidationError, valid_load_index, None, field)

    def test_engine(self):
        field = FloatField()
        field.data = 0
        self.assertRaises(ValidationError, valid_engine_capacity, None, field)
        field.data = 5
        self.assertRaises(ValidationError, valid_engine_capacity, None, field)

    def test_clearance(self):
        field = FloatField()
        field.data = 90
        self.assertRaises(ValidationError, valid_ground_clearance, None, field)
        field.data = 300
        self.assertRaises(ValidationError, valid_ground_clearance, None, field)


if __name__ == '__main__':
    unittest.main()
