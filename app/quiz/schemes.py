from marshmallow import Schema, fields


class ThemeSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)


class AnswerSchema(Schema):
    title = fields.Str()
    is_correct = fields.Bool()


class QuestionSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    theme_id = fields.Int()
    answers = fields.List(fields.Nested(AnswerSchema()))


class ThemeListSchema(Schema):
    themes = fields.List(fields.Nested(ThemeSchema()))


class ThemeIdSchema(Schema):
    pass


class ListQuestionSchema(Schema):
    questions = fields.List(fields.Nested(QuestionSchema()))
