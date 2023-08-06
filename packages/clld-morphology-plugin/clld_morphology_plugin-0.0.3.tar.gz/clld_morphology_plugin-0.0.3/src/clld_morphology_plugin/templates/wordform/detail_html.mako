<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>
% try:
    <%from clld_corpus_plugin.util import rendered_sentence%>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry
<%! active_menu_item = "wordforms" %>


<%doc><h2>${_('Form')} ${ctx.name} (${h.link(request, ctx.language)})</h2>
</%doc>


<h3>${_('Form')} <i>${ctx.name}</i></h3>

<table class="table table-nonfluid">
    <tbody>
<%doc>        <tr>
            <td>Form:</td>
            <td>${ctx.name}</td>
        </tr></%doc>
        % if ctx.morphs:
        <tr>
            <td>Structure:</td>
            <td>
                    ${h.text2html("-".join([h.link(request, slice.morph, label=string) for string, slice in zip(ctx.segmented.split("-"), ctx.morphs)]))}
            </td>
        </tr>
        % endif
        <tr>
            <td> Meanings:</td>
            <td>
                <ol>
                    % for meaning in ctx.meanings:
                        <li> ‘${h.link(request, meaning.meaning)}’ </li>
                    % endfor
                </ol>
            </td>
        </tr>
        % if ctx.pos:
        <tr>
            <td>Part of speech:</td>
            <td>
                ${h.link(request, ctx.pos)}
            </td>
        </tr>
        % endif
        % if getattr(ctx, "segments", None):
            <tr>
                <td>Segments:</td>
                <td>
                % for segment in ctx.segments:
                ${h.link(request, segment.phoneme)}
                    % endfor</td>
            </tr>
        % endif
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
    </tbody>
</table>

% if ctx.audio:
    <audio controls="controls"><source src="/audio/${ctx.audio}" type="audio/x-wav"></source></audio>
% endif 

% if getattr(ctx.meanings[0], "form_tokens", None):
    <h3>${_('Sentences')}</h3>
    % for form_meaning in ctx.meanings:
        <h4>‘${h.link(request, form_meaning.meaning)}’:</h4>
        <ol class="example">
            % for form_token in form_meaning.form_tokens:
                ${rendered_sentence(request, form_token.sentence,       sentence_link=True)}
            % endfor
        </ol>
    % endfor
% endif

<script>
var highlight_targets = document.getElementsByName("${ctx.id}");
for (index = 0; index < highlight_targets.length; index++) {
    highlight_targets[index].children[0].classList.add("morpho-highlight");
}
</script>