{{header(1, str(_("Data views")))}}

.. toctree::
    :maxdepth: 2
    :hidden:

{% for a in actors.actors_list if not a.abstract %}
    {{a}}{{makedocs.generate('makedocs/actor.tpl.rst', str(a)+'.rst', actor=a)}}
{% endfor  %}

{{actors2table()}}
