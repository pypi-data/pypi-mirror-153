<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%import clld_corpus_plugin.util as cutil%>
<link rel="stylesheet" href="${req.static_url('clld_corpus_plugin:static/clld-corpus.css')}"/>
<%! active_menu_item = "texts" %>


<h3>${_('Text')} “${ctx.name}”</h3>
<dl>
    % if ctx.source:
        <dt>Source</dt> <dd>${h.link(request, ctx.source)}</dd>
    % endif
    % if ctx.description:
        <dt>Summary</dt> <dd>${h.text2html(h.Markup(ctx.description))}</dd>
    % endif
    % if ctx.tags:
        <dt>Tags</dt> <dd>
        % for tag in ctx.tags:
            ${h.link(request, tag.tag)}
        % endfor
        </dd>
    % endif
    % if ctx.text_metadata:
        % for key, value in ctx.text_metadata.items():
            <dt>${key.capitalize()}</dt> <dd>${value}</dd>
        % endfor
    % endif
</dl>

<ol>
% for s in sorted(ctx.sentences, key=lambda x: x.part_no):
${cutil.rendered_sentence(request, s.sentence, text_link=False, sentence_link=True)}
% endfor
</ol>

<script src="${req.static_url('clld_corpus_plugin:static/clld-corpus.js')}">
</script>

<script>
number_examples()
</script>