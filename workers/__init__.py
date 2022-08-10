def runtask(name):
    workers = __import__('workers.{}'.format(name))
    print('Running task: {}'.format(name))
    task = getattr(workers, name)
    task.run()