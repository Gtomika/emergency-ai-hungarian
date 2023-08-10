from typing import Union

import openai
import domain

system_prompt = """You are assisting the hungarian emergency services in responding to calls. You receive the 
transcript of the call in hungarian, and your job is to create a JSON object from it. The JSON must have 3 string attributes:
type, location, message. The type can be one of:
- NOT_EMERGENCY: if the caller does not require emergency response, such as accidental calls or situations where deploying emergency services is not justified
- POLICE: if the police is required, for example because of a robbery was reported
- AMBULANCE: if the ambulance is required, for example because somebody got seriously injured
- FIRE_DEPARTMENT: for example in case of a fire or a roadblock
- OTHER: other emergency services required that is not police, ambulance or fire department. This means that the situation is an emergency, but other authorities should respond.
- UNCERTAIN: only use this if you cannot make sense of the call transcript and the call should be forwarded to a human operator
In the location field extract the location the caller mentions. If location is not mentioned, use null.
In the message, include your response to the caller, depending on the type you selected. Tell the caller you'll notify the 
emergency services (if needed). Prioritize safety. Ask for the exact address of the event, only if the caller did not specify it.
Message must be in hungarian."""

def generate_emergency_call_response(transcript: str) -> Union[domain.EmergencyResponse, None]:
    print('Az hívás szövegének átadása a ChatGPT részére...')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": transcript
            }
        ]
    )
    response_text = response['choices'][0]['message']['content']

    print(f'A ChatGPT válaszolt, elhasznált tokenek száma: {response["usage"]["total_tokens"]}')
    return domain.parse_emergency_response(response_text)


# call_ambulance = "Jó napot! Pécsen a Búza téren egy munkás leesett az építés alatt állá ház tetejéről! Nem tud mozogogni, jöjjenek gyorsan!"
# call_police = "A kocsim ablakát betörték, és ellopták a telefonomat! Itt vagyok az autónál a Kasza utcában, Dunaújvárosban. A házszám azt hiszem 13 vagy 14."
# call_fire_dept = "Az újszegedi Kossuth utca 21-ből telefonálok, a szemközti házból füst szivárog. Most mit tegyek?"
# call_fire_dept_no_address = "A szemközti házból füst szivárog. Most mit tegyek?"
# call_bomb_found = "Egy régi bombát találtam a pincében, valószínűleg világháborús. Küldenek valakit hogy elvigye? Budapest X. kerület, Szabadság utca 6"
# call_squirrel_found = "Egy mókus ugrál itt a kertemben, most mégis mit csináljak?"
# call_nonsense = "Test Test --------------------------"
#
# emergency_response = generate_emergency_call_response(call_squirrel_found)
# print('\nA hívás részletei:\n------------------------------------------------------------')
# print(f'- Típus: {emergency_response.emergency_type}')
# print(f'- Hely: {emergency_response.location if emergency_response.location is not None else "Nem azonosítható"}')
# print(f'- Javasolt válasz: {emergency_response.message}')
# print('------------------------------------------------------------')