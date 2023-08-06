<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%from clld_morphology_plugin.models import Wordform%>
<%! active_menu_item = "pos" %>


<h3>${ctx.name.capitalize()} (Part of speech, ${ctx.id})</h3>

% if ctx.description:
    ${ctx.description}
% endif

% if ctx.wordforms:
<h4>Wordforms:</h4>
<div>
    ${request.get_datatable('wordforms', Wordform, pos=ctx).render()}
</div>
% endif


