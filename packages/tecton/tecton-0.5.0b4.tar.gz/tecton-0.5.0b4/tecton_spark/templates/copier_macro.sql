{% macro copy_into(destination, source, materialization_schema, cast_types) %}
COPY INTO {{ destination }}
FROM (
    SELECT
        {%- for column in materialization_schema.columns %}
            {{ column.name }}
            {%- if cast_types[column.feature_server_type] != None -%}
                ::{{cast_types[column.feature_server_type]}} AS {{column.name}}
            {%- endif %}
            {%- if not loop.last %}, {%- endif %}
        {%- endfor %}
    FROM ({{ source }})
)
header = true
detailed_output = true
file_format = (type=parquet)
{% endmacro %}
