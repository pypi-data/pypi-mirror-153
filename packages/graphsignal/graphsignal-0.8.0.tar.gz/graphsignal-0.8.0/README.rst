Graphsignal Profiler
====================

|License| |Version| |Status|

Graphsignal is a machine learning profiler. It helps data scientists and
ML engineers make model training and inference faster and more
efficient. It is built for real-world use cases and allows ML
practitioners to:

-  Optimize training and inference by benchmarking and analyzing speed,
   compute and operation statistics.
-  Start profiling scripts and notebooks automatically by adding a few
   lines of code.
-  Use the profiler in local, remote or cloud environment without
   installing any additional software or opening inbound ports.
-  Keep data private; no code or data is sent to Graphsignal cloud, only
   run statistics and metadata.

|Dashboards|

Learn more at `graphsignal.com <https://graphsignal.com>`__.

Documentation
-------------

See full documentation at
`graphsignal.com/docs <https://graphsignal.com/docs/>`__.

Getting Started
---------------

1. Installation
~~~~~~~~~~~~~~~

Install the profiler by running:

::

   pip install graphsignal

Or clone and install the `GitHub
repository <https://github.com/graphsignal/graphsignal>`__:

::

   git clone https://github.com/graphsignal/graphsignal.git
   python setup.py install

Import the module in your application:

.. code:: python

   import graphsignal

For GPU profiling, make sure the `NVIDIA® CUDA® Profiling Tools
Interface <https://developer.nvidia.com/cupti>`__ (CUPTI) is installed
by running:

.. code:: console

   /sbin/ldconfig -p | grep libcupti

2. Configuration
~~~~~~~~~~~~~~~~

Configure the profiler by specifying your API key and workload name
directly or via environment variables.

.. code:: python

   graphsignal.configure(api_key='my_api_key', workload_name='job1')

To get an API key, sign up for a free account at
`graphsignal.com <https://graphsignal.com>`__. The key can then be found
in your account’s `Settings / API
Keys <https://app.graphsignal.com/settings/api_keys>`__ page.

``workload_name`` identifies the job, application or service that is
being profiled.

3. Profiling
~~~~~~~~~~~~

Use the following minimal examples to integrate Graphsignal into your
machine learning script. See integration documentation and `profiling
API reference <https://graphsignal.com/docs/profiler/api-reference/>`__
for full reference.

To ensure optimal statistics and low overhead, the profiler
automatically profiles only certain training steps and/or predictions.

`TensorFlow <https://graphsignal.com/docs/integrations/tensorflow/>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from graphsignal.profilers.tensorflow import profile_step

   with profile_step():
       # training batch, prediction, etc.

`Keras <https://graphsignal.com/docs/integrations/keras/>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from graphsignal.profilers.keras import GraphsignalCallback

   model.fit(..., callbacks=[GraphsignalCallback()])
   # or model.predict(..., callbacks=[GraphsignalCallback()])

`PyTorch <https://graphsignal.com/docs/integrations/pytorch/>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from graphsignal.profilers.pytorch import profile_step

   with profile_step():
       # training batch, prediction, etc.

`PyTorch Lightning <https://graphsignal.com/docs/integrations/pytorch-lightning/>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from graphsignal.profilers.pytorch_lightning import GraphsignalCallback

   trainer = Trainer(..., callbacks=[GraphsignalCallback()])

`Hugging Face <https://graphsignal.com/docs/integrations/hugging-face/>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from graphsignal.profilers.huggingface import GraphsignalPTCallback
   # or GraphsignalTFCallback for TensorFlow

   trainer = Trainer(..., callbacks=[GraphsignalPTCallback()])
   # or trainer.add_callback(GraphsignalPTCallback())

Other frameworks
^^^^^^^^^^^^^^^^

ML operation and kernel statistics are not supported by generic
profiler.

.. code:: python

   from graphsignal.profilers.generic import profile_step

   with profile_step():
       # training batch, prediction, etc.

Distributed workloads
^^^^^^^^^^^^^^^^^^^^^

Graphsignal has a built-in support for distributed training and
inference, e.g. multi-node and multi-gpu training. See `Distributed
Workloads <https://graphsignal.com/docs/profiler/distributed-workloads/>`__
section for more information.

4. Dashboards
~~~~~~~~~~~~~

After profiling is setup, `open <https://app.graphsignal.com/>`__ to
Graphsignal to analyze recorded profiles.

Example
-------

.. code:: python

   # 1. Import Graphsignal modules
   import graphsignal
   from graphsignal.profilers.keras import GraphsignalCallback

   # 2. Configure
   graphsignal.configure(api_key='my_key', workload_name='training_example')

   ....

   # 3. Add profiler callback or use profiler API
   model.fit(..., callbacks=[GraphsignalCallback()])

More integration examples are available in
```examples`` <https://github.com/graphsignal/examples>`__ repo.

Overhead
--------

Although profiling may add some overhead to applications, Graphsignal
Profiler only profiles certain steps, e.g. training batches or
predictions, automatically limiting the overhead.

Security and Privacy
--------------------

Graphsignal Profiler can only open outbound connections to
``profile-api.graphsignal.com`` and send data, no inbound connections or
commands are possible.

No code or data is sent to Graphsignal cloud, only run statistics and
metadata.

Troubleshooting
---------------

To enable debug logging, add ``debug_mode=True`` to ``configure()``. If
the debug log doesn’t give you any hints on how to fix a problem, please
report it to our support team via your account.

In case of connection issues, please make sure outgoing connections to
``https://profile-api.graphsignal.com`` are allowed.

.. |License| image:: http://img.shields.io/github/license/graphsignal/graphsignal
   :target: https://github.com/graphsignal/graphsignal/blob/main/LICENSE
.. |Version| image:: https://img.shields.io/github/v/tag/graphsignal/graphsignal?label=version
   :target: https://github.com/graphsignal/graphsignal
.. |Status| image:: https://img.shields.io/uptimerobot/status/m787882560-d6b932eb0068e8e4ade7f40c?label=SaaS%20status
   :target: https://stats.uptimerobot.com/gMBNpCqqqJ
.. |Dashboards| image:: https://graphsignal.com/external/screencast-dashboards.gif
   :target: https://graphsignal.com/
