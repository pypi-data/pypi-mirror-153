Registering dashboard widgets
=============================

Apps can register their own dashboard widgets which are automatically registered in the corresponding frontend for
configuring them.

To implement a widget, add a model that subclasses ``DashboardWidget``, set the template
and implement the ``get_context`` method to return a dictionary to be passed as context
to the template. The template system works as in every Django view and allows you to use the normal Django
template language.

If your widget does not add any custom database fields, you should mark it as a proxy model.

You can provide a ``Media`` meta class with custom JS and CSS files which
will be added to the HTML head on the dashboard if the dashboard widget is shown.
For further information on media definition, see `Django Media`_.

Example::

  from django.forms.widgets import Media

  from aleksis.core.models import DashboardWidget

  class MyWidget(DashboardWidget):
      template = "myapp/widget.html"

      def get_context(self, request):
          context = {"some_content": "foo"}
          return context

      class Meta:
          proxy = True

      media = Media(css={
              'all': ('pretty.css',)
          },
          js=('animations.js', 'actions.js')
      )

.. _Django Media: https://docs.djangoproject.com/en/3.0/topics/forms/media/
