from marshmallow import Schema, fields


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


class QuestionSchema(Schema):
    pass


class AnswerSchema(Schema):
    pass


class ThemeListSchema(Schema):
    themes = fields.Dict(fields.Nested(ThemeSchema()))


class ThemeIdSchema(Schema):
    pass


class ListQuestionSchema(Schema):
    pass
