#! /usr/bin/env python
from BeautifulSoup import  BeautifulSoup

def _attr_name_whitelisted(attr_name,  attr_value):
    if attr_name.lower() == "align" and attr_value.lower() == "center":
        return True
    elif attr_name.lower() == "class" and attr_value == "blockquote":
        return True
    else:
        return False

# remove these tags, complete with contents.
blacklist = ["head",  "div" ]
    
striplist = [ "p",  "h1",  "h2",  "h3" ]

whitelist = [
    "p", "br", "pre", "meta", 
    "table", "tbody", "thead", "tr", "td", "a",
    "blockquote", "h1", "h2",  "h3",  "h4", 
    "ul", "li",  
    "b", "em", "i", "strong", "u"                 
    ]

soup = BeautifulSoup(open("input.html"))

print "<html>\n<head>\n<meta http-equiv=\"CONTENT-TYPE\" content=\"text/html; charset=UTF-8\">"
print soup.title
print "<style type='text/css'>"
print "@font-face {\n    font-family: Yataghan;\n    src: url('../Fonts/yataghan.ttf');\n }"
print "@font-face {\n    font-family: Akashi;\n    src: url('../Fonts/akashi.ttf');\n }"
print "p {\n    text-align: left;\n      text-indent: 0;\n    margin-bottom: .5em;\n  }\n  h1,h2,h3 {\n    font-family: Yataghan; text-align: center; margin-top: 3em; margin-bottom: .5em;    clear: both;  }" 
print "p.blockquote {\n    text-align: left;\n      text-indent: 0;\n    margin-bottom: .5em;\n    margin-left: .5in;\n    margin-right: .5in;  }" 
print "</style>\n<head>\n<body>"

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

print "<p style=\"font-family: Akashi; text-align: center; font-size: 3em; font-weight: bold\">"
print soup.title.string
print "</p>"

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
