{# Renders CSS for j1-nbinteract-specific layouting. Only included in full.tpl. #}
{# Keep classes in sync with plain.tpl #}
{%- macro j1-nbinteract_css() -%}
    <style>
        .cell.j1-nbinteract-left {
            width: 50%;
            float: left;
        }

        .cell.j1-nbinteract-right {
            width: 50%;
            float: right;
        }

        .cell.j1-nbinteract-hide_in > .input {
            display: none;
        }

        .cell.j1-nbinteract-hide_out > .output_wrapper {
            display: none;
        }

        .cell:after {
          content: "";
          display: table;
          clear: both;
        }

        div.output_subarea {
            max-width: initial;
        }

        .jp-OutputPrompt {
            display: none;
        }
    </style>
{%- endmacro %}
