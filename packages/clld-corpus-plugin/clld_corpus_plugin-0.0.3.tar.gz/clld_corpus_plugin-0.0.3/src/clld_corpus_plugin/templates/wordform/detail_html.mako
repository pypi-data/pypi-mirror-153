<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%import clld_corpus_plugin.util as cutil%>
<link rel="stylesheet" href="${req.static_url('clld_corpus_plugin:static/clld-corpus.css')}"/>
<%! active_menu_item = "wordforms" %>


<%doc><h2>${_('Form')} ${ctx.name} (${h.link(request, ctx.language)})</h2>
</%doc>

<h3>${_('Form')} <i>${ctx.name}</i></h3>

<table class="table table-nonfluid">
    <tbody>
        <tr>
            <td> Meanings:</td>
            <td>
                <ol>
                    % for meaning in ctx.meanings:
                        <li> ${h.link(request, meaning.meaning)} </li>
                    % endfor
                </ol>
            </td>
        </tr>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
    </tbody>
</table>

<h3>${_('Sentences')}</h3>
% for form_meaning in ctx.meanings:
    ‘${h.link(request, form_meaning.meaning)}’:
    <ol class="example">
        % for form_token in form_meaning.form_tokens:
            ${cutil.rendered_sentence(request, form_token.sentence,     sentence_link=True)}
        % endfor
    </ol>
% endfor

<script>
var highlight_targets = document.getElementsByName("${ctx.id}");
for (index = 0; index < highlight_targets.length; index++) {
    highlight_targets[index].children[0].classList.add("corpus-highlight");
}
</script>