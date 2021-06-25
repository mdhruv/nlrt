from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models.raider import Raider
from flask_login import current_user
from flask import render_template, flash, redirect, url_for
from app import db, constants
from sqlalchemy import func

class AddRemoveRaiderForm(FlaskForm):
    operation  = SelectField('Add/Remove', choices=["Add", "Remove"])
    name = StringField('Raider Name', validators=[DataRequired()])
    game_class = SelectField('Class', choices=constants.Classes)
    role = SelectField('Role', choices=constants.Roles)
    submit = SubmitField('Update!')

class UpdateRaiderForm(FlaskForm):
    name = SelectField('Raider Name', choices=[], validators=[DataRequired()])
    submit = SubmitField('Update!')
    
class RaiderDetailForm(FlaskForm):
    game_class = SelectField('Class', choices=constants.Classes)
    role = SelectField('Role', choices=constants.Roles)
    main = SelectField('Main')
    friends = StringField('Friends')
    partner = SelectField('Partner')
    profession1 = SelectField("Profession 1", choices=constants.Professions)
    profession2 = SelectField("Profession 2", choices=constants.Professions)
    has_cooking = BooleanField('Has Cooking')
    has_first_aid = BooleanField('Has First Aid')
    has_fishing = BooleanField('Has Fishing')
    is_raid_leader = BooleanField('Is Raid Leader')
    submit = SubmitField('Update!')

def _handle_add(form):
    raider = Raider.query.filter_by(name=form.name.data).first()
    if raider is not None:
        flash('Raider already exists: %s' % raider.name)
        return redirect(url_for('add_remove_raider'))
    flash('Adding Raider: %s' % form.name.data)
    raider = Raider(name=form.name.data, game_class=form.game_class.data, role=form.role.data, guild=current_user.guild, realm=current_user.realm)
    db.session.add(raider)
    db.session.commit()
    return redirect(url_for('add_remove_raider'))

def _handle_remove(form):
    raider = Raider.query.filter_by(name=form.name.data).first()
    if raider is not None:
        flash('Removing Raider: %s' % raider.name)
        db.session.delete(raider)
        db.session.commit()
    else:
        flash('Unable to Remove Raider: %s' % form.name.data)
    return redirect(url_for('add_remove_raider'))

def _parse_friends(selected_raider, friends_string):
    friends_string_split = friends_string.lower().replace(',', ' ').split()
    friends = []
    for friend_string in friends_string_split:
        friend = Raider.query.filter_by(guild=current_user.guild, realm=current_user.realm).filter(func.lower(Raider.name) == friend_string).first()
        if friend is None or friend.name == selected_raider.name:
            return None
        friends.append(friend)
    for friend in friends:
        if friend not in selected_raider.friends:
            selected_raider.friends.append(friend)
        if selected_raider not in friend.friends:
            friend.friends.append(selected_raider)
    for old_friend in selected_raider.friends:
        if old_friend.name.lower() not in friends_string_split:
            selected_raider.friends.remove(old_friend)
            old_friend.friends.remove(selected_raider)
    return friends

def _update_partner(selected_raider, partner_string):
    if partner_string == 'None':
        old_partner = selected_raider.partner
        if old_partner is not None:
            old_partner.partner = None
        selected_raider.partner = None
        return ''
    partner = Raider.query.filter(Raider.name == partner_string).first()
    if partner is None or partner.name == selected_raider.name:
        return None
    selected_raider.partner = partner
    partner.partner = selected_raider
    return partner

def _update_main(selected_raider, main_string):
    if main_string == 'None':
        selected_raider.main = None
        return ''
    main = Raider.query.filter_by(guild=current_user.guild, realm=current_user.realm).filter(func.lower(Raider.name) == main_string).first()
    if main is None or main.name == selected_raider.name:
        return None
    selected_raider.main = main
    return main

def _get_all_mains(selected_raider):
    mains = Raider.query.filter_by(guild=current_user.guild, realm=current_user.realm).filter(~Raider.main.has())
    mains = sorted(mains, key=lambda x:x.sort_key(), reverse=True)
    return list(filter(lambda x: x != selected_raider.name, map(lambda x: x.name, mains)))
    
    
def HandleAddRemoveRaider():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))            
    raiders = Raider.query.all()
    raiders = sorted(raiders, key=lambda x:x.sort_key(), reverse=True)
    form = AddRemoveRaiderForm()
    if form.validate_on_submit():
        if form.operation.data == 'Add':
            return _handle_add(form)
        if form.operation.data == 'Remove':
            return _handle_remove(form)
    return render_template('add_remove_raider.html', title='Add Remove Raider', form=form, raiders=raiders)

def HandleUpdateRaider():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = UpdateRaiderForm()           
    raiders = Raider.query.filter_by(guild=current_user.guild, realm=current_user.realm)
    raiders = sorted(raiders, key=lambda x:x.sort_key(), reverse=True)
    if len(raiders) == 0:
        return redirect(url_for('add_remove_raider'))
    form.name.choices = list(map(lambda x: x.name, raiders))
    if form.validate_on_submit():
        selected_raider = Raider.query.filter_by(guild=current_user.guild, realm=current_user.realm, name=form.name.data)
        if selected_raider is None:
            redirect(url_for('update_raider'))
        return redirect(url_for('raider_details', raider_name=form.name.data))
    return render_template('update_raider.html', title='Update Raider', form=form)

def HandleRaiderDetails(raider_name):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    selected_raider = Raider.query.filter_by(guild=current_user.guild, realm=current_user.realm, name=raider_name).first()
    if selected_raider is None:
        redirect(url_for('update_raider'))
    form = RaiderDetailForm() 
    form.main.choices = ['None'] + _get_all_mains(selected_raider)
    form.partner.choices = ['None'] + _get_all_mains(selected_raider)

    if not form.validate_on_submit():
        form.game_class.data = selected_raider.game_class
        form.role.data = selected_raider.role
        if selected_raider.main:
            form.main.data = selected_raider.main.name
        if selected_raider.partner:
            form.partner.data = selected_raider.partner.name
        form.friends.data = ", ".join(list(map(lambda x: x.name, selected_raider.friends)))
        if selected_raider.profession1:
            form.profession1.data = selected_raider.profession1
        if selected_raider.profession2:
            form.profession2.data = selected_raider.profession2
        if selected_raider.has_cooking:
            form.has_cooking.render_kw = {'checked': True}
        if selected_raider.has_first_aid:
            form.has_first_aid.render_kw = {'checked': True}
        if selected_raider.has_fishing:
            form.has_fishing.render_kw = {'checked': True}
        if selected_raider.is_raid_leader:
            form.is_raid_leader.render_kw = {'checked': True}
    else:
        friends = _parse_friends(selected_raider, form.friends.data)
        if friends is None:
            flash('Error parsing friends list: %s' % form.friends.data)
            return redirect(url_for('raider_details', raider_name=raider_name))

        partner = _update_partner(selected_raider, form.partner.data)
        if partner is None:
            flash('Error parsing partner: %s' % form.partner.data)
            return redirect(url_for('raider_details', raider_name=raider_name))
        main = _update_main(selected_raider, form.main.data)
        if main is None:
            flash('Error parsing main: %s' % form.main.data)
            return redirect(url_for('raider_details', raider_name=raider_name))
        selected_raider.game_class = form.game_class.data
        selected_raider.role = form.role.data
        if form.profession1.data == form.profession2.data and form.profession1.data != 'None':
            flash('Duplicate Professions: %s' % form.profession1.data)
            return redirect(url_for('raider_details', raider_name=raider_name))
        if form.profession1.data == 'None':
            selected_raider.profession1 = None;
        else:
            selected_raider.profession1 = form.profession1.data
        if form.profession2.data == 'None':
            selected_raider.profession2 = None;
        else:
            selected_raider.profession2 = form.profession2.data
        selected_raider.has_cooking = form.has_cooking.data
        selected_raider.has_first_aid = form.has_first_aid.data
        selected_raider.has_fishing = form.has_fishing.data
        selected_raider.is_raid_leader = form.is_raid_leader.data
        flash('Successfully Updated: %s' % selected_raider.name)
        db.session.commit()
        return redirect(url_for('update_raider'))
        
    return render_template('raider_details.html', title='Update Raider Details', raider_name=raider_name, form=form)
    