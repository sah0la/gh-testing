{{ fullname | underline }}

.. automodule:: {{ fullname }}
   :members:
   :no-private-members:
   :show-inheritance:
   :inherited-members:

.. autosummary::
   :toctree:
   :template: autosummary/module.rst
   :recursive:

   {% for item in modules %}
      {{ item }}
   {% endfor %}
