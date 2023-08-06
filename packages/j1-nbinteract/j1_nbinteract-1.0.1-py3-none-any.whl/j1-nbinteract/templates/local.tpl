{#
Like the full.tpl template but loads a local copy of the j1-nbinteract library
instead of using unpkg.com. Used for development purposes only alongside the
webpack-dev-server.
#}

{%- extends 'full.tpl' -%}

{% block j1-nbinteract_script %}
<!-- Loads j1-nbinteract package -->
<script src="http://localhost:8080/index.bundle.js"></script>
<script>
  var interact = new j1-nbinteract({
    nbUrl: 'http://localhost:8889/',
  })
  interact.prepare()
</script>
{%- endblock j1-nbinteract_script %}
