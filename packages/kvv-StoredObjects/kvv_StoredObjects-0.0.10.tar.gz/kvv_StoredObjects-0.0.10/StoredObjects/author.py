from transliterate import translit
from bs4 import BeautifulSoup


class Author:

    def __init__(self, name):
        self.name = name
        self.engName = translit(name, 'ru', reversed=True)
        self.crossrefName = []
        self.scopusName = []
        self.affiliations = []
        self.orcID = None
        self.researcherID = None
        self.publonsID = None
        self.publications = []

    def getScopusName(self):
        if not self.scopusName:
            splitName = self.engName.split(' ')
            self.scopusName = (splitName[0], splitName[1][0] + '.' + splitName[2][0] + '.')
        return self.scopusName

    def checkSameAuthor(self, author):
        if (self.name == author.name): return True
        if (self.orcID == author.orcID): return True
        if (self.researcherID == author.researcherID): return True
        if (self.publonsID == author.publonsID): return True
        return False

    def searchPublicationByDOI(self, doi):
        for pub in self.publications:
            if pub.doi == doi:
                return pub
        return None
