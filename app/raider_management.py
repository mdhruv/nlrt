from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models.raider import Raider
from flask_login import current_user
from flask import render_template, flash, redirect, url_for
from app import db

class UpdateRaiderForm(FlaskForm):
    game_classes = ["Mage", "Warlock", "Priest", "Druid", "Rogue", "Hunter", "Shaman", "Paladin", "Warrior"]
    operation  = SelectField('Add/Remove/Update', choices=["Add", "Remove", "Update"])
    name = StringField('Raider Name', validators=[DataRequired()])
    game_class = SelectField('Class', choices=game_classes)
    role = SelectField('Role', choices=["Tank", "Healer", "Melee DPS", "Ranged DPS"])
    submit = SubmitField('Update!')


def _handle_add(form):
    raider = Raider.query.filter_by(name=form.name.data).first()
    if raider is not None:
        flash('Raider already exists: %s' % raider.name)
        return redirect(url_for('raider_management'))
    flash('Adding Raider: %s' % form.name.data)
    raider = Raider(name=form.name.data, game_class=form.game_class.data, role=form.role.data, guild=current_user.guild, realm=current_user.realm)
    db.session.add(raider)
    db.session.commit()
    return redirect(url_for('raider_management'))

def _handle_remove(form):
    raider = Raider.query.filter_by(name=form.name.data).first()
    if raider is not None:
        flash('Removing Raider: %s' % raider.name)
        db.session.delete(raider)
        db.session.commit()
    else:
        flash('Unable to Remove Raider: %s' % form.name.data)
    return redirect(url_for('raider_management'))

def _handle_update(form):
    raider = Raider.query.filter_by(name=form.name.data).first()
    if raider is not None:
        flash('Modifying Raider: %s' % raider.name)
        db.session.delete(raider)
        raider = Raider(name=form.name.data, game_class=form.game_class.data, role=form.role.data, guild=current_user.guild, realm=current_user.realm)
        db.session.add(raider)
        db.session.commit()
    else:
        flash('Raider does not exist: %s' % form.name.data)
        return redirect(url_for('raider_management'))
    return redirect(url_for('raider_management'))
    
def HandleRaiderManagement():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))            
    raiders = Raider.query.all()
    form = UpdateRaiderForm()
    if form.validate_on_submit():
        if form.operation.data == 'Add':
            return _handle_add(form)
        if form.operation.data == 'Remove':
            return _handle_remove(form)
        if form.operation.data == 'Update':
            return _handle_update(form)
    return render_template('raider_management.html', title='Raider Management', form=form, raiders=raiders)