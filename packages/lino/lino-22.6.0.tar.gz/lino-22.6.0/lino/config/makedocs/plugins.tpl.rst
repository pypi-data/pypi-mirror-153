{{header(1, str(_("Plugins")))}}

.. toctree::
    :maxdepth: 2
    :hidden:

{% for p in settings.SITE.installed_plugins %}
    {{p.app_label}}
{% endfor  %}

{% for p in settings.SITE.installed_plugins %}
- :doc:`{{p.app_label}}` (:mod:`{{p.app_name}}`)
  {{makedocs.generate('makedocs/plugin.tpl.rst', p.app_label+'.rst', plugin=p)}}

{% endfor  %}
