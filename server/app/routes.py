from flask import render_template, flash, redirect, url_for, send_from_directory, abort
import uuid
from app import app, db
from app.forms import URLForm, TaskForm
from app.models import Task
from app.tasks import send_task


@app.route('/')
@app.route('/index')
def index():
    form_for_url = URLForm()
    form_for_task = TaskForm()
    all_tasks = Task.query.order_by(Task.start_time.desc()).all()
    return render_template('index.html', URLForm=form_for_url, TaskForm=form_for_task, tasks=all_tasks)


@app.route('/taskform-handler', methods=['POST'])
def taskform_handle():
    form_for_task = TaskForm()
    if form_for_task.validate_on_submit():
        flash('Handle task {0}'.format(form_for_task.task_id.data))
        return redirect(url_for('task_status', task_id=form_for_task.task_id.data))

    return redirect(url_for('index'))


@app.route('/tasks/<string:task_id>', methods=['GET'])
def task_status(task_id):
    task = Task.query.get(task_id)
    if not task:
        return abort(404, description="No task with id {0}".format(task_id))

    if task.status != "parsed":
        return 'Task {0} {1} with url={2}'.format(task.id, task.status, task.url)
    else:
        return f"http://127.0.0.1:5001/get-archive/{task.id}"


@app.route('/tasks', methods=['POST'])
def new_task():
    # TODO: validate URL
    form_for_url = URLForm()
    if form_for_url.validate_on_submit():
        task_id = uuid.uuid4().hex
        db.session.add(Task(id=task_id, url=form_for_url.URL.data, status='added'))
        db.session.commit()

        send_task(task_id)
        flash('Your URL: {0} parsing with task №{1}'.format(form_for_url.URL.data, task_id))

        return task_id

    return redirect(url_for('index'))
