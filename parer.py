from bs4 import BeautifulSoup, PageElement
import requests

f = open("template/bestiary.html", 'r', encoding='UTF-8')
bestiaryTemplateData = f.read()
f.close()

f = open("input.txt", 'r', encoding='UTF-8')
urls = f.readlines()
f.close()


bestiaryTemplateSoup = BeautifulSoup(bestiaryTemplateData, "html.parser");
bestiaryTemplateContents = bestiaryTemplateSoup.find("main")
bestiaryTemplateContents.clear()


for url in urls:
    targetBestiaryUrl = url.replace('\n', "")
    targetBestiaryPage = requests.get(targetBestiaryUrl)
    targetBestiarySoup = BeautifulSoup(targetBestiaryPage.content, "html.parser")


    # remove ads
    ad = targetBestiarySoup.find("article-content-autowrap-1")
    if ad is not None:
        ad.decompose()


    # remove some elements
    targetBestiaryContents = targetBestiarySoup.find("article")
    targetBestiaryContents.find("div", "page-widget top-post").decompose()
    targetBestiaryContents.find("div", "col-sm-3 col-md-3 col-lg-2 col-xs-12 right-sidebar").decompose()
    targetBestiaryContents.find("script").decompose()

    # # setup each contencts layout
    # # description
    statblockTag = targetBestiarySoup.new_tag("div", attrs={"class": "statblock"})
    targetBestiaryContents.find(attrs={"class": "description"}).wrap(statblockTag)

    # # ECOLOGY
    statblockTag = targetBestiarySoup.new_tag("div", attrs={"class": "statblock"})
    statblockTarget = targetBestiaryContents.find("p", string="ECOLOGY")
    statblockTargets = []
    sibling = statblockTarget
    while True:
        statblockTargets.append(sibling)
        sibling = sibling.next_sibling
        if sibling == None:
            break
    for target in statblockTargets:
        target.wrap(statblockTag)

    # insert bestiary contents
    layout = targetBestiarySoup.new_tag("div", attrs={"style": "border: none; float:left; width:50%;"})
    targetBestiaryContents.wrap(layout)
    bestiaryTemplateContents.append(str(layout.prettify()))
    # bestiaryTemplateContents.append(str(targetBestiaryContents.prettify()))




f = open("./output.html", "w", encoding='UTF-8')
outputStr = str(bestiaryTemplateSoup.prettify()).replace("&amp;gt;", ">").replace("&gt;", ">").replace("&lt;", "<").replace("../", "")
f.write(outputStr)
f.close()

