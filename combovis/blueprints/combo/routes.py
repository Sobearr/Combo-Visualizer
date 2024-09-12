from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from combovis.app import db
from .models import Combo, Favourite
import ast

from .combo_reader import convert_combo

combo = Blueprint('combo', __name__, static_folder='static', template_folder='templates')


# Route that handles combo visualization
@combo.route('/visualizer', methods=['GET', 'POST'])
def visualizer():
    if request.method == 'POST':
        form_combo = request.form.get('combo_string')
        form_combo_upper = form_combo.upper()
        converted_combo = convert_combo(form_combo_upper).split(' ')
        return render_template('combo/visualizer.html',
                               combo_str=converted_combo, raw_combo=form_combo)
    else:
        return render_template('combo/visualizer.html',
                               combo_str='', raw_combo='')


# Route that handles the deletion of saved combos
@combo.route('/delete/<int:id>')
@login_required
def delete(id):
    fav = Favourite.query.filter_by(fid=id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        flash('You have successfuly removed the combo from your list.', 'success')
    else:
        flash('This combo does not exist.', 'danger')
    return redirect(url_for('combo.favourite'))


@combo.route('/favourite', methods=['GET', 'POST'])
@login_required
def favourite():
    uid = current_user.get_id()
    if request.method == 'POST':
        combo = request.form.get('combo_string')
        if len(combo) > 2:
            # Add combo to db with user id
            check_combo = Combo.query.filter_by(notation=combo).first()

            # Add new combo to the DB
            if not check_combo:
                # Combo does not exist
                combo_str = request.form.get('combo_str')

                # Clean the combo string
                cleaned_string = combo_str.strip("[]").strip('"')
                combo_list = ast.literal_eval(cleaned_string)

                # Buttons that spend drive bars
                drive_1 = ['DI', 'DR']
                drive_2 = ['PP', 'KK', 'PPP', 'KKK']
                drive = 0

                # Bars would have other purpose, now it should be a boolean but I haven't change the Combo model, maybe later...
                bars = '0'

                # Check input validity and calculate the use of drive bars and supers
                for btn in combo_list:
                    if btn == 'unknown':
                        flash('Cannot save combos with \'unknown\' inputs', 'warning')
                        return redirect(url_for('combo.visualizer'))
                    if btn in ['qcb2', 'qcf2', 'charge_back_forward_back_forward', 'demon']:
                        bars = '1'
                    if btn in drive_1:
                        drive += 1
                    elif btn in drive_2:
                        drive += 2
                    elif btn == 'DRC':
                        drive += 3

                # Add combo do DB
                new_combo = Combo(notation=combo, drive=str(drive), bars=bars)

                db.session.add(new_combo)
                db.session.commit()

            # Add combo to user's favourites
            cid = Combo.query.filter_by(notation=combo).first().cid

            favourite = Favourite.query.filter_by(cid=cid, uid=uid).first()
            if favourite:
                flash('You already have saved this combo', 'warning')
                return redirect(url_for('combo.visualizer'))

            new_fav = Favourite(cid=cid, uid=uid)

            db.session.add(new_fav)
            db.session.commit()
            flash('You have saved the combo to your favourites.', 'success')
        else:
            flash('Please input a combo.', 'info')
        return redirect(url_for('combo.visualizer'))
    elif request.method == 'GET':
        favourites = Favourite.query.filter_by(uid=uid).all()
        ids = [fav.fid for fav in favourites]
        fav_combos = [Combo.query.filter_by(cid=fav.cid).first() for fav in favourites]
        for combo in fav_combos:
            combo.notation = convert_combo(combo.notation).split(' ')

        combo_list = list(zip(ids, fav_combos))

        return render_template('combo/favourite.html', favourites=combo_list)
