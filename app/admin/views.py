# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import TrainerForm
from .. import db
from ..models import Trainer
from forms import TrainerForm, SessionForm, TraineeAssignForm
from ..models import Trainer, Session, Trainee

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Trainer Views

@admin.route('/trainers', methods=['GET', 'POST'])
@login_required
def list_trainers():
    """
    List all trainers
    """
    check_admin()

    trainers = Trainer.query.all()

    return render_template('admin/trainers/trainers.html',
                           trainers=trainers, title="Trainer")

@admin.route('/trainers/add', methods=['GET', 'POST'])
@login_required
def add_trainer():
    """
    Add a trainer to the database
    """
    check_admin()

    add_trainer = True

    form = TrainerForm()
    if form.validate_on_submit():
        trainer = Trainer(name=form.name.data,
                                description=form.description.data)
        try:
            # add trainer to the database
            db.session.add(trainer)
            db.session.commit()
            flash('You have successfully added a new trainer.')
        except:
            # in case trainer name already exists
            flash('Error: trainer name already exists.')

        # redirect to trainers page
        return redirect(url_for('admin.list_trainers'))

    # load trainer template
    return render_template('admin/trainers/trainer.html', action="Add",
                           add_trainer=add_trainer, form=form,
                           title="Add trainer")

@admin.route('/trainers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_trainer(id):
    """
    Edit a trainer
    """
    check_admin()

    add_trainer = False

    trainer = Trainer.query.get_or_404(id)
    form = TrainerForm(obj=trainer)
    if form.validate_on_submit():
        trainer.name = form.name.data
        trainer.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the trainer.')

        # redirect to the trainer page
        return redirect(url_for('admin.list_trainers'))

    form.description.data = trainer.description
    form.name.data = trainer.name
    return render_template('admin/trainers/trainer.html', action="Edit",
                           add_trainer=add_trainer, form=form,
                           trainer=trainer, title="Edit Trainer")

@admin.route('/trainer/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_trainer(id):
    """
    Delete a trainer from the database
    """
    check_admin()

    trainer = Trainer.query.get_or_404(id)
    db.session.delete(trainer)
    db.session.commit()
    flash('You have successfully deleted the trainer.')

    # redirect to the trainer page
    return redirect(url_for('admin.list_trainers'))

    return render_template(title="Delete Trainer")

@admin.route('/sessions')
@login_required
def list_sessions():
    check_admin()
    """
    List all sessions
    """
    sessions = Session.query.all()
    return render_template('admin/sessions/sessions.html',
                           sessions=sessions, title='Sessions')

@admin.route('/sessions/add', methods=['GET', 'POST'])
@login_required
def add_session():
    """
    Add a session to the database
    """
    check_admin()

    add_session = True

    form = SessionForm()
    if form.validate_on_submit():
        session = Session(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(session)
            db.session.commit()
            flash('You have successfully added a new session.')
        except:
            # in case session already exists
            flash('Error: session name already exists.')

        # redirect to the sessions page
        return redirect(url_for('admin.list_sessions'))

    # load session template
    return render_template('admin/sessions/session.html', add_session=add_session,
                           form=form, title='Add Session')

@admin.route('/sessions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_session(id):
    """
    Edit a session
    """
    check_admin()

    add_session = False

    session = Session.query.get_or_404(id)
    form = SessionForm(obj=session)
    if form.validate_on_submit():
        session.name = form.name.data
        session.description = form.description.data
        db.session.add(session)
        db.session.commit()
        flash('You have successfully edited the session.')

        # redirect to the sessions page
        return redirect(url_for('admin.list_sessions'))

    form.description.data = session.description
    form.name.data = session.name
    return render_template('admin/sessions/session.html', add_session=add_session,
                           form=form, title="Edit Session")

@admin.route('/sessions/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_session(id):
    """
    Delete a session from the database
    """
    check_admin()

    session = Session.query.get_or_404(id)
    db.session.delete(session)
    db.session.commit()
    flash('You have successfully deleted the session.')

    # redirect to the sessions page
    return redirect(url_for('admin.list_sessions'))

    return render_template(title="Delete Session")


@admin.route('/trainees')
@login_required
def list_trainees():
    """
    List all trainees
    """
    check_admin()

    trainees = Trainee.query.all()
    return render_template('admin/trainees/trainees.html',
                           trainees=trainees, title='Trainees')

@admin.route('/trainees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_trainee(id):
    """
    Assign a trainer and a session to a trainee
    """
    check_admin()

    trainee = Trainee.query.get_or_404(id)

    # prevent admin from being assigned a trainer or a session
    if trainee.is_admin:
        abort(403)

    form = TraineeAssignForm(obj=trainee)
    if form.validate_on_submit():
        trainee.trainer = form.trainer.data
        trainee.session = form.session.data
        db.session.add(trainee)
        db.session.commit()
        flash('You have successfully assigned a trainer and session.')

        # redirect to the sessions page
        return redirect(url_for('admin.list_trainees'))

    return render_template('admin/trainees/trainee.html',
                           trainee=trainee, form=form,
                           title='Assign Trainee')