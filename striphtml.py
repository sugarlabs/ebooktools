#! /usr/bin/env python
from BeautifulSoup import  BeautifulSoup

def _attr_name_whitelisted(attr_name,  attr_value):
    if attr_name.lower() == "align" and attr_value.lower() == "center":
        return True
    elif attr_name.lower() == "class" and attr_value == "blockquote":
        return True
    elif attr_name.lower() == "src":
        return True
    else:
        return False

# remove these tags, complete with contents.
blacklist = ["head" ]
    
striplist = [ "p",  "h1",  "h2",  "h3" ]

whitelist = [
    "p", "br", "pre", "meta", 
    "table", "tbody", "thead", "tr", "td", "a",
    "blockquote", "h1", "h2",  "h3",  "h4", 
    "ul", "li",  "img", 
    "b", "em", "i", "strong", "u"                 
    ]

soup = BeautifulSoup(open("input.html"))

print "<html>\n<head>\n"
print "<meta http-equiv=\"CONTENT-TYPE\" content=\"text/html; charset=UTF-8\">"
print soup.title
print "<link href=\"../Styles/ebook.css\" rel=\"stylesheet\" type=\"text/css\"/>"
print "\n<head>\n<body>"

print "<h1>Contents</h1>"
print "<ul>"
print "<li><a href=\"TOC_0001.xhtml\">Title Page</a></li>"
i = 1
for chapter in soup.findAll("h1"):
    i = i + 1
    print("<li><a href=\"TOC_" + str(i).zfill(4) + ".xhtml\">")
    print(chapter.string)
    print("</a></li>")
    
print "</ul>"
print "<hr class=\"sigilChapterBreak\" />"

print "<p class=\"title\">"
print soup.title.string
print "</p>"

print "<p class=\"author\">Author Name</p>"

for tag in soup.findAll():
    if tag.name.lower() in blacklist:
        # blacklisted tags are removed in their entirety
        tag.extract()
    elif tag.name.lower() in striplist:
        tag.attrs = [(a[0], a[1]) for a in tag.attrs if _attr_name_whitelisted(a[0],  a[1])]
    elif tag.name.lower() not in whitelist:
        # not a whitelisted tag. I'd like to remove it from the tree
        # and replace it with its children. But that's hard. It's much
        # easier to just replace it with an empty span tag.
        tag.name = "span"
        tag.attrs = []

print(soup.renderContents("utf-8"))
print "</body></html>"
