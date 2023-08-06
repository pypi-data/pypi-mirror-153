{{header(1, "``{}`` : {}".format(plugin.app_label, plugin.short_name))}}

{{plugin_overview(plugin)}}

See also :mod:`{{plugin.app_name}}`.

Models
======

{% for model in get_models() if model.app_label == plugin.app_label %}
- :doc:`{{full_model_name(model)}}` :
  {{abstract(model, 2)}}

{% endfor %}

Actors
======

{% for a in actors.actors_list if a.app_label == plugin.app_label %}
{% if not a.abstract %}
- :doc:`{{a.label}} <{{a}}>` :
  {{abstract(a, 2)}}

{% endif  %}
{% endfor %}
