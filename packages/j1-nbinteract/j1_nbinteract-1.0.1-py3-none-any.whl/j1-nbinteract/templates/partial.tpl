{#
Outputs an HTML partial for embedding in other pages. Like the plain.tpl
template but also loads the j1-nbinteract library.
#}

{%- extends 'plain.tpl' -%}

{% block body %}
{{ super() }}

{% block j1-nbinteract_script %}
<!-- Loads j1-nbinteract package -->
<script src="https://unpkg.com/j1-nbinteract-core" async></script>
<script>
  (function setupj1-nbinteract() {
    // If j1-nbinteract hasn't loaded, wait one second and try again
    if (window.j1-nbinteract === undefined) {
      setTimeout(setupj1-nbinteract, 1000)
      return
    }

    var interact = new window.j1-nbinteract({
      spec: '{{ spec }}',
      baseUrl: '{{ base_url }}',
      provider: '{{ provider }}',
    })
    interact.prepare()

    window.interact = interact
  })()
</script>
{%- endblock j1-nbinteract_script %}

{%- endblock body %}
