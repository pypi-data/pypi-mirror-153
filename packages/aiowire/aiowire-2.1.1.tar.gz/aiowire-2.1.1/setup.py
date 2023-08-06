# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiowire']

package_data = \
{'': ['*']}

install_requires = \
['pyzmq>=22.3.0,<23.0.0']

setup_kwargs = {
    'name': 'aiowire',
    'version': '2.1.1',
    'description': 'A simple event loop using asyncio',
    'long_description': 'aiowire - A simple event loop using asyncio\n============================================\n\nThis package implements a ``EventLoop`` class\nthat manages concurrent coroutines.\n\nIt is based on the principles of functional\nreactive programming and draws inspiration\nfrom Haskell\'s `Control.Wire <https://hackage.haskell.org/package/netwire-4.0.7/docs/Control-Wire.html>`_ library.\n\nIn particular, every co-routine started by the\nevent loop is a ``Wire``.\n\n``Wire``-s either return ``None``, indicating they\'re done,\nor another ``Wire``.\n\nAn example helps explain the idea::\n\n    from aiowire import EventLoop\n\n    event = 0\n    async def show_event(ev) \\\n            -> Optional[Callable[[EventLoop],Awaitable]]:\n        print("Running...")\n        event += 1\n        await asyncio.sleep(event*0.15)\n        print(f"Event {event}")\n        if event < 5:\n            return show_event\n\n    async with EventLoop(timeout=1) as event:\n        event.start(show_event)\n        event.start(show_event)\n\n\nWe start up an event loop and drop in two wires.\nEach runs, then returns the ``show_event`` function.\nThe event loop runs those functions next... and so on.\n\nBut this isn\'t functional programming.  The wires\nhave access to the event loop, and can start more\ntasks.  Easy, right?\n\n\nWhat can I do with it?\n^^^^^^^^^^^^^^^^^^^^^^\n\nWhat if you have a server that\'s spawning programs,\nworking with sockets, and managing timeouts?  Drop\nin one wire for each program, one polling on socket I/O,\nand another acting as a timer (as above).\n\nThe canonical task types are thus::\n\n    asyncio.create_subprocess_exec # run a process\n\n    asyncio.sleep # awake the loop after a given time lapse\n\n    zmq.asyncio.Poller.poll # awake the loop after I/O on socket/file\n    # Note: see aiowire.Poller for a Wire-y interface.\n\nNow your sockets can launch programs, and your program\nresults can start/stop sockets, and everyone can start\nbackground tasks.\n\n\nPoller?\n^^^^^^^\n\nThe ``Poller`` class lets you schedule callbacks in response\nto socket or file-descriptor activity.  Of course, the callbacks\nare wires, and run concurrently.\n\nPoller is also a Wire, created as,\n`Poller(dictionary mapping sockets / fd-s to callback wires)`.\n\nYou add it to your event loop as usual::\n\n    # ... create sock from zmq.asyncio.Context\n\n    async def echo(ev):\n        await sock.send( await sock.recv() )\n\n    todo = { 0:  Call(print, "received input on sys.stdin"),\n             sock: echo\n           }\n    async with EventLoop() as ev:\n        ev.start( Poller(todo) )\n\n\nTell me more\n^^^^^^^^^^^^\n\nYes, you *could* just send async functions taking one\nargument to ``EventLoop.start``, but where\'s the fun in\nwriting closures everywhere?\n\nTo take it to the next level, aiowire comes with a\n``Wire`` convenience class that lets you write ``Wire``-s expressively.\nThe following class extensions help you make Wire-s out of common \nprogramming idioms:\n\n* `Wire(w)`: acts like an identity over "async func(ev):" functions\n* `Repeat(w, n)`: repeat wire ``w`` n times in a row\n* `Forever(w)`: repeat forever -- like `Repeat(w) * infinity`\n* `Call(fn, *args)`: call fn (normal or async), ignore the return, and exit\n\nConsider, for example, printing 4 alarms separated by some time interval::\n\n    from aiowire import EventLoop, Call\n\n    prog = ( Call(asyncio.sleep, 0.1) >> Call(print, \'beep\\a\') ) * 4\n\n    async with EventLoop() as ev:\n        ev.start(prog)\n\nReferences\n==========\n\n* https://pyzmq.readthedocs.io/en/latest/api/zmq.html#poller\n* https://pythontic.com/modules/select/poll\n* https://blog.tomecek.net/post/non-blocking-stdin-in-python/\n',
    'author': 'David M. Rogers',
    'author_email': 'predictivestatmech@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/frobnitzem/aiowire',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
