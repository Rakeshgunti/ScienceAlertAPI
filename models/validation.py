import re
from datetime import datetime
from marshmallow import Schema, fields, ValidationError, validates
from marshmallow.validate import Length, Range, Email, ContainsOnly

class RegistrationSchema(Schema):
    """
    Parameters:
     - email (str)
     - password (str)
     - name (int)
     - time_created (time)
    """
    # the 'required' argument ensures the field exists
    email = fields.Str(required=True, validate=Email)
    password = fields.Str(required=True,
        validate=Length(min=8, max=32, error='Length of password should be between 8-32'))
    name = fields.Str(required=True, 
        validate=Length(min=8, max=32, error='Name cannot be less than 2 characters'))
    time_created = fields.DateTime(required=True, default=datetime.now())

    @validates("password")
    def password_check(self, data):
        """
        Description: Validates if passwords consists of atleast one lowercase, uppercase alphabet, numeric, punctuation
        Input: String
        Output: ValidationError or None
        """
        reg = '[!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~-]{1,}'
        if not (re.search('[a-z]{1,}', data) and re.search('[A-Z]{1,}', data) 
            and re.search('[0-9]{1,}', data) and re.search(reg, data)):
            raise ValidationError("Please make sure password consists of atleast one lowercase and uppercase alphabet, numeric, punctuation")

    @validates("name")
    def name_check(self, data):
        """
        Description: Validates Name
        Input: String
        Output: ValidationError or None
        """
        if not re.findall('[A-Za-z]{2,25}\s[A-Za-z]{2,25}', data):
            raise ValidationError('Invalid Name. Please check and update')