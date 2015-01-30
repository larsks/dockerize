FROM scratch
COPY . /

{% if model.entrypoint %}
ENTRYPOINT {{model.entrypoint}}
{% endif %}
{% if model.cmd %}
CMD {{model.cmd}}
{% endif %}

