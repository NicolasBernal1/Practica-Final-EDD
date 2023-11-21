import json
import ast


def read_data(file_path):
    data = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                items = json.loads(line.strip())
                items[-1] = ast.literal_eval(items[-1])
                data.append(items)

    return data

rd = read_data("data.txt")

class Graph:
    def __init__(self):
        self.la = {}

    def add_vertex(self, valor):
        if(valor in self.la.keys()):
            print("Valor ya existente")
            return
        self.la[valor] = []

    def add_edge(self,v1,v2,valor=None,dirigido=True):
        if(v1 not in self.la.keys()):
            self.add_vertex(v1)
        if(v2 not in self.la.keys()):
            self.add_vertex(v2)
        
        self.la[v1].append((v2,valor))
        if(dirigido == False):
            self.la[v2].append((v1,valor))
        
Grafo = Graph()

def fill_graph(grafo:Graph,data:list):
    for element in data:
        try:
            if(element[0] not in grafo.la.keys()):
                grafo.add_vertex(element[0])
            else:
                continue

            if(element[1] not in grafo.la.keys()):
                grafo.add_vertex(element[1])
            grafo.add_edge(element[0],element[1],"Escrito por",False)

            pub = element[2].split(",")
            pub = int(pub[1])
            if(pub not in grafo.la.keys()):
                grafo.add_vertex(pub)
            grafo.add_edge(element[0],pub,"Publicado en",False)
        
            pr = float(element[3])
            if(pr not in grafo.la.keys()):
                grafo.add_vertex(pr)
            grafo.add_edge(element[0],pr,"Cuesta",False)

            ra = float(element[4])
            if(ra not in grafo.la.keys()):
                grafo.add_vertex(ra)
            grafo.add_edge(element[0],ra,"Calificado",False)

            for genre in element[5]:
                if(genre not in grafo.la.keys()):
                    grafo.add_vertex(genre)
                grafo.add_edge(element[0],genre,"Genero",False)
        except:
            continue

fill_graph(Grafo,rd)

def get_author_books():
    author = input("Autor: ")
    libros = []
    libros_temp = []
    for book in Grafo.la[author]:
        a = Grafo.la[book[0]]
        temp = (book[0],a[1][0])
        libros_temp.append(temp)
    libros_temp.sort(key=lambda x: x[1])

    for libro in libros_temp:
        libros.append(libro[0])
    
    for lib in libros:
        print(lib)

def get_books_rec_genre_decade():
    cant = int(input("Cantidad: "))
    book_ = input("Libro: ")
    libros = []
    lib_f = Grafo.la[book_][1][0]
    genre = Grafo.la[book_][4][0]
    for book in Grafo.la[genre]:
        fecha=Grafo.la[book[0]][1][0]
        if(int(str(fecha)[:2]) == int(str(lib_f)[:2]) and str(fecha)[-2] == str(lib_f)[-2]):
            if(len(libros) == cant):
                break
            if(book[0] == book_):
                continue
            libros.append(book[0])
    
    for a in libros:
        print(a)

def get_autors_by_genre():
    genero = input("Genero: ")
    autores=[]
    autores_ = []
    libs = Grafo.la[genero]
    authors={}
    for lib in libs:
        aut = Grafo.la[lib[0]][0][0]
        if aut not in authors.keys():
            authors[aut] = 1
        else:
            authors[aut] += 1
    for k in authors.keys():
        autores_.append((k,authors[k]))
    autores_.sort(key=lambda x: x[1])
    for a in autores_:
        autores.append(a[0])
    
    for a in list(reversed(autores)):
        print(a)

def rec_books_mt_rate_genres():
    rating = float(input("Puntaje mayor o igual a: "))
    if(1 <= rating <= 5):
        all_books=[]
        genres = []
        books=[]
        sw = True
        while sw:
            gen = input("Genero (Escribir No para finalizar): ")
            if(gen.lower() == "no"):
                sw = False
                continue
            genres.append(gen)
        if(len(genres) == 0):
            print("Debe haber por lo menos 1 genero")
            return
        
        for gene in genres:
            l = Grafo.la[gene]
            for i in l:
                all_books.append(i[0])
        all_books = list(set(all_books))
        for b in all_books:
            if(Grafo.la[b][3][0] >= rating):
                books.append(b)
        
        for book in books:
            print(book)
    else:
        print("La calificación debe estar entre 1 y 5")

print(Grafo.la["To Kill a Mockingbird"][2][0])

def recomendar_libros():
    presupuesto = float(input("Presupuesto: "))
    all_books=[]
    genres = []
    temp=[]
    books=[]
    sw = True
    while sw:
        gen = input("Genero (Escribir No para finalizar): ")
        if(gen.lower() == "no"):
            sw = False
            continue
        genres.append(gen)
    if(len(genres) == 0):
        print("Debe haber por lo menos 1 genero")
        return
    
    for gene in genres:
        l = Grafo.la[gene]
        for i in l:
            all_books.append(i[0])
    all_books = list(set(all_books))
    
    for b in all_books:
        temp.append((b, Grafo.la[b][2][0]))
    
    temp.sort(key=lambda x: x[1])

    cont = 0
    for b in temp:
        if(cont + b[1] > presupuesto):
            break
        books.append(b[0])
        cont += b[1]

    for book in books:
        print(book)



