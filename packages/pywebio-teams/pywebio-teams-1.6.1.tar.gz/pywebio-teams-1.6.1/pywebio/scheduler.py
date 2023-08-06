import logging
import time
from collections import defaultdict
from datetime import datetime, timedelta
from functools import partial
from threading import Thread

logger = logging.getLogger(__name__)

_queue = defaultdict(list)  # ts -> [tid]
_scheduler_thread = None


class Task:
    _tasks = {}  # tid -> task

    @classmethod
    def get(cls, tid):
        return cls._tasks.get(tid)

    def __init__(self, name, interval, start_time, end_time, run_info, start_ts):
        self.name = name
        self.interval = interval
        self.start_time = start_time
        self.end_time = end_time
        self.id = len(Task._tasks)
        Task._tasks[self.id] = self

        self.state = 'waiting'
        self.last_error = None
        self.cnt = 0

        self._run_info = run_info
        self._start_ts = start_ts

        self.abort = False


def _run_scheduler():
    global _queue
    while True:
        if not _queue:
            time.sleep(1)
            continue

        next_tick = min(_queue.keys())
        tids = _queue.pop(next_tick, None)
        s = next_tick - time.time()
        if s < 0:
            s = 0

        logger.debug('scheduler sleep %s seconds', s)
        time.sleep(s)

        for tid in tids:
            print('run task', tid)
            task = Task.get(tid)
            Thread(target=_run_task, args=(task,), daemon=True).start()


def _run_task(task: Task):
    logger.debug('scheduler run task', task.id)
    task.state = 'running'
    try:
        task._run_info()
    except Exception as e:
        task.last_error = e

    if task.interval is None:  # no repeat
        task.state = 'finish'
    else:
        task.cnt += 1
        next_tick = task.interval * task.cnt + time.time()
        if (task.end_time is None or task.end_time.timestamp() > next_tick) and not task.abort:
            task.state = 'waiting'
            _queue[next_tick].append(task.id)
        else:
            task.state = 'finish'

    logger.debug('task[%s] run over, state: %s', task.id, task.state)


def start(target, name=None, args=(), kwargs={}, interval=None, start_time=None, end_time=None):
    """Start a scheduled task

    :param callable target: callable object to be invoked when the task run.
    :param str name: task name
    :param list/tuple args: the argument tuple for the `target` invocation. Defaults to ().
    :param dict kwargs: a dictionary of keyword arguments for the `target` invocation. Defaults to {}.
    :param int interval: the time, in second, the timer should delay in between each run.
    :param datetime start_time: the start time to run. Default is now
    :param datetime end_time: the end time for task. If no set, the task will run forever.
    :return int: task id
    """
    global _scheduler_thread
    if _scheduler_thread is None:
        _scheduler_thread = Thread(target=_run_scheduler, daemon=True, name='scheduler')
        _scheduler_thread.start()

    if start_time is None:
        start_time = datetime.now()
    elif start_time < datetime.now():
        s = (interval - (datetime.now() - start_time).seconds % interval) % interval
        start_time = datetime.now() + timedelta(seconds=s)
    else:
        start_time = start_time

    start_ts = int(start_time.timestamp())

    task = Task(name, interval, start_time, end_time, partial(target, *args, **kwargs), start_ts=start_ts)

    _queue[start_ts].append(task.id)

    return task.id


def cancel(task_id):
    """Cancel the task.

    :param int task_id: The id of the task
    """
    t = Task.get(task_id)
    if t and not t.abort:
        t.abort = True
        return True


def state(task_id):
    """Get state of the task

    :param int task_id: The ID of the task
    :return dict: {
        'id': task id,
        'name': task name,
        'interval': task interval,
        'start_time': task start_time,
        'end_time': task end_time,
        'run_count': run count,
        'state': 'running'/'waiting'/'finish',
        'last_exception': The last exception encountered when running the task, `None` if no exception.
    }
    """
    t = Task.get(task_id)
    if not t:
        return

    return {
        'id': task_id,
        'name': t.name,
        'interval': t.interval,
        'start_time': t.start_time,
        'end_time': t.end_time,
        'run_count': t.cnt,
        'state': t.state,
        'last_exception': t.last_error
    }


def enumerate():
    """Get all tasks' state.

    :return list: state list for all tasks.
    """
    return [state(tid) for tid in Task._tasks]


def taskboard():
    """Task Scheduler"""
    from pywebio import output
    from pywebio import session
    output.put_markdown("## Scheduled Task Board")

    output.set_scope('tasks')

    def cancel_task(tid):
        task = Task.get(tid)
        if task.abort:
            return output.toast('Task already canceled', color='error')
        elif task.state == 'finish':
            return output.toast('Task already finished', color='error')

        cancel(tid)
        show_task()
        output.toast('Canceled')

    @output.use_scope('tasks', clear=True)
    def show_task():
        tasks = enumerate()
        if not tasks:
            output.put_info("No task, create one first")
            return

        output.put_table([
            {
                **t,
                'action': output.put_button('Cancel', partial(cancel_task, t['id']))
            }
            for t in tasks
        ], header=['id', 'name', 'interval', 'start_time', 'end_time', 'run_count', 'state', 'last_exception',
                   'action'])

    def show_task_t():
        while True:
            show_task()
            time.sleep(min(list(_queue.keys()) + [time.time() + 60]) - time.time() + 1)

    t = Thread(target=show_task_t, daemon=True)
    session.register_thread(t)
    t.start()

    session.hold()


if __name__ == '__main__':
    from . import start_server

    start(lambda: None, name='T0')
    start(lambda: None, name='T1', interval=10)
    start(lambda: None, name='T2', interval=10, start_time=datetime.now() - timedelta(seconds=5))
    start(lambda: None, name='T3', interval=10, end_time=datetime.now() + timedelta(seconds=100))
    start(lambda a, b: a / b, name='T4', args=(1, 0), interval=10, end_time=datetime.now() + timedelta(seconds=100))
    start(lambda a, b: a / b, name='T5', kwargs=dict(a=1, b=2), interval=10,
          end_time=datetime.now() + timedelta(seconds=100))

    start_server(taskboard, port=8080, debug=True)
