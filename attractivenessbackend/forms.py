from wtforms import Form, validators, ValidationError
from wtforms.fields import FileField


class UploadForm(Form):
    file = FileField(u'file', [validators.InputRequired()])

    def validate_file(form, field):
        if not field.data:
            raise ValidationError('Bad Request')
        if field.data.filename != "filename.png":
            raise ValidationError('Bad Request')
