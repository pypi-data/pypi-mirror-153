<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>
<%import clld_morphology_plugin.util as mutil%>
<%! active_menu_item = "meanings" %>

<h2>${_('Meaning')} ‘${ctx.name}’</h2>

%if ctx.forms:
    <h3>${_('Forms')}</h3>
    <ol>
        % for form in ctx.forms:
            <li>${h.link(request, form.form)}</li>
    % endfor
    </ol>
%endif

% if ctx.morphemes:
    <h3>${_('Morphemes')}</h3>
    <ol>
        % for m in ctx.morphemes:
            <li>${h.link(request, m.morpheme)}</li>
        % endfor
    </ol>
%endif