from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models.raider import Raider
from flask_login import current_user
from flask import render_template, flash, redirect, url_for, request
from app import db

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RaidSplitForm(FlaskForm):
    choices = MultiCheckboxField('Routes', coerce=int)
    submit = SubmitField('Split!')


def _get_checked_raiders(form, raiders):
    checked_raiders = []
    for raider in raiders:
        if raider.id in form.choices.data:
            checked_raiders.append(raider)
            print("Checked Raider: %s" % raider.name)
    return checked_raiders
    
def HandleRaidSplit():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))            
    raiders = Raider.query.all()
    #raider_names = list(map(lambda x: x.name, raiders))
    #print(raider_names)
    form = RaidSplitForm()
    form.choices.choices = list(map(lambda x: (x.id, x.name), raiders))
    #form.choices = ['a', 'b', 'c']
    if form.validate_on_submit():
        _get_checked_raiders(form, raiders)
        return redirect(url_for('raid_split'))
        
    return render_template('raid_split.html', title='Raider Split', form=form)