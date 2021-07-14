FROM scratch
COPY . /

{% if docker.entrypoint -%}
ENTRYPOINT {{docker.entrypoint}}
{% endif -%}
{% if docker.cmd -%}
CMD {{docker.cmd}}
{% endif -%}

{% for env in docker.envs %}
ENV {{env}}
{% endfor %}