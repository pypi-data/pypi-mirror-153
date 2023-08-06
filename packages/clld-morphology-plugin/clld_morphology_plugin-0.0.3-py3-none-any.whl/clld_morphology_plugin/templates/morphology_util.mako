<%def name="morph_sentences(request, ctx, rendered_sentence)">
<%sentences = []%>
% if getattr(ctx.forms[0].form, "sentence_assocs", None):
    <ol>
        % for form_slice in ctx.forms:
            % for s in form_slice.form.sentence_assocs:
                <%sentences.append(s.sentence)%>
            % endfor
        % endfor
        % for s in set(sentences):
            ${rendered_sentence(request, s, sentence_link=True)}
        %endfor
    </ol>
    
    <script>
    var highlight_targets = document.getElementsByName("${ctx.id}");
    console.log(highlight_targets)
    for (index = 0; index < highlight_targets.length; index++) {
        highlight_targets[index].classList.add("morpho-highlight");
    }
    console.log(highlight_targets)
    </script>
%endif
</%def>

