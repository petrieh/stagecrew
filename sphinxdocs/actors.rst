.. Copyright (C) 2020, Nokia

Actors
------

Abstract actor
^^^^^^^^^^^^^^

Similarly like in Pykka_, the following built-in methods could be
implemented:

 - on_start

 - on_stop

 - on_failure

From Thespian_ the special *DeadLetter* can be used in case the message cannot
be delivered.

Moreover, the actor could respond with acknowledgement when it receives the
message.  It is quite obvious that the message handling may block
indefinitely. It is important to be able to distinguish between the cases
where the actor never receives the actual message (which should cause
DeadLetter in configured timeout) and that the action itself hangs.

The transport layer may use also acknowledgements but it this is not
implemented in *stagecrew*. The reasoning is that it UDS rather robust.

As in Pykka_ actors are called via proxies which are returned in the actor
creation.  The proxy has the same public methods than the actual actor. The
actor system transforms the proxy calls to the messaging between the proxy and the
Actor. The return values of the calls are either *futures* or alternatively, in
the call the handler method for the response can be given. The latter is
obviously for the proxy calls from the actor. In the actor, the *futures*
cannot be used nicely as the *get* method expects message to be received. This
is a deadlock, because the receiving of the messages are done in the single
thread. However, the *futures* are useful from calls from the outside of the
actor system as there it is possible to receive the message independently
from the actor receive system.

In addition to the simple *get* method in the *future* like implemented in
Pykka_ it would be useful to implement iterator *future*. The reasoning is
simply that the actor may send multiple messages in the tell fashion. The
receiving of such stream of the messages would be rather clumsy with *get*
only.


Stageman
^^^^^^^^

Simple implementation for the *stageman* actor is provided. The duty of the
*stageman* is to manage actor system. It can for example modify transport on
need bases. It can also kill malfunctioning actors and stop the actor system on
need bases. All actor creations and closings are reported to *stageman* so that
it has up to date information about the actor system.

File manager
^^^^^^^^^^^^

The file manager actor is for file and directory copying between actors.

Command Executor
^^^^^^^^^^^^^^^^

The command executor is for executing shell commands via *subprocess*.

Python object proxy
^^^^^^^^^^^^^^^^^^^

Python object proxy actor creates Python objects and stores them into the state
of it. The methods of the proxies can be called similarly like in
*crl.interactivesessions.remoteproxies* proxies. The basic idea is to implement
replacement for the current global store for the proxies.

Logging
^^^^^^^

Logging should be built-in functionality in the actor base. In addition, it is
useful to write simple implementation as an actor for the logging.  Basically,
this means that the actor base should should get the address of the logging
actor (of course configurable). In *stagecrew* the implementation could be
simply writing the received logs to the specified file.

Reminder
^^^^^^^^

Reminder actor implements timeouts. This could be built-in functionality. For
example in case the actor asks other actor, then the handler could create
reminder actor and ask. If the reminder returns before the asking response,
then the timeout handler is called otherwise the actual response handler.

Actor system messaging
^^^^^^^^^^^^^^^^^^^^^^

The messages are basically sequentially numbered Python objects serialized by
*pickle*.  The messages contains also the header: the sender and the target
address. The actor system may request again messages if it notices gaps. The
actor creation message may contain meta-data which can be used for deciding
e.g. how and where the new actor should be launched. For example, in meta-data
can be given the instruction to start the actor in the daemon mode.

In more detail, the actor messages are tuples containing method names
and proprietary serialization of the arguments. Basically, all Python objects
are serialized with *pickle*. The exceptions are the proxy objects, string and
bytes like objects. String and bytes have special serialization because they
have to work still on cross Python 2 and Python 3 platforms.

.. _`Pykka`: https://www.pykka.org
.. _`Thespian`: https://thespianpy.com
.. _`Actor model`: https://en.wikipedia.org/wiki/Actor_model
