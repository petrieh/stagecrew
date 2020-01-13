.. Copyright (C) 2020, Nokia

Transport and concurrency
-------------------------

Abstraction for *concurrency* is just a class which implements *run* method so
that the code block associated with *start* is executed concurrently. This is
similar to *multiprocessing.Process* and *threading.Thread*.

The abstraction for the *transport* is defined so that if the code block of the
*start* of the *concurrency* contains *transport* implementation, then the
*transport* can send bytes to any address given in *start* (or later on
*receive*). It can also receive bytes from any *concurrency* execution which has
the address of the *transport* object.

Transport implementation
^^^^^^^^^^^^^^^^^^^^^^^^

One implementation for transport is provided by *stagecrew*. This
implementation is Unix Domain Socket (UDS) based. Each execution unit with
transport has unique file name (in e.g. current working directory) for UDS.
For more detail implementation there are many Python examples using sockets and
especially UDS (e.g.  `UDS socket example`_, `Python sockets`_ and
`TCP sockets`_).

The listening of the socket is done in a separate thread (listener thread).
This thread may also manage all connections which it passes to the *select* (or
*poll*) call. Actual receiving of the message is done in the single worker
thread or in the main thread. Alternatively first on listener thread, then on
receiver thread and only after that on the worker thread. The receiver thread
is possibly better as in that case the sending would not block even if the
capacity of the UDS is exceeded.  The socket on receiving side should be made
non-blocking. However, the sockets for sending messages should probably be
blocking: one thread per address. The sending part may block (e.g. if the other
end is slow in receive) It would be better to use internally *dequeue* and
*memoryview* as there is no need to pass Python objects in transport but just
bytes.

For unit testing purposes it is possible to provide the transport and the
concurrency pair implementation via asyncio_ in Python 3. However, in this case
it is not possible to test daemon actors. It is also possible to implement
parts of sender, listener and receiver threads using instead of threads
asyncio_. However, this solution is only available in Python 3 and so the
threading based solution has to be anyway implemented.

.. _`UDS socket example`: https://pymotw.com/3/socket/uds.html
.. _`Python sockets`:  https://docs.python.org/3/library/socket.html
.. _`TCP sockets`: https://steelkiwi.com/blog/working-tcp-sockets/
.. _`asyncio`: https://docs.python.org/3/library/asyncio.html
