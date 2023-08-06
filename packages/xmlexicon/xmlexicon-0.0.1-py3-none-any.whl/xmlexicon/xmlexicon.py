
# Commented out IPython magic to ensure Python compatibility.
import re 
import csv
from lxml import etree
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

class Dictionary():

  def __init__(self, csv_file):
    self.slovar = pd.read_csv(csv_file, sep=";", encoding="UTF-8")
    self._root = etree.Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
    self._teiheader = etree.Element("teiHeader", xml_lang="ru")
    self._root.append(self._teiheader)
    self.csv_file = csv_file

  def write_to_xml(self):
    etree.ElementTree(self._root).write(self.csv_file.strip(".csv")+'_TEI'+'.xml', pretty_print=True, xml_declaration = True, encoding='UTF-8', standalone = None)

class Epifanii_dict(Dictionary):

  def encode(self):
    self.slovar.columns = ["Griechisch", "GLemma", "GMSA", "Slavisch", "SÜbersetzung", "SemantK", "Lateinisch", "LLemma", "LGram"]
    self._file_desc()
    text = etree.SubElement(self._root, "text")
    self._body = etree.SubElement(text, "body")
    for self._index, row in self.slovar.iterrows():
      if self._index == 0:
        continue
      else:
        if type(row["Griechisch"]) != float:
          if type(row["GLemma"]) == float and type(row["SÜbersetzung"]) == float and type(row["LLemma"]) == float:
            self._page_note(row)
          if type(row["GLemma"]) != float:
            self._entry = etree.SubElement(self._body, "entry", xml_id=row["GLemma"], xml_lang="grc")
            form = etree.SubElement(self._entry, "form", type="hyperlemma")
            orth = etree.SubElement(form, "orth")
            orth.text = row["Griechisch"]
          else:
            continue
        if type(row["GLemma"]) != float:
          if type(row["Griechisch"]) == float:
            self._entry = etree.SubElement(self._body, "entry", xml_id=row["GLemma"], xml_lang="grc")
          form = etree.SubElement(self._entry, "form", type="lemma")
          orth = etree.SubElement(form, "orth")
          orth.text = row["GLemma"]
          if type(row["GMSA"]) != float: 
            self._grammar(row["GMSA"])
          if type(row["SÜbersetzung"]) != float:
            self._sense_greek = etree.SubElement(self._entry, "sense", xml_id=row["GLemma"]+".1")
            self._slavic_latin_translation(row)
            self._several_slavic_equivalents_check(self.slovar["SÜbersetzung"], self.slovar["Lateinisch"], self.slovar["LLemma"])
        if type(row["SemantK"]) != float:
          self._semantischer_kommentar(row)

  def _file_desc(self):
  
    fileDesc = etree.SubElement(self._teiheader, "fileDesc")
    titleStmt = etree.SubElement(fileDesc, "titleStmt")
    title = etree.SubElement(titleStmt, "title")
    title.text = "Лексикон греко-славяно-латинский"
    author = etree.SubElement(titleStmt, "author")
    author.text = "Епифаний Славинецкий"
    publication = etree.SubElement(fileDesc, "publicationStmt")
    p = etree.SubElement(publication, "p")
    p.text = "Не опубликован"
    source = etree.SubElement(fileDesc, "sourceDesc")
    msDesc = etree.SubElement(source, "msDesc")
    idm = etree.SubElement(msDesc, "msIdentifier")
    settlement = etree.SubElement(idm, "settlement")
    settlement.text = "Москва"
    institution = etree.SubElement(idm, "institution")
    institution.text = "Государственный исторический музей"
    repository = etree.SubElement(idm, "repository")
    repository.text = "Отдел рукописей и старопечатных книг, Синодальное собрание"
    idno = etree.SubElement(idm, "idno")
    idno.text = "№ 488"
    history= etree.SubElement(msDesc, "history")
    origin = etree.SubElement(history, "origin")
    origDate = etree.SubElement(origin, "origDate")
    origDate.text = "XVII в."
    origPlace = etree.SubElement(origin, "origPlace")
    origPlace.text = "Москва"
    profileDesc = etree.SubElement(self._teiheader, "profileDesc")
    langUsage = etree.SubElement(profileDesc, "langUsage")
    lang_grc = etree.SubElement(langUsage, "language", ident="grc")
    lang_grc.text = "Древнегреческий язык"
    lang_chu = etree.SubElement(langUsage, "language", ident="chu")
    lang_chu.text = "Церковнославянский язык"
    lang_lat = etree.SubElement(langUsage, "language", ident="lat")
    lang_lat.text = "Латинский язык"


  def _page_note(self, row):
    column = re.search("^(?P<f>f.)\s(?P<page_num>\d\d\d.).*(?P<side>linke|rechte)\s(?P<Spalte>Spalte)", row["Griechisch"])
    page = re.search("Kustode.*(?P<pg>\d\d\d.)", row["Griechisch"])
    if column:
      cb = etree.SubElement(self._body, "cb", pageside=column.group("page_num"), side=column.group("side"))
      cb.text = row["Griechisch"]
    if page:
      pb = etree.SubElement(self._body, "pb", n=page.group("pg"))
      pb.text = row["Griechisch"]
    if not column and not page:
      marg_note = etree.SubElement(self._body, "note")
      marg_note.text = row["Griechisch"]


  def _grammar(self, MSA):
    index = self._index
    noun = re.search("(ὁ|ἡ|τὸ)", MSA)
    nouns = re.search("(οἱ|αἱ|τὰ)", MSA)
    verb = re.search(r"((\\?μ),?\s(?P<aorist>.*?))?\s(.?(π),?\s(?P<perfect>.*))?", MSA)
    adj = re.search("((.*?),\s?)?(.?ὁ καὶ ἡ.?)", MSA)
    just_noun = re.search("(.*?),\s(ὁ|ἡ|τὸ)", MSA)
    genitive_noun = re.search("(?P<first>.*?)\s(καὶ)\s(?P<second>.*?),\s?(?P<gen>ὁ|ἡ|τὸ)", MSA)

    def _gen_check():
      if re.search("ὁ", MSA):
        gram = etree.SubElement(gramGrp, "gram", type="gen", value="m")
        gram.text = "ὁ"
      if re.search("ἡ", MSA):
        gram = etree.SubElement(gramGrp, "gram", type="gen", value="f")
        gram.text = "ἡ"
      if re.search("τὸ", MSA):
        gram = etree.SubElement(gramGrp, "gram", type="gen", value="n")
        gram.text = "τὸ"

    def _verb_gram(self):
      if type(MSA) != float and verb:
        verb1 =  re.search(r"((\\?μ),?\s(?P<aorist>.*?))?\s(.?(π),?\s(?P<perfect>.*))?", MSA)
        form = etree.SubElement(self._entry, "form", type="inflected")
        gramGrp = etree.SubElement(form, "gramGrp")
        gram = etree.SubElement(gramGrp, "gram", type="pos", value="verb")
        gram = etree.SubElement(gramGrp, "gram", type="tense", value="aorist")
        orth = etree.SubElement(form, "orth")
        orth.text = verb1.group("aorist")
        form = etree.SubElement(self._entry, "form", type="inflected")
        gramGrp = etree.SubElement(form, "gramGrp")
        gram = etree.SubElement(gramGrp, "gram", type="pos", value="verb")
        gram = etree.SubElement(gramGrp, "gram", type="tense", value="perfect")
        orth = etree.SubElement(form, "orth")
        orth.text = verb1.group("perfect")

    if type(MSA) != float and  type(self.slovar["GLemma"][index]) != float: 
        if adj:
          form = etree.SubElement(self._entry, "form", type="inflected")
          gramGrp = etree.SubElement(form, "gramGrp")
          gram = etree.SubElement(gramGrp, "gram", type="pos", value="adj")
          gram = etree.SubElement(gramGrp, "gram", type="number", value="sg")
          gram = etree.SubElement(gramGrp, "gram", type="gen", value="m")
          gram = etree.SubElement(gramGrp, "gram", type="gen", value="f")
          gram = etree.SubElement(gramGrp, "gram", type="case", value="genitiv")
          orth = etree.SubElement(form, "orth", extent="part")
          orth.text = MSA  
        elif noun:
          form = etree.SubElement(self._entry, "form", type="inflected")
          gramGrp = etree.SubElement(form, "gramGrp")
          gram = etree.SubElement(gramGrp, "gram", type="pos", value="noun")
          gram = etree.SubElement(gramGrp, "gram", type="number", value="sg")
          if re.search("^(ὁ|ἡ|τὸ)$", MSA):
            _gen_check()
          if just_noun:
            gram = etree.SubElement(gramGrp, "gram", type="case", value="genitiv")
            orth = etree.SubElement(form, "orth", extent="part")
            orth.text = just_noun.group(1)
            _gen_check()
          if genitive_noun:
            gram = etree.SubElement(gramGrp, "gram", type="case", value="genitiv")
            form_var1 = etree.SubElement(form, "form", type="variant", n="1")
            orth = etree.SubElement(form_var1, "orth", extent="part")
            orth.text = genitive_noun.group("first")
            form_var2 = etree.SubElement(form, "form", type="variant", n="2")
            orth = etree.SubElement(form_var2, "orth", extent="part")
            orth.text = genitive_noun.group("second")
            _gen_check()
        elif nouns:
          form = etree.SubElement(self._entry, "form", type="inflected")
          gramGrp = etree.SubElement(form, "gramGrp")
          gram = etree.SubElement(gramGrp, "gram", type="pos", value="noun")
          gram = etree.SubElement(gramGrp, "gram", type="number", value="pl")
          if re.search("οἱ", MSA):
            gram = etree.SubElement(gramGrp, "gram", type="gen", value="m")
            gram.text = "οἱ"
          if re.search("αἱ", MSA):
            gram = etree.SubElement(gramGrp, "gram", type="gen", value="f")
            gram.text = "αἱ"
          if re.search("τὰ", MSA):
            gram = etree.SubElement(gramGrp, "gram", type="gen", value="n")
            gram.text = "τὰ"
        elif MSA == "ῶ" and type(self.slovar["GMSA"][index+1]) != float and type(self.slovar["GLemma"][index+1]) == float:
          MSA = MSA+" "+ self.slovar["GMSA"][index+1]
          if type(self.slovar["GMSA"][index+2]) != float and type(self.slovar["GLemma"][index+2]) == float:
            MSA = MSA+" "+self.slovar["GMSA"][index+2]
          form = etree.SubElement(self._entry, "form", type="variant")
          gramGrp = etree.SubElement(form, "gramGrp")
          gram = etree.SubElement(gramGrp, "gram", type="pos", value="verb")
          gram = etree.SubElement(gramGrp, "gram")
          gram.text = "ῶ"
          _verb_gram(self)
        elif verb:
          if type(self.slovar["GMSA"][index+1]) != float and type(self.slovar["GLemma"][index+1]) == float:
            MSA = self.slovar.at[index, "GMSA"]+" "+self.slovar.at[index+1, "GMSA"]
            _verb_gram(self)
        elif MSA == "ῶ":
          form = etree.SubElement(self._entry, "form", type="variant")
          gramGrp = etree.SubElement(form, "gramGrp")
          gram = etree.SubElement(gramGrp, "gram")
          gram.text = "ῶ"
        else:
          form = etree.SubElement(self._entry, "form", type="inflected")
          gramGrp = etree.SubElement(form, "gramGrp")
          gram = etree.SubElement(gramGrp, "gram")
          orth = etree.SubElement(form, "orth")
          orth.text = MSA 


  def _slavic_latin_translation(self, row):
    index = self._index
    cit = etree.SubElement(self._sense_greek, "cit", type="translationEquivalent", xml_lang = "chu")
    form = etree.SubElement(cit, "form",  xml_id=row["SÜbersetzung"].strip(","))
    orth = etree.SubElement(form, "orth")
    orth.text = row["SÜbersetzung"].strip(",")
    if type(row["Lateinisch"]) != float and row["Lateinisch"] != "-":
          sense = etree.SubElement(cit, "sense", xml_id=row["SÜbersetzung"].strip(",")+".1")
          cit = etree.SubElement(sense, "cit", type="translationEquivalent", xml_lang = "lat")
          form = etree.SubElement(cit, "form", type="hyperlemma", xml_id=row["Lateinisch"])
          orth = etree.SubElement(form, "orth")
          if type(self.slovar["SÜbersetzung"][index+1]) == float \
          and type(self.slovar["Lateinisch"][index+1]) != float and self.slovar["Lateinisch"][index+1] != "-":
            orth.text = row["Lateinisch"]+" "+self.slovar["Lateinisch"][index+1]
          else:
            orth.text = row["Lateinisch"]
    if type(row["LLemma"]) != float and row["LLemma"] != "-":
      form = etree.SubElement(cit, "form", type="lemma", xml_id=row["LLemma"])
      orth = etree.SubElement(form, "orth")
      orth.text = row["LLemma"]


  def _several_slavic_equivalents_check(self, Slavic, Latin, LatLemma):
    index = self._index
    while type(self.slovar["GLemma"][index+1]) == float:
      if type(Slavic[index+1]) != float:
        cit = etree.SubElement(self._sense_greek, "cit", type="translationEquivalent", xml_lang = "chu")
        form = etree.SubElement(cit, "form",  xml_id=Slavic[index+1].strip(","))
        orth = etree.SubElement(form, "orth")
        orth.text = Slavic[index+1].strip(",")
        if type(Latin[index+1]) != float and Latin[index+1] != "-":
          sense = etree.SubElement(cit, "sense", xml_id=Slavic[index+1]+".1")
          cit = etree.SubElement(sense, "cit", type="translationEquivalent", xml_lang = "lat")
          form = etree.SubElement(cit, "form", type="hyperlemma", xml_id=Latin[index+1])
          orth = etree.SubElement(form, "orth")
          if type(Slavic[index+2]) == float and type(Latin[index+2]) != float and Latin[index+2] != "-": 
            orth.text = Latin[index+1]+" "+Latin[index+2]
            if type(Slavic[index+3]) == float \
            and type(Latin[index+3]) != float and Latin[index+3] != "-":
              orth.text = Latin[index+1]+" "+Latin[index+2]+" "+Latin[index+3]
          else:
            orth.text = Latin[index+1]
        if type(LatLemma[index+1]) != float and LatLemma[index+1] != "-":
          if type(Latin[index+1]) == float or Latin[index+1] == "-":
            sense = etree.SubElement(cit, "sense", xml_id=Slavic[index+1].strip(",")+".1")
            cit = etree.SubElement(sense, "cit", type="translationEquivalent", xml_lang = "lat")
          form = etree.SubElement(cit, "form", type="lemma", xml_id=LatLemma[index+1])
          orth = etree.SubElement(form, "orth")
          if type(Slavic[index+2]) == float and type(LatLemma[index+2]) != float and LatLemma[index+2] != "-": 
            orth.text = LatLemma[index+1]+" "+LatLemma[index+2]
            if type(Slavic[index+3]) == float \
            and type(LatLemma[index+3]) != float and LatLemma[index+3] != "-":
              orth.text = LatLemma[index+1]+" "+LatLemma[index+2]+" "+LatLemma[index+3]
          else:
            orth.text = LatLemma[index+1]
      index+= 1


  def _semantischer_kommentar(self, row):
    index = self._index
    if type(row["GLemma"]) == float and type(self.slovar["SÜbersetzung"][index-1]) != float:
      index-= 1
      while type(self.slovar["GLemma"][index-1]) == float and type(self.slovar["SÜbersetzung"][index]) != float:
        row["GLemma"] = self.slovar["GLemma"][index-1]
        index-= 1
      row["GLemma"] = self.slovar["GLemma"][index-1]
    note_in__entry = re.search("(\[.*\])", row["SemantK"])
    cross_reference_mention = re.search("^(тожде єже|тожде|таже)\s(.*)", row["SemantK"])
    sense_note = etree.SubElement(self._entry, "sense", xml_id=row["GLemma"]+".1")
    note = etree.SubElement(sense_note, "note")
    if row["SemantK"] == "тожде":
      xr = etree.SubElement(note, "xr", type="synonymy")
      while type(self.slovar["GLemma"][index-1]) == float:
        index-= 1
      ref = etree.SubElement(xr, "ref", type="entry", target="#"+self.slovar["GLemma"][index-1])
      ref.text = row["SemantK"]
    if cross_reference_mention:
      xr = etree.SubElement(note, "xr", type="synonymy")
      lbl = etree.SubElement(xr, "lbl")
      lbl.text = cross_reference_mention.group(1)
      ref = etree.SubElement(xr, "ref", type="entry", target="#"+cross_reference_mention.group(2))
      ref.text = cross_reference_mention.group(2)
    if not row["SemantK"] == "тожде" and not cross_reference_mention:
      note.text = row["SemantK"]
    if note_in__entry:
      note_editorial = etree.SubElement(note, "note", type="editor")
      note_editorial.text = note_in__entry.group(1)





class Epifanii_visual(Epifanii_dict):

  def analyze(self):
    self.slovar.columns = ["Griechisch", "GLemma", "GMSA", "Slavisch", "SÜbersetzung", "SemantK", "Lateinisch", "LLemma", "LGram"]
    self.df = pd.DataFrame({'parts_of_speech': ['сущ.', 'глагол', 'прил.', 'null'], 'entry_cnt': [0, 0, 0, 0],  'translat_cnt': [0, 0, 0, 0]})
    slovar = self.slovar
    for index, row in slovar.iterrows():
      if index == 0:
        continue
      else:
        if type(row["GLemma"]) != float:
          if type(row["GMSA"]) != float: 
            noun = re.search("(ὁ|ἡ|τὸ)", row["GMSA"])
            nouns = re.search("(οἱ|αἱ|τὰ)", row["GMSA"])
            verb = re.search(r"((\\?μ),?\s(?P<aorist>.*?))?\s(.?(π),?\s(?P<perfect>.*))?", row["GMSA"])
            adj = re.search("((.*?),\s?)?(.?ὁ καὶ ἡ.?)", row["GMSA"])
            just_noun = re.search("(.*?),\s(ὁ|ἡ|τὸ)", row["GMSA"])
            genitive_noun = re.search("(?P<first>.*?)\s(καὶ)\s(?P<second>.*?),\s?(?P<gen>ὁ|ἡ|τὸ)", row["GMSA"])
            if type(row["GMSA"]) != float and  type(slovar["GLemma"][index]) != float: 
              if adj:
                self.df.loc[2, "entry_cnt"] += 1
                part_speech = 2
              elif noun:
                self.df.loc[0, "entry_cnt"] += 1
                part_speech = 0
              elif nouns:
                self.df.loc[0, "entry_cnt"] += 1
                part_speech = 0
              elif row["GMSA"] == "ῶ" and type(slovar["GMSA"][index+1]) != float and type(slovar["GLemma"][index+1]) == float:
                if type(slovar["GMSA"][index+2]) != float and type(slovar["GLemma"][index+2]) == float:
                  self.df.loc[1, "entry_cnt"] += 1
                  part_speech = 1
              elif verb:
                if type(slovar["GMSA"][index+1]) != float and type(slovar["GLemma"][index+1]) == float:
                  self.df.loc[1, "entry_cnt"] += 1
                  part_speech = 1
          if type(row["GMSA"]) == float and  type(row["GLemma"]) != float: 
              self.df.loc[3, "entry_cnt"] += 1
              part_speech = 3
          if type(row["SÜbersetzung"]) != float:
            while type(slovar["GLemma"][index+1]) == float:
                if type(slovar["SÜbersetzung"][index+1]) != float:
                  self.df.loc[part_speech, "translat_cnt"] += 1
                index+= 1
    self.df['true avg'] = self.df["translat_cnt"]/self.df['entry_cnt']

  def visualize(self):
    fig = plt.figure(figsize=(15,5))
    fig.add_axes([0, 0, 1, 1])
    color=['#990202', '#bf8300', '#5f8004', '#005bab']

    ax1 = plt.subplot(1,2,1)
    x=self.df['parts_of_speech'].values
    y=self.df['entry_cnt'].values
    plt.title('Количество вхождений по частям речи')
    ax1.bar(x,y, color=color)

    ax2 = plt.subplot(1,2,2)
    plt.title("Среднее число русских аналогов")
    ax2.pie(self.df['true avg'].values, explode = (0, 0.1, 0, 0), labels=self.df['parts_of_speech'].values, colors=color, 
            autopct='%1.1f%%', startangle=90)
    ax2.axis('equal');
    plt.savefig("Epifanii_visual")


