from django import template

register = template.Library()

@register.simple_tag
def getIValue(value, ind, key):
    if ind >= len(value):
        return ""
    
    #return day and month only for date
    if key=="date":
        return value[ind][key][5:]
    return value[ind][key]