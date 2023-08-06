{{header(1,"``{}`` ({})".format(full_model_name(model), model._meta.verbose_name))}}

{# doc2rst(model.__doc__) #}

{{model_overview(model)}}

.. Referenced from {#model_referenced_from(model)#}

{{header(2, str(_("Database fields")))}}

{{doctest.fields_help(model, all=True)}}
