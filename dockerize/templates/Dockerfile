{% if docker.base -%}
FROM {{ docker.base }}
{% else -%}
FROM scratch
{% endif -%}
COPY . /

{% if docker.entrypoint -%}
ENTRYPOINT {{docker.entrypoint}}
{% endif -%}
{% if docker.cmd -%}
CMD {{docker.cmd}}
{% endif -%}
