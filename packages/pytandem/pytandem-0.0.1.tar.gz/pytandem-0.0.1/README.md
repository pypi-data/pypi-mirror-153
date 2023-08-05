# PyTandem
> A multi-threaded event manager package for triggering methods in
> tandem groups.

## Installation

### Requirements
```
- python>=3.6
```

### Install using PIP
```
python3 -m pip install --upgrade pytandem
```

## Usage

First define the method(s) you would like to attach to the manager.
```
def print_num(num):
  print(num)
```

Then attach the method using the provided decorator - this will take an
event name as a paramaneter. It should look like so:
```
from pytandem import pytandem

@pytandem.attach('event-name-here')
def print_num(num):
  print(num)
```

> Whenever the above method (`print_num()`) is called, instead of being fired
> immediately it will be added to the manager threads to be started later on.

Next we can fire the method a few times:
```
for i in range(0, 3):
  print_num(i)
```

> You'll notice nothing gets printed yet.

Now we can initiate the concurrent trigger of the 3 instances of the print_num()
method we added to the threads earlier using the `trigger()` method - this, again,
takes the event name as a parameter.
```
pytandem.trigger('event-name-here')
```

We can run the methods synchronously also by passing `False` in the `threaded` argument.
This is set to True by default.
```
pytandem.trigger('event-name-here', threaded=False)
```

And lastly, we can also set the maximum number of concurrent threads that pytandem
will use when triggering an event group. The default value for this is 4.
```
pytandem.trigger('event-name-here', max_threads=16)
```

> Point to note: if max_threads is set to 4, and there are 20 methods attached on the
> same event name, then only 4 will run concurrently until one pops off the queue,
> essentially allowing the next in line to run. Methods will be fired according to
> the order in which they were first attached.

> Note that a high `max_threads` value can cause out of memory issues if not careful.