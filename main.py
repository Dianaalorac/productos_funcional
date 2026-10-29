from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Producto(BaseModel):
    nombre : str = Field(min_length=5)
    precio : float = Field(ge= 0, lt= 51000) #greater or equal(que sea mayor que cero) y con uns restriccion (less than) de precio)
    stock : int = Field(ge = 0)

#Esto es un diccionario (lo de abajo) 
datos = {
    "nombre": "Laptop",
    "precio": 15000.0,
     "stock": 5}


#Hasta aqui datos no era un objeto de la clase producto
objeto = Producto(**datos) #(Esto es lo mismo a lo de abajo )
objeto = Producto.model_validate(datos) ##Esto es lo mismo de lo de arriba

#Ya es un producto


db = [objeto]
i = 0

@app.get("/")
def saludar():
    return{"mensaje": "Hola desde mi api"}

#mostrar database
@app.get("/db")
def mostrar():
    return{"db":db}

#Especificar con field restricciones de nuetra clase

#Como crear el producto sin tener  que hacer lo de 
@app.post("/")
def crear_producto(datos:Producto):
    nuevo_producto = {
        "id" : i
        **datos.model_dump()
    }
    db.append(nuevo_producto)
    i = i+1 
    return{"mensaje": "elemento creado"}

@app.delete("/producto/{producto_id}")
def eliminar_producto(producto_id):
    for elemento in db:
        if elemento["id"] == producto_id:
            db.remove(elemento)
        else:
            return{"warning": f"El producto  {elemento["nombre"]} no fue encontrado"}
    