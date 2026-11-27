from flask import Flask, request, jsonify
from flask_cors import CORS
from conexao import conectar

app = Flask(__name__)
CORS(app)  # Libera o acesso do Frontend HTML/JS


# [R] READ - Listar todos os itens cadastrados
@app.route("/ITENS", methods=["GET"])
def listar_itens():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM ITENS ORDER BY id DESC")
    lista = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(lista), 200


# [C] CREATE - Cadastrar um novo item perdido
@app.route("/ITENS", methods=["POST"])
def criar_item():
    dados = request.get_json()

    if not dados.get("titulo") or not dados.get("local_encontrado"):
        return jsonify({"erro": "Título e local são obrigatórios!"}), 400

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO ITENS (titulo, descricao, local_encontrado, data_encontro)
        VALUES (%s, %s, %s, %s)
    """
    valores = (
        dados["titulo"],
        dados.get("descricao", ""),
        dados["local_encontrado"],
        dados["data_encontro"],
    )

    cursor.execute(sql, valores)
    conn.commit()  # Confirma a gravação no banco!

    novo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"mensagem": "Item Cadastrado!", "id": novo_id}), 201


# [U] UPDATE - Registrar a devolução de um item pelo ID
@app.route("/ITENS/<int:id>/devolver", methods=["PUT"])
def devolver_item(id):
    dados = request.get_json()
    retirado_por = dados.get("retirado_por")

    if not retirado_por:
        return jsonify({"erro": "Informe o nome de quem retirou o item!"}), 400

    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE ITENS
        SET status = 'Devolvido', retirado_por = %s
        WHERE id = %s
    """
    cursor.execute(sql, (retirado_por, id))
    conn.commit()

    linhas_afetadas = cursor.rowcount
    cursor.close()
    conn.close()

    if linhas_afetadas == 0:
        return jsonify({"erro": "Item não encontrado!"}), 404

    return jsonify({"mensagem": "Devolução registrada com sucesso!"}), 200


# [D] DELETE - Excluir um registro incorreto pelo ID
@app.route("/ITENS/<int:id>", methods=["DELETE"])
def deletar_item(id):
    conn = conectar()
    cursor = conn.cursor()

    sql = "DELETE FROM ITENS WHERE id = %s"
    cursor.execute(sql, (id,))  # Atenção à vírgula na tupla de 1 elemento: (id,)
    conn.commit()

    linhas_afetadas = cursor.rowcount
    cursor.close()
    conn.close()

    if linhas_afetadas == 0:
        return jsonify({"erro": "Item não encontrado!"}), 404

    return jsonify({"mensagem": "Item removido do sistema!"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
