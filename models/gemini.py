import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("AIzaSyDC_8wHDJlUqis0Z2FdwLwZILUqVKLMSb4"),
    )

    article = "Israel’s military has backtracked on its account of the killing of 15 Palestinian medics in Gaza last month after footage contradicted its claims that their vehicles did not have emergency signals on when Israeli troops opened fire. The military said initially it opened fire because the vehicles were advancing suspiciously on nearby troops without headlights or emergency signals. An Israeli military official, speaking on condition of anonymity in line with regulations late on Saturday, said that account was mistaken.The almost seven-minute video, which the Palestine Red Crescent Society (PRCS) said on Saturday was recovered from the phone of Rifat Radwan, one of the men killed, appears to have been filmed from inside a moving vehicle. It shows a red fire engine and clearly marked ambulances driving at night, using headlights and flashing emergency lights. The vehicle stops beside another that has driven off the road. Two men get out to examine the stopped vehicle, then gunfire erupts before the screen goes black.Fifteen Palestinian paramedics and rescue workers, including at least one UN employee, were killed in the incident in Rafah on 23 March, in which the UN said Israeli forces shot the men one by one and then buried them in a mass grave.The Israel Defense Forces (IDF) said the incident was still under investigation. It added: All claims, including the documentation circulated about the incident, will be thoroughly and deeply examined to understand the sequence of events and the handling of the situation.The official said the initial report received from the field did not describe lights but that investigators were looking at operational information and were trying to understand whether this was due to an error by the person making the initial report.What we understand currently is the person who gives the initial account is mistaken. We’re trying to understand why, the official added. According to the UN Office for the Coordination of Humanitarian Affairs (Ocha), the PRCS and civil defence workers were on a mission to rescue colleagues who had been shot at earlier in the day, when their clearly marked vehicles came under heavy Israeli fire in the Tel al-Sultan area of Rafah. A Red Crescent official in Gaza said there was evidence of at least one person being detained and killed, as the body of one of the dead had been found with his hands tied."

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=article),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""find severity score for given news articles. the severity score should depend on topics like military, political instability, government policies, environmental disasters, conflicts etc. The score should be between 0(least severe) and 1(most severe). Give only the score nothing else."""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
