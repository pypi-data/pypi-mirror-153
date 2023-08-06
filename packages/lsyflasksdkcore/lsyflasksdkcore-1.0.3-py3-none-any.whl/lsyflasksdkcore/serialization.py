from marshmallow import ValidationError, EXCLUDE


class SerializationError(Exception):
    def __init__(self, message: ValidationError, many=False):
        self.validation_error = message
        self.many = many
        super().__init__(message)

    def normalized_messages(self):
        return self.validation_error

    def description_messages(self):
        _valid_message = set()
        if self.many:
            for index, row_err in self.validation_error.messages.items():
                for field_name, msg in row_err.items():
                    _msg = "{}:{}".format(msg[0], ','.join(msg[1]))
                    _valid_message.add("第{}条:{}".format(index, _msg))
        else:
            for field_name, msg in self.validation_error.messages.items():
                _valid_message.add("{}:{}".format(msg[0], ','.join(msg[1])))
        return _valid_message

    def field_name_messages(self):
        _valid_message = set()
        if self.many:
            for index, row_err in self.validation_error.messages.items():
                for field_name, msg in row_err.items():
                    _msg = "{}:{}".format(field_name, ','.join(msg[1]))
                    _valid_message.add("第{}条:{}".format(index, _msg))
        else:
            for field_name, msg in self.validation_error.messages.items():
                _valid_message.add("{}:{}".format(field_name, ','.join(msg[1])))
        return _valid_message


class AutoClass(object):
    """根据字典自动给类实例字段赋值"""

    def __fill__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self


class Serialization(object):
    """_deserialize"""

    def __init__(self):
        pass

    @staticmethod
    def dump(shema_instance, data, many=False):
        try:
            return shema_instance.dump(data, many=many)
        except ValidationError as ex:
            raise SerializationError(ex, many)

    @staticmethod
    def load(shema_instance, data, many=False):
        try:
            return shema_instance.load(data=data, unknown=EXCLUDE, many=many)
        except ValidationError as ex:
            raise SerializationError(ex, many)
