# Neo4j Exerciții - Rețea Socială Academică

## Configurare

**Conectare la Neo4j Aura Free:**
1. Creați un cont gratuit la [console.neo4j.io](https://console.neo4j.io)
2. Creați o nouă instanță (Free tier)
3. Salvați credențialele (URI, username, password)
4. Instalați driver-ul Python: `pip install neo4j`
```python
# Instalare librării necesare
!pip install neo4j pandas
```
```python
from neo4j import GraphDatabase
import pandas as pd

# Configurare conexiune - COMPLETAȚI CU DATELE VOASTRE
URI = "neo4j+s://xxxxxxxx.databases.neo4j.io"  # Din Neo4j Aura
AUTH = ("neo4j", "password")  # Username și parola voastră

driver = GraphDatabase.driver(URI, auth=AUTH)

def run_query(query, parameters=None):
    """Funcție helper pentru rularea query-urilor"""
    with driver.session() as session:
        result = session.run(query, parameters or {})
        return [record.data() for record in result]

# Test conexiune
try:
    driver.verify_connectivity()
    print("✓ Conectare reușită la Neo4j!")
except Exception as e:
    print(f"✗ Eroare la conectare: {e}")
```

## Partea 1: Creare și Populare Bază de Date

### Schema bazei de date:
- **Noduri**: Student, Profesor, Curs, Proiect, Companie
- **Relații**: ENROLLED_IN, TEACHES, COLLABORATES_WITH, WORKS_ON, MENTORED_BY, INTERNED_AT

## 📊 Schema Bazei de Date

### Noduri (Node Types)

| Label | Proprietăți | Descriere |
|-------|-------------|-----------|
| **Student** | id, nume, an, facultate, medie, email | Studenți din facultate |
| **Profesor** | id, nume, departament, grad, experienta | Cadre didactice |
| **Curs** | cod, nume, credite, semestru, nivel | Cursuri disponibile |
| **Proiect** | id, nume, descriere, status, deadline | Proiecte de cercetare |
| **Companie** | id, nume, domeniu, locatie | Companii pentru internship |

### Relații (Relationships)

| Tip | De la → La | Proprietăți | Descriere |
|-----|-----------|-------------|-----------|
| **ENROLLED_IN** | Student → Curs | nota, an_inscris | Înscriere la curs |
| **TEACHES** | Profesor → Curs | din_an | Predare curs |
| **WORKS_ON** | Student → Proiect | rol, ore_saptamana | Lucru la proiect |
| **COLLABORATES_WITH** | Student → Student | din_data, proiecte_comune | Colaborare |
| **MENTORED_BY** | Student → Profesor | din_data, tip | Mentorat |
| **INTERNED_AT** | Student → Companie | perioada, pozitie | Internship |

```python
# Ștergere date existente (ATENȚIE: șterge tot!)
clear_query = "MATCH (n) DETACH DELETE n"
run_query(clear_query)
print("Baza de date curățată!")
```
```python
# Creare constrângeri și indexuri pentru performanță
constraints = [
    "CREATE CONSTRAINT student_id IF NOT EXISTS FOR (s:Student) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT profesor_id IF NOT EXISTS FOR (p:Profesor) REQUIRE p.id IS UNIQUE",
    "CREATE CONSTRAINT curs_cod IF NOT EXISTS FOR (c:Curs) REQUIRE c.cod IS UNIQUE",
    "CREATE CONSTRAINT proiect_id IF NOT EXISTS FOR (pr:Proiect) REQUIRE pr.id IS UNIQUE",
    "CREATE INDEX student_nume IF NOT EXISTS FOR (s:Student) ON (s.nume)",
]

for constraint in constraints:
    try:
        run_query(constraint)
    except Exception as e:
        print(f"Constrângere deja existentă sau eroare: {e}")

print("✓ Constrângeri și indexuri create!")
```
```python
# Populare bază de date - STUDENȚI
create_students = """
CREATE 
  (s1:Student {id: 'S001', nume: 'Popescu Ion', an: 3, facultate: 'Informatică', medie: 9.2, email: 'ion.popescu@student.ro'}),
  (s2:Student {id: 'S002', nume: 'Ionescu Maria', an: 2, facultate: 'Informatică', medie: 8.7, email: 'maria.ionescu@student.ro'}),
  (s3:Student {id: 'S003', nume: 'Georgescu Andrei', an: 3, facultate: 'Informatică', medie: 9.5, email: 'andrei.georgescu@student.ro'}),
  (s4:Student {id: 'S004', nume: 'Popa Elena', an: 1, facultate: 'Informatică', medie: 8.3, email: 'elena.popa@student.ro'}),
  (s5:Student {id: 'S005', nume: 'Marin Alexandru', an: 2, facultate: 'Informatică', medie: 7.9, email: 'alex.marin@student.ro'}),
  (s6:Student {id: 'S006', nume: 'Stan Diana', an: 3, facultate: 'Informatică', medie: 9.0, email: 'diana.stan@student.ro'}),
  (s7:Student {id: 'S007', nume: 'Dumitrescu Vlad', an: 1, facultate: 'Informatică', medie: 8.5, email: 'vlad.dumitrescu@student.ro'}),
  (s8:Student {id: 'S008', nume: 'Constantinescu Ana', an: 2, facultate: 'Matematică', medie: 9.3, email: 'ana.constantinescu@student.ro'})
"""
run_query(create_students)
print("✓ Studenți creați!")
```
```python
# Populare bază de date - PROFESORI
create_professors = """
CREATE 
  (p1:Profesor {id: 'P001', nume: 'Dr. Vasilescu Mihai', departament: 'Informatică', grad: 'Profesor', experienta: 15}),
  (p2:Profesor {id: 'P002', nume: 'Dr. Cristescu Laura', departament: 'Informatică', grad: 'Conferențiar', experienta: 10}),
  (p3:Profesor {id: 'P003', nume: 'Dr. Radu Stefan', departament: 'Matematică', grad: 'Lector', experienta: 5}),
  (p4:Profesor {id: 'P004', nume: 'Dr. Nicolescu Anca', departament: 'Informatică', grad: 'Profesor', experienta: 20})
"""
run_query(create_professors)
print("✓ Profesori creați!")
```
```python
# Populare bază de date - CURSURI
create_courses = """
CREATE 
  (c1:Curs {cod: 'CS101', nume: 'Structuri de Date', credite: 6, semestru: 1, nivel: 'intermediar'}),
  (c2:Curs {cod: 'CS201', nume: 'Baze de Date', credite: 5, semestru: 2, nivel: 'intermediar'}),
  (c3:Curs {cod: 'CS301', nume: 'Inteligență Artificială', credite: 6, semestru: 1, nivel: 'avansat'}),
  (c4:Curs {cod: 'CS102', nume: 'Algoritmi', credite: 7, semestru: 2, nivel: 'intermediar'}),
  (c5:Curs {cod: 'CS401', nume: 'Machine Learning', credite: 6, semestru: 1, nivel: 'avansat'}),
  (c6:Curs {cod: 'MATH201', nume: 'Algebră Liniară', credite: 5, semestru: 2, nivel: 'fundamental'})
"""
run_query(create_courses)
print("✓ Cursuri create!")
```
```python
# Populare bază de date - PROIECTE
create_projects = """
CREATE 
  (pr1:Proiect {id: 'PRJ001', nume: 'Sistem Recomandare Filme', descriere: 'Algoritm ML pentru recomandări', status: 'în desfășurare', deadline: date('2024-12-15')}),
  (pr2:Proiect {id: 'PRJ002', nume: 'Chatbot Educațional', descriere: 'Bot pentru asistență studenți', status: 'finalizat', deadline: date('2024-06-30')}),
  (pr3:Proiect {id: 'PRJ003', nume: 'Analiză Rețele Sociale', descriere: 'Vizualizare grafuri sociale', status: 'în desfășurare', deadline: date('2024-11-20')}),
  (pr4:Proiect {id: 'PRJ004', nume: 'Aplicație Mobile Sănătate', descriere: 'Tracking fitness și nutriție', status: 'planificat', deadline: date('2025-03-01')})
"""
run_query(create_projects)
print("✓ Proiecte create!")
```
```python
# Populare bază de date - COMPANII
create_companies = """
CREATE 
  (comp1:Companie {id: 'C001', nume: 'TechCorp', domeniu: 'Software Development', locatie: 'București'}),
  (comp2:Companie {id: 'C002', nume: 'DataSolutions', domeniu: 'Data Analytics', locatie: 'Cluj-Napoca'}),
  (comp3:Companie {id: 'C003', nume: 'AI Innovations', domeniu: 'Artificial Intelligence', locatie: 'București'})
"""
run_query(create_companies)
print("✓ Companii create!")
```
```python
# Creare RELAȚII - ENROLLED_IN (studenți înscriși la cursuri)
create_enrollments = """
MATCH (s1:Student {id: 'S001'}), (c1:Curs {cod: 'CS101'})
CREATE (s1)-[:ENROLLED_IN {nota: 9.5, an_inscris: 2023}]->(c1)

WITH 1 as dummy
MATCH (s1:Student {id: 'S001'}), (c2:Curs {cod: 'CS201'})
CREATE (s1)-[:ENROLLED_IN {nota: 9.0, an_inscris: 2024}]->(c2)

WITH 1 as dummy
MATCH (s2:Student {id: 'S002'}), (c1:Curs {cod: 'CS101'})
CREATE (s2)-[:ENROLLED_IN {nota: 8.5, an_inscris: 2024}]->(c1)

WITH 1 as dummy
MATCH (s2:Student {id: 'S002'}), (c4:Curs {cod: 'CS102'})
CREATE (s2)-[:ENROLLED_IN {nota: 8.8, an_inscris: 2024}]->(c4)

WITH 1 as dummy
MATCH (s3:Student {id: 'S003'}), (c3:Curs {cod: 'CS301'})
CREATE (s3)-[:ENROLLED_IN {nota: 10.0, an_inscris: 2024}]->(c3)

WITH 1 as dummy
MATCH (s3:Student {id: 'S003'}), (c5:Curs {cod: 'CS401'})
CREATE (s3)-[:ENROLLED_IN {nota: 9.7, an_inscris: 2024}]->(c5)

WITH 1 as dummy
MATCH (s4:Student {id: 'S004'}), (c1:Curs {cod: 'CS101'})
CREATE (s4)-[:ENROLLED_IN {nota: 8.0, an_inscris: 2024}]->(c1)

WITH 1 as dummy
MATCH (s5:Student {id: 'S005'}), (c2:Curs {cod: 'CS201'})
CREATE (s5)-[:ENROLLED_IN {nota: 7.5, an_inscris: 2024}]->(c2)

WITH 1 as dummy
MATCH (s6:Student {id: 'S006'}), (c3:Curs {cod: 'CS301'})
CREATE (s6)-[:ENROLLED_IN {nota: 9.2, an_inscris: 2024}]->(c3)

WITH 1 as dummy
MATCH (s8:Student {id: 'S008'}), (c6:Curs {cod: 'MATH201'})
CREATE (s8)-[:ENROLLED_IN {nota: 9.5, an_inscris: 2024}]->(c6)
"""
run_query(create_enrollments)
print("✓ Înscrieri create!")
```
```python
# Creare RELAȚII - TEACHES (profesori predau cursuri)
create_teaches = """
MATCH (p1:Profesor {id: 'P001'}), (c1:Curs {cod: 'CS101'})
CREATE (p1)-[:TEACHES {din_an: 2020}]->(c1)

WITH 1 as dummy
MATCH (p1:Profesor {id: 'P001'}), (c4:Curs {cod: 'CS102'})
CREATE (p1)-[:TEACHES {din_an: 2018}]->(c4)

WITH 1 as dummy
MATCH (p2:Profesor {id: 'P002'}), (c2:Curs {cod: 'CS201'})
CREATE (p2)-[:TEACHES {din_an: 2019}]->(c2)

WITH 1 as dummy
MATCH (p4:Profesor {id: 'P004'}), (c3:Curs {cod: 'CS301'})
CREATE (p4)-[:TEACHES {din_an: 2015}]->(c3)

WITH 1 as dummy
MATCH (p4:Profesor {id: 'P004'}), (c5:Curs {cod: 'CS401'})
CREATE (p4)-[:TEACHES {din_an: 2017}]->(c5)

WITH 1 as dummy
MATCH (p3:Profesor {id: 'P003'}), (c6:Curs {cod: 'MATH201'})
CREATE (p3)-[:TEACHES {din_an: 2021}]->(c6)
"""
run_query(create_teaches)
print("✓ Relații TEACHES create!")
```
```python
# Creare RELAȚII - WORKS_ON (studenți lucrează la proiecte)
create_works_on = """
MATCH (s1:Student {id: 'S001'}), (pr1:Proiect {id: 'PRJ001'})
CREATE (s1)-[:WORKS_ON {rol: 'Lead Developer', ore_saptamana: 15}]->(pr1)

WITH 1 as dummy
MATCH (s2:Student {id: 'S002'}), (pr1:Proiect {id: 'PRJ001'})
CREATE (s2)-[:WORKS_ON {rol: 'Data Scientist', ore_saptamana: 10}]->(pr1)

WITH 1 as dummy
MATCH (s3:Student {id: 'S003'}), (pr2:Proiect {id: 'PRJ002'})
CREATE (s3)-[:WORKS_ON {rol: 'AI Engineer', ore_saptamana: 12}]->(pr2)

WITH 1 as dummy
MATCH (s6:Student {id: 'S006'}), (pr3:Proiect {id: 'PRJ003'})
CREATE (s6)-[:WORKS_ON {rol: 'Researcher', ore_saptamana: 8}]->(pr3)

WITH 1 as dummy
MATCH (s3:Student {id: 'S003'}), (pr3:Proiect {id: 'PRJ003'})
CREATE (s3)-[:WORKS_ON {rol: 'Lead Analyst', ore_saptamana: 10}]->(pr3)
"""
run_query(create_works_on)
print("✓ Relații WORKS_ON create!")
```
```python
# Creare RELAȚII - COLLABORATES_WITH (studenți colaborează)
create_collaborations = """
MATCH (s1:Student {id: 'S001'}), (s2:Student {id: 'S002'})
CREATE (s1)-[:COLLABORATES_WITH {din_data: date('2024-01-15'), proiecte_comune: 1}]->(s2)

WITH 1 as dummy
MATCH (s3:Student {id: 'S003'}), (s6:Student {id: 'S006'})
CREATE (s3)-[:COLLABORATES_WITH {din_data: date('2024-02-10'), proiecte_comune: 1}]->(s6)

WITH 1 as dummy
MATCH (s1:Student {id: 'S001'}), (s3:Student {id: 'S003'})
CREATE (s1)-[:COLLABORATES_WITH {din_data: date('2023-09-01'), proiecte_comune: 2}]->(s3)
"""
run_query(create_collaborations)
print("✓ Relații COLLABORATES_WITH create!")
```
```python
# Creare RELAȚII - MENTORED_BY (studenți au mentori profesori)
create_mentoring = """
MATCH (s1:Student {id: 'S001'}), (p1:Profesor {id: 'P001'})
CREATE (s1)-[:MENTORED_BY {din_data: date('2023-10-01'), tip: 'Cercetare'}]->(p1)

WITH 1 as dummy
MATCH (s3:Student {id: 'S003'}), (p4:Profesor {id: 'P004'})
CREATE (s3)-[:MENTORED_BY {din_data: date('2023-09-15'), tip: 'Doctorat'}]->(p4)

WITH 1 as dummy
MATCH (s6:Student {id: 'S006'}), (p4:Profesor {id: 'P004'})
CREATE (s6)-[:MENTORED_BY {din_data: date('2024-02-01'), tip: 'Licență'}]->(p4)
"""
run_query(create_mentoring)
print("✓ Relații MENTORED_BY create!")
```
```python
# Creare RELAȚII - INTERNED_AT (studenți au făcut internship)
create_internships = """
MATCH (s1:Student {id: 'S001'}), (comp1:Companie {id: 'C001'})
CREATE (s1)-[:INTERNED_AT {perioada: '2023-07 - 2023-09', pozitie: 'Software Developer Intern'}]->(comp1)

WITH 1 as dummy
MATCH (s3:Student {id: 'S003'}), (comp3:Companie {id: 'C003'})
CREATE (s3)-[:INTERNED_AT {perioada: '2024-06 - 2024-08', pozitie: 'ML Engineer Intern'}]->(comp3)

WITH 1 as dummy
MATCH (s2:Student {id: 'S002'}), (comp2:Companie {id: 'C002'})
CREATE (s2)-[:INTERNED_AT {perioada: '2024-07 - prezent', pozitie: 'Data Analyst Intern'}]->(comp2)
"""
run_query(create_internships)
print("✓ Relații INTERNED_AT create!")
print("\n🎉 Baza de date complet populată!")
```

## Partea 2: Exerciții Rezolvate

### Exercițiul 1: Interogări Simple (READ)
```python
# 1.1. Afișați toți studenții din anul 3
query = """
MATCH (s:Student)
WHERE s.an = 3
RETURN s.nume AS Nume, s.medie AS Medie, s.facultate AS Facultate
ORDER BY s.medie DESC
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Studenți anul 3:")
print(df)
```
```python
# 1.2. Găsiți toate cursurile de nivel avansat
query = """
MATCH (c:Curs)
WHERE c.nivel = 'avansat'
RETURN c.cod AS Cod, c.nume AS Nume, c.credite AS Credite
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Cursuri avansate:")
print(df)
```

### Exercițiul 2: Relații și Pattern Matching
```python
# 2.1. Afișați studenții și cursurile la care sunt înscriși
query = """
MATCH (s:Student)-[r:ENROLLED_IN]->(c:Curs)
RETURN s.nume AS Student, c.nume AS Curs, r.nota AS Nota
ORDER BY r.nota DESC
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Studenți și cursuri:")
print(df.head(10))
```
```python
# 2.2. Găsiți studenții care colaborează între ei
query = """
MATCH (s1:Student)-[c:COLLABORATES_WITH]->(s2:Student)
RETURN s1.nume AS Student1, s2.nume AS Student2, 
       c.proiecte_comune AS ProiecteComune, c.din_data AS DinData
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Colaborări între studenți:")
print(df)
```

### Exercițiul 3: Agregări și Funcții
```python
# 3.1. Numărul de studenți înscriși la fiecare curs
query = """
MATCH (s:Student)-[:ENROLLED_IN]->(c:Curs)
RETURN c.nume AS Curs, c.cod AS Cod, count(s) AS NumarStudenti
ORDER BY NumarStudenti DESC
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Număr studenți pe curs:")
print(df)
```
```python
# 3.2. Media notelor pentru fiecare student
query = """
MATCH (s:Student)-[e:ENROLLED_IN]->(c:Curs)
RETURN s.nume AS Student, 
       round(avg(e.nota) * 100) / 100 AS MediaNote,
       count(c) AS NumarCursuri
ORDER BY MediaNote DESC
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Media studenților:")
print(df)
```
```python
# 3.3. Profesori și numărul de cursuri predate
query = """
MATCH (p:Profesor)-[:TEACHES]->(c:Curs)
RETURN p.nume AS Profesor, p.grad AS Grad,
       count(c) AS NumarCursuri,
       collect(c.nume) AS Cursuri
ORDER BY NumarCursuri DESC
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Profesori și cursuri:")
print(df)
```

### Exercițiul 4: Path Queries (Căi în Graf)
```python
# 4.1. Găsiți profesorii care predau cursuri la care sunt înscriși studenți din anul 3
query = """
MATCH (s:Student)-[:ENROLLED_IN]->(c:Curs)<-[:TEACHES]-(p:Profesor)
WHERE s.an = 3
RETURN DISTINCT p.nume AS Profesor, c.nume AS Curs, 
       collect(DISTINCT s.nume) AS Studenti
ORDER BY Profesor
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Profesori cu studenți din anul 3:")
print(df)
```
```python
# 4.2. Studenți care lucrează împreună la proiecte
query = """
MATCH (s1:Student)-[:WORKS_ON]->(p:Proiect)<-[:WORKS_ON]-(s2:Student)
WHERE id(s1) < id(s2)
RETURN s1.nume AS Student1, s2.nume AS Student2, 
       p.nume AS Proiect, p.status AS Status
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Colegi de proiect:")
print(df)
```
```python
# 4.3. Studenți care au același mentor
query = """
MATCH (s1:Student)-[:MENTORED_BY]->(p:Profesor)<-[:MENTORED_BY]-(s2:Student)
WHERE id(s1) < id(s2)
RETURN p.nume AS Mentor, 
       collect(s1.nume + ', ' + s2.nume) AS GrupStudenti
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Studenți cu același mentor:")
print(df)
```

### Exercițiul 5: Queries Complexe și Recomandări
```python
# 5.1. Recomandare cursuri pentru studenți (bazat pe ce au urmat colegii lor)
query = """
MATCH (s:Student {nume: 'Popescu Ion'})-[:ENROLLED_IN]->(c1:Curs)
MATCH (c1)<-[:ENROLLED_IN]-(altStudent:Student)-[:ENROLLED_IN]->(c2:Curs)
WHERE NOT (s)-[:ENROLLED_IN]->(c2)
RETURN DISTINCT c2.nume AS CursRecomandat, c2.cod AS Cod,
       count(DISTINCT altStudent) AS NumarColegi,
       collect(DISTINCT altStudent.nume)[0..3] AS ExempluColegi
ORDER BY NumarColegi DESC
LIMIT 5
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Cursuri recomandate pentru Popescu Ion:")
print(df)
```
```python
# 5.2. Top studenți cu cele mai multe conexiuni (colaborări + proiecte)
query = """
MATCH (s:Student)
OPTIONAL MATCH (s)-[:COLLABORATES_WITH]-(colab:Student)
OPTIONAL MATCH (s)-[:WORKS_ON]->(p:Proiect)
RETURN s.nume AS Student, s.medie AS Medie,
       count(DISTINCT colab) AS NumarColaborari,
       count(DISTINCT p) AS NumarProiecte,
       (count(DISTINCT colab) + count(DISTINCT p)) AS ScorConexiuni
ORDER BY ScorConexiuni DESC
LIMIT 5
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Top studenți după conexiuni:")
print(df)
```
```python
# 5.3. Găsiți shortest path între doi studenți
query = """
MATCH path = shortestPath(
  (s1:Student {nume: 'Popescu Ion'})-[*]-(s2:Student {nume: 'Stan Diana'})
)
RETURN [node in nodes(path) | 
        CASE 
          WHEN 'Student' IN labels(node) THEN node.nume
          WHEN 'Curs' IN labels(node) THEN node.nume
          WHEN 'Proiect' IN labels(node) THEN node.nume
          ELSE 'Unknown'
        END
       ] AS CaleaIntre,
       length(path) AS Lungime
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Cea mai scurtă cale între Popescu Ion și Stan Diana:")
print(df)
```

### Exercițiul 6: CREATE, UPDATE, DELETE
```python
# 6.1. Adăugați un student nou
query = """
CREATE (s:Student {
  id: 'S009', 
  nume: 'Marinescu Cristian', 
  an: 1, 
  facultate: 'Informatică', 
  medie: 8.8,
  email: 'cristian.marinescu@student.ro'
})
RETURN s.nume AS StudentAdaugat, s.id AS ID
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Student adăugat:")
print(df)
```
```python
# 6.2. Înscrieți studentul nou la un curs
query = """
MATCH (s:Student {id: 'S009'}), (c:Curs {cod: 'CS101'})
CREATE (s)-[r:ENROLLED_IN {nota: null, an_inscris: 2024}]->(c)
RETURN s.nume AS Student, c.nume AS Curs
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Înscriere creată:")
print(df)
```
```python
# 6.3. Actualizați nota unui student
query = """
MATCH (s:Student {id: 'S009'})-[r:ENROLLED_IN]->(c:Curs {cod: 'CS101'})
SET r.nota = 9.0
RETURN s.nume AS Student, c.nume AS Curs, r.nota AS NotaNoua
"""
result = run_query(query)
df = pd.DataFrame(result)
print("Notă actualizată:")
print(df)
```
```python
# 6.4. Ștergeți studentul creat (pentru curățare)
query = """
MATCH (s:Student {id: 'S009'})
DETACH DELETE s
RETURN 'Student șters' AS Rezultat
"""
result = run_query(query)
print("Ștergere completă!")
```

---

## Partea 3: Exerciții Propuse (rezolvati 7 la alegere)

### Nivel Beginner

**Exercițiul P1:** Afișați toți profesorii din departamentul de Informatică, ordonați alfabetic.

**Exercițiul P2:** Găsiți toate proiectele cu status 'în desfășurare'.

**Exercițiul P3:** Afișați studenții cu media peste 9.0.

**Exercițiul P4:** Listați toate cursurile care au mai mult de 5 credite.

### Nivel Intermediate

**Exercițiul P5:** Pentru fiecare proiect, afișați studenții care lucrează la el și rolul lor.

**Exercițiul P6:** Găsiți studenții care au note peste 9.0 la toate cursurile la care sunt înscriși.

**Exercițiul P7:** Calculați numărul total de ore pe săptămână pe care le dedică fiecare student proiectelor.

**Exercițiul P8:** Găsiți cursurile care nu au niciun student înscris.

**Exercițiul P9:** Afișați pentru fiecare profesor lista de studenți pe care îi mentorează.

### Nivel Advanced

**Exercițiul P10:** Creați un query care să recomande colaboratori potențiali pentru un student (studenți care sunt înscriși la aceleași cursuri dar nu colaborează încă).

**Exercițiul P11:** Găsiți „influencerii" din rețea - studenții cu cel mai mare număr de conexiuni directe și indirecte (grad 2).

**Exercițiul P12:** Identificați „community clusters" - grupuri de studenți care sunt strâns conectați între ei prin colaborări și proiecte comune.

**Exercițiul P13:** Creați un sistem de recomandare pentru internship-uri: pentru fiecare student fără internship, recomandați companii bazat pe: cursurile urmate, proiectele la care lucrează, și unde au făcut internship colegii lor.

**Exercițiul P14:** Calculați „centralitatea" fiecărui student în rețea folosind numărul de shortest paths care trec prin el (betweenness centrality simplificat).

**Exercițiul P15:** Găsiți toate ciclurile de colaborare (ex: A colaborează cu B, C cu A).

### Exerciții de Modificare a Datelor

**Exercițiul P16:** Adăugați un curs nou „Web Development" (CS501) cu 6 credite, nivel intermediar.

**Exercițiul P17:** Înscrieți 3 studenți la acest curs nou.

**Exercițiul P18:** Creați un proiect nou și adăugați 2 studenți să lucreze la el.

**Exercițiul P19:** Actualizați mediile tuturor studenților care au note peste 9.5 la cursurile de nivel avansat (adăugați 0.1 la medie).

**Exercițiul P20:** Ștergeți toate relațiile ENROLLED_IN unde nota este sub 7.0.

### Exerciții Bonus - Analiză Avansată

**Exercițiul B.1:** Creați o vizualizare a rețelei de colaborare (exportați datele într-un format care poate fi vizualizat).

**Exercițiul B.2:** Implementați un algoritm de PageRank simplificat pentru a identifica cei mai „importanți" studenți din rețea.

**Exercițiul B.3:** Analizați „asortativitatea" rețelei - studenții tind să colaboreze cu colegi cu medii similare?

---

## Curățare și Închidere Conexiune

```python
# Ștergeți cursul test creat
cleanup = """
MATCH (c:Curs {cod: 'CS501'})
DETACH DELETE c
"""
try:
    run_query(cleanup)
    print("Curățare completă!")
except:
    print("Nimic de curățat")
```

```python
# Închideți conexiunea
driver.close()
print("Conexiune închisă!")
```

---

## Resurse Suplimentare

### Documentație Neo4j:
- [Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [Python Driver](https://neo4j.com/docs/python-manual/current/)
- [Graph Data Science](https://neo4j.com/docs/graph-data-science/current/)

### Practică:
- [Neo4j Sandbox](https://sandbox.neo4j.com/) - Baze de date demo
- [GraphAcademy](https://graphacademy.neo4j.com/) - Cursuri gratuite

### Sfaturi:
1. Începeți cu queries simple și construiți treptat complexitate
2. Folosiți `EXPLAIN` și `PROFILE` pentru a înțelege performanța
3. Desenați schema grafului înainte de a scrie queries complexe
4. Testați fiecare parte a query-ului separat
5. Folosiți Neo4j Browser pentru vizualizare interactivă