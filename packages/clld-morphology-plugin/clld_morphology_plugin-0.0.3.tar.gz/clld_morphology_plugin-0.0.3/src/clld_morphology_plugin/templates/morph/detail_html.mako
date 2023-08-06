<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>

% try:
    <%from clld_corpus_plugin.util import rendered_sentence%>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry 
<%! active_menu_item = "morphs" %>


<%doc><h2>${_('Morph')} ${ctx.name} (${h.link(request, ctx.language)})</h2>
</%doc>

<h3>${_('Morph')} <i>${ctx.name}</i></h3>

<table class="table table-nonfluid">
    <tbody>
<%doc>        <tr>
            <td>Form:</td>
            <td>${ctx.name}</td>
        </tr></%doc>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
        <tr>
            <td> Morpheme:</td>
            <td>${h.link(request, ctx.morpheme)}</td>
        </tr>
        <tr>
            <td> Meanings:</td>
            <td>
                <ol>
                    % for meaning in ctx.morpheme.meanings:
                        <li> ‘${h.link(request, meaning.meaning)}’ </li>
                    % endfor
                </ol>
            </td>
        </tr>
        % if cognates in dir(ctx):
        <tr>
            <td>Cognate set(s):</td>
            <td>
              <%
                cogsets = []
              %>
                    % for c in ctx.cognates:
                        % if c.cognateset not in cogsets:
                            <%
                                cogsets.append(c.cognateset)
                            %>
                        % endif
                    % endfor
                    ${h.text2html("*"+"+".join([h.link(request, c) for c in cogsets]))}
            </td>
            % for c in ctx.cognates:
                ${type(c.cognateset)}
            % endfor
        </tr>
        % endif
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

% if ctx.forms:
    <% meaning_forms = {} %>
    <% meaning_sentences = {} %>
    <h3>${_('Word forms')}</h3>
    <ol>
        % for form_slice in ctx.forms:
            % if not form_slice.morpheme_meaning:
                <li>${h.link(request, form_slice.form)}</li>
            % else:
                <% meaning_forms.setdefault(form_slice.morpheme_meaning, [])%>
                <% meaning_forms[form_slice.morpheme_meaning].append(form_slice.form) %>
                % if getattr(form_slice.form_meaning, "form_tokens", None):
                    <% meaning_sentences.setdefault(form_slice.morpheme_meaning, [])%>
                    <%meaning_sentences[form_slice.morpheme_meaning].extend(form_slice.form_meaning.form_tokens)%>
                % endif
            % endif
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
            <h4> As ‘${h.link(request, morpheme_meaning.meaning)}’:</h4> <button type="button" class="btn btn-primary" onclick="copyIDs('${morpheme_meaning.id}-ids')">Copy IDs</button>

            <code class="id_list" id=${morpheme_meaning.id}-ids>${" ".join([x.sentence.id for x in sentences])}</code>

                <ol class="example">
                    % for sentence in sentences:
                        ${rendered_sentence(request, sentence.sentence, sentence_link=True)}
                    % endfor
                </ol>
        </div>
        <script>
        var highlight_div = document.getElementById("${morpheme_meaning.id}");
        var highlight_targets =     highlight_div.querySelectorAll("*[name='${ctx.id}-${morpheme_meaning.id}']")
        for (index = 0; index < highlight_targets.length; index++) {
            highlight_targets[index].classList.add("morpho-highlight");
        }
        </script>
        % endfor
    % endif
% endif

<script src="${req.static_url('clld_morphology_plugin:static/clld-morphology.js')}"></script>
