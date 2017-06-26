# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Trainer, Session

class TrainerForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SessionForm(FlaskForm):
    """
        Form for admin to add or edit a session
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TraineeAssignForm(FlaskForm):
    """
    Form for admin to assign trainers and sessions to trainees
    """
    trainer = QuerySelectField(query_factory=lambda: Trainer.query.all(),
                                  get_label="name")
    session = QuerySelectField(query_factory=lambda: Session.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')