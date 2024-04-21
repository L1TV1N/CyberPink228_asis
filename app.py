from flask import Flask, render_template, request, jsonify
import json
import g4f

app = Flask(__name__)

with open('for detect.txt', 'r', encoding="utf-8") as for_detect0:
    for_detect = [list(map(str, row.split())) for row in for_detect0.readlines()]


with open('for otvet.txt', 'r', encoding="utf-8") as for_otvet0:
    for_otvet = [list(map(str, row.split())) for row in for_otvet0.readlines()]



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.get_json()
    user_message = data['message']

    check = 0
    for i in range(len(for_detect)):
        for j in range(len(for_detect[i])):
            print(for_detect[i][j])
            if for_detect[i][j] in user_message.lower():
                bot_response0 = for_otvet[i]
                bot_response = str(*bot_response0)
                bot_response = bot_response.replace('*', ' ')
                check += 1
                break

            if check == 0:
                user_input = user_message
                # подгружаем первую часть промта
                f_prom0 = open('promt0.txt', encoding="utf-8")
                f_prom0 = f_prom0.read()
                itog = f_prom0 + user_input
                # настройки для GPT
                response = g4f.ChatCompletion.create(model=g4f.models.gpt_4, provider=g4f.Provider.You,
                                                     messages=[{"role": "user", "content": itog}])
                print(response)
                bot_response = response
                check += 1
                break



    # Сохранить сообщения в JSON файле
    save_message(user_message, bot_response)

    return jsonify({'bot_message': bot_response})

def save_message(user_message, bot_message):
    message_data = {
        "user_message": user_message,
        "bot_message": bot_message
    }

    with open("messages.json", "a") as f:
        json.dump(message_data, f)
        f.write("\n")

if __name__ == '__main__':
    app.run(debug=True)
