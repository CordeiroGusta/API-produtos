# '''
# QUAIS ENTIDADES QUE EU TENHO NA MINHA API:
# itens:{
#     'id' => identificador único do item cadastrado,
#     'nome' => nome do item cadastrado,
#     'descricao' => descricao breve sobre o item,
#     'familia' => classificação a qual o item pertence,
#     'valor_unitario' => valor unitario do item,
#     'quantidade' => quantidade que tem desse item
# }

# QUAIS RECURSOS EU VOU DISPONIBILIZAR NESSA API:
# todo o crud dos itens cadastrados
#
# ENDPOINTS;
# - GET api/v1/items => busca geral por todos os itens
# - GET api/v1/items/{id} => busca o item pelo seu id
# - POST api/v1/items/ => Cria um novo item no armazenamento local
# - PATCH api/v1/items/{id} => atualiza o item pelo seu id
# - DELETE api/v1/items/{id} => deleta o item pelo seu id
# '''

from fastapi import FastAPI

app = FastAPI(
    title="teste"
)

@app.get("/")
def teste_api():
    return "Ola, mundo!"
