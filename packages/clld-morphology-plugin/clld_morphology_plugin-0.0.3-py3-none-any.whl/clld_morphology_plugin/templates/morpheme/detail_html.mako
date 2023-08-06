<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%namespace name="mutil" file="../morphology_util.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>
% try:
    <%from clld_corpus_plugin.util import rendered_sentence%>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry 

<%! active_menu_item = "morphemes" %>


<%doc><h2>${_('Morpheme')} ${ctx.name} (${h.link(request, ctx.language)})</h2>
</%doc>

<h3>${_('Morpheme')} <i>${ctx.name}</i></h3>

<table class="table table-nonfluid">
    <tbody>
<%doc>        <tr>
            <td>Label:</td>
            <td>${ctx.name}</td>
        </tr></%doc>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
        <tr>
            <td>Allomorphs:</td>
            <td>
                % for i, morph in enumerate(ctx.allomorphs):
                    % if i < len(ctx.allomorphs)-1:
                        <% comma = "," %>
                    % else:
                        <% comma = "" %>
                    % endif
                <i>${h.link(request, morph)}</i>${comma}
                % endfor
            </td>
        </tr>
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
        % if contribution in dir(ctx):
        <tr>
            <td> Contribution:</td>
            <td>
                ${h.link(request, ctx.contribution)} by
% for contributor in ctx.contribution.primary_contributors:
${h.link(request, contributor)}
% endfor
            </td>
        </tr>
        % endif
    </tbody>
</table>


% if len(ctx.allomorphs[0].forms) > 0:
    <% meaning_forms = {} %>
    <% meaning_sentences = {} %>
    <h3>${_('Word forms')}</h3>
    <ol>
        % for morph in ctx.allomorphs:
            % for form_slice in morph.forms:
                % if not form_slice.morpheme_meaning:
                    <li>${h.link(request, form_slice.form)}</li>
                % else:
                    <% meaning_forms.setdefault(form_slice.morpheme_meaning,    [])%>
                    <% meaning_forms[form_slice.morpheme_meaning].append(   form_slice.form) %>
                    % if getattr(form_slice.form_meaning, "form_tokens", None):
                        <% meaning_sentences.setdefault(    form_slice.morpheme_meaning, [])%>
                        <%meaning_sentences[form_slice.morpheme_meaning].extend(    form_slice.form_meaning.form_tokens)%>
                    % endif
                % endif
            % endfor
        % endfor
    </ol>
    % for meaning, forms in meaning_forms.items():
        <h5> As ‘${h.link(request, meaning.meaning)}’:</h5>
        <ol>
            % for form in forms:
                <li>${h.link(request, form)} (${form.pos.id})</li>
            % endfor
        </ol>
    % endfor
    % if len(meaning_sentences) > 0:
        <h3>${_('Sentences')}</h3>
        % for morpheme_meaning, sentences in meaning_sentences.items():
            <div id=${morpheme_meaning.id}>
                <h4> As ‘${h.link(request, morpheme_meaning.meaning)}’:</h4>

                <button type="button" class="btn btn-primary" onclick="copyIDs('${morpheme_meaning.id}-ids')">Copy IDs</button>

                <code class="id_list" id=${morpheme_meaning.id}-ids>${" ".join([x.sentence.id for x in sentences])}</code>

                <ol class="example">
                    % for sentence in sentences:
                            ${rendered_sentence(request, sentence.sentence, sentence_link=True)}
                    % endfor
                </ol>
            </div>
            <script>
                var highlight_div = document.getElementById("${morpheme_meaning.id}");
                var highlight_targets = highlight_div.querySelectorAll("*[name*='${morpheme_meaning.id}']")
                for (index = 0; index < highlight_targets.length; index++) {
                    highlight_targets[index].classList.add("morpho-highlight");
                }
            </script>
        % endfor
    % endif
% endif

<script src="${req.static_url('clld_morphology_plugin:static/clld-morphology.js')}"></script>
