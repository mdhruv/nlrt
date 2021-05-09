from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, SelectMultipleField, StringField, IntegerField, widgets
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models.raider import Raider
from flask_login import current_user
from flask import render_template, flash, redirect, url_for, request
from app import db
from app.raid_split import CalculateSplits

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RaidSplitForm(FlaskForm):
    choices = MultiCheckboxField('Routes', coerce=int)
    req_str = StringField('Requirement String', default="tank:2;healer:2;paladin:1;priest:1;druid:1;mage:1;raidleader:1;warlock:1")
    loot_str = StringField('Loot String', default="item1:Altear,Salvion,Hotdogfarm;item2:Loriley,Nemsky")
    num_splits = IntegerField("Number of Splits", default=2)
    sim_num = IntegerField("Number of Simulations", default=1000)
    submit = SubmitField('Split!')


def _get_checked_raiders(form, raiders):
    checked_raiders = []
    for raider in raiders:
        if raider.id in form.choices.data:
            checked_raiders.append(raider)
    return checked_raiders
    
def HandleRaidSplit():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))            
    raiders = Raider.query.filter_by(guild=current_user.guild, realm=current_user.realm)
    form = RaidSplitForm()
    form.choices.choices = list(map(lambda x: (x.id, x.name), raiders))
    
    if not form.validate_on_submit():
        form.choices.data = list(map(lambda x: x.id, raiders))
    else:
        checked_raiders = _get_checked_raiders(form, raiders)
        splits = CalculateSplits(checked_raiders, form.req_str.data, form.loot_str.data, form.num_splits.data, form.sim_num.data)
        if splits is not None and len(splits) > 0:
            return render_template('splits.html', title='Splits', splits=splits)
        else:
            flash('Error Calculatig Splits! Check Params!')
            
        
    return render_template('raid_split.html', title='Raider Split', form=form)