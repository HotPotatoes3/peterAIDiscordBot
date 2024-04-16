import os

import google.generativeai as genai

TOKEN2 = os.environ['TOKEN2']
genai.configure(api_key=TOKEN2)

model = genai.GenerativeModel('gemini-pro')
model2 = genai.GenerativeModel('gemini-pro-vision')



def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == '?green fn':
        return 'https://tenor.com/view/green-fn-peter-griffin-green-gif-1521709978489846232'
    if p_message == '?help':
        return '**Commands:**\n\n**?askpeter {Your question/statement}:** Responds as Peter Griffin from Family Guy'
    if p_message[0:9] == "?askpeter":
        try:
            response = model.generate_content(
                'Answer the following question/statement as if you are the character Peter Griffin from the TV show "Family Guy" (try to include a cutaway gag/reference from the show in your response): ' + p_message[
                                                                                                                                                                                                              10:],
                safety_settings={'HARM_CATEGORY_HARASSMENT': 'block_none', 'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                                 'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                                 'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})

            peterResponse = response.text
            return peterResponse
        except Exception as e:
            print(e)
            return "Please ask a question properly as follows: **?askpeter {Your question/statement}:**"

# async def handle_response2(message):
#     image = 'None'
#     for i in message.attachments:
#         if i.content_type == 'image/png':
#             image = i.url
#             await i.to_file()
#             break
#     print("Handled url")
#     print(image)


def image_to_text(text, image):
    try:
        response = model2.generate_content(['React to the following image and statement as if you are the character Peter Griffin from the TV show "Family Guy" (try to include a cutaway gag/reference from the show in your response): ' + text, image], safety_settings={'HARM_CATEGORY_HARASSMENT': 'block_none', 'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                                 'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                                 'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})

        peterResponse = response.text
        return peterResponse
    except Exception as e:
        print(e)
        return "An error occured"




def slash_response(type, input):
    if type == 'askpeter':
        response = model.generate_content(
                        'Answer the following question/statement as if you are the character Peter Griffin from the TV show "Family Guy" (try to include a cutaway gag/reference from the show in your response): ' + input,
                        safety_settings={'HARM_CATEGORY_HARASSMENT': 'block_none', 'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                                         'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                                         'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})

        peterResponse = response.text
        return peterResponse
    elif type == 'help':
        return '**Commands:**\n\n**?askpeter {Your question/statement}:** Responds as Peter Griffin from Family Guy'

