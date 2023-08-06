from content.models import Snippet, Page


def content(request):
    return {
        "page": Page.objects.get_current(request.path)
    }


def content_snippets(request):
    snippets = Snippet.objects.from_url(request.path).prefetch_related(
        'options', 'section')
    by_section = {}
    for s in snippets:
        n = s.section.name
        if n not in by_section:
            by_section[n] = []
        by_section[n].append(s)

    return {'content_snippets': by_section}
