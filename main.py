from fakepinterest import app

# Coloca o site no ar
# Roda o site apenas se o arquivo main for executado, não permite rodar por meio de importação
if __name__ == "__main__":
    # debug=True: Toda alteração no código é transmitida ao site sem a necessidade de reiniciar o programa
    app.run(debug=True)
