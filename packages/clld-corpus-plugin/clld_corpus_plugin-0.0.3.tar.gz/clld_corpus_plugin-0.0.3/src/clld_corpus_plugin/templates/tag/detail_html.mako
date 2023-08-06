<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%import clld_corpus_plugin.util as cutil%>
<%! active_menu_item = "tags" %>

Tag <<b>${ctx.name}</b>>

% if ctx.texts:
    <div>
        Texts:
        <ol>
            % for text in ctx.texts:
                <li>${h.link(request, text.text)}</li>
            % endfor
        </ol>
    </div>
% endif

% if ctx.sentences:
    <div>
        Text records:
        <ol class="example">
            % for s in ctx.sentences:
                ${cutil.rendered_sentence(request, s.sentence)}
            % endfor
        </ol>
    </div>
% endif