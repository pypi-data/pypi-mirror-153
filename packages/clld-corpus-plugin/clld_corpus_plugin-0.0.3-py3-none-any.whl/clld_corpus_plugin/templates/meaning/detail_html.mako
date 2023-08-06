<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_corpus_plugin:static/clld-corpus.css')}"/>
<%import clld_corpus_plugin.util as cutil%>
<%! active_menu_item = "meanings" %>

<h2>${_('Meaning')} ‘${ctx.name}’</h2>

<h3>${_('Forms')}</h3>
<ol>
% for form in ctx.forms:
    <li>${h.link(request, form.form)}</li>
% endfor
</ol>

<h3>${_('Sentences')}</h3>
<ol class="example">
    <% form_ids = [] %>
    % for form_meaning in ctx.forms:
        ${form_meaning.form}
        % for form_token in form.form_tokens:
            ${cutil.rendered_sentence(request, form_token.sentence, sentence_link=True)}
          <% form_ids.append(form_token.form.id) %>
        % endfor
    % endfor
</ol>

% for form_id in set(form_ids):
    <script>
var highlight_targets = document.getElementsByName("${form_id}");
for (index = 0; index < highlight_targets.length; index++) {
    highlight_targets[index].children[0].classList.add("corpus-highlight");
}
</script>

%endfor

