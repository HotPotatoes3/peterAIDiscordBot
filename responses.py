import os

import google.generativeai as genai

import requests
import json


TOKEN2 = os.environ['TOKEN2']
genai.configure(api_key=TOKEN2)

model = genai.GenerativeModel('gemini-pro')
model2 = genai.GenerativeModel('gemini-pro-vision')





# def handle_response(message) -> str:
#     p_message = message.lower()
#
#     if p_message == '?help':
#         return '**Commands:**\n\n**?askpeter {Your question/statement}:** Responds as Peter Griffin from Family Guy\n**?askpeter+ {Your question/statement along with an image attatchment}: Peter responds to the statement along with the image**'
#     if p_message[0:9] == "?askpeter":
#         try:
#             response = model.generate_content(
#                 'Answer the following question/statement as if you are the character Peter Griffin from the TV show "Family Guy" in less than 2000 characters(try to include a cutaway gag/reference from the show in your response, and keep your response under 2000 characters): ' + p_message[
#                                                                                                                                                                                                               10:],
#                 safety_settings={'HARM_CATEGORY_HARASSMENT': 'block_none', 'HARM_CATEGORY_HATE_SPEECH': 'block_none',
#                                  'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
#                                  'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})
#
#             peterResponse = response.text
#             return peterResponse
#         except Exception as e:
#             print(e)
#             return "Please ask a question properly as follows: **?askpeter {Your question/statement}:**"






# def image_to_text(text, image):
#     try:
#         response = model2.generate_content(['React to the following image and statement as if you are the character Peter Griffin from the TV show "Family Guy" in less than 2000 characters (try to include a cutaway gag/reference from the show in your response): ' + text, image], safety_settings={'HARM_CATEGORY_HARASSMENT': 'block_none', 'HARM_CATEGORY_HATE_SPEECH': 'block_none',
#                                  'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
#                                  'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})
#
#         peterResponse = response.text
#         return peterResponse
#     except Exception as e:
#         print(e)
#         return "An error occured"


def ai_response(type, input, image):
    if type == 'askpeter':
        try:
            while True:
                response = model.generate_content(
                                'Answer the following question/statement as if you are the character Peter Griffin from the TV show "Family Guy" in less than 2000 characters (try to include a cutaway gag/reference from the show in your response): ' + input,
                                safety_settings={'HARM_CATEGORY_HARASSMENT': 'block_none', 'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                                                 'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                                                 'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})

                peterResponse = response.text
                if len(peterResponse) < 2000:
                    break
            return peterResponse
        except Exception as e:
            print(e)
            return "An error occured"
    elif type == 'askpeter2':
        try:
            while True:
                response = model2.generate_content([
                                                       'React to the following image and statement as if you are the character Peter Griffin from the TV show "Family Guy" in less than 2000 characters (try to include a cutaway gag/reference from the show in your response): ' + input,
                                                       image], safety_settings={'HARM_CATEGORY_HARASSMENT': 'block_none',
                                                                                'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                                                                                'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                                                                                'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'})

                peterResponse = response.text
                if len(peterResponse) < 2000:
                    break
            return peterResponse
        except Exception as e:
            print(e)
            return "An error occured"

    elif type == 'help':
        return '**Commands:**\n\n**?askpeter {Your question/statement}:** Responds as Peter Griffin from Family Guy'

