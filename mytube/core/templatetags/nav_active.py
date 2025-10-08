from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, url_name): 
    """
    Compares the url name from the parameters and the passed url name
    if converges returns: 'active' else ''
    """
    return "active" if context["request"].resolver_match.url_name == url_name else ""


@register.simple_tag(takes_context=True)
def active_tags(context, tag_id):
    """
    Compares the tag ID from the parameters and the passed ID
    if converges returns: 'active' else ''
    """
    request = context["request"]
    current_tag = request.GET.get("tag")
    return "active" if str(tag_id) == current_tag else ""