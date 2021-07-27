FROM scratch
COPY . /

{% if docker.entrypoint -%}
ENTRYPOINT {{docker.entrypoint}}
{% endif -%}
{% if docker.cmd -%}
CMD {{docker.cmd}}
{% endif -%}

{% if docker.workdir is not none %}
WORKDIR {{docker.workdir}}
{% endif %}

{% for env in docker.envs %}
ENV {{env}}
{% endfor %}
