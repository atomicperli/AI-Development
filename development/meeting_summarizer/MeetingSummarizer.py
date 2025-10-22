import os
from openai import OpenAI
import json
import re

class MeetingSummarizer:
    def __init__(self, model: str = 'gpt-4o', user_prompt_summary: str = "", user_prompt_actions: str = ""):
        self.model = model
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.user_prompt_summary = user_prompt_summary or ("You are an AI assistant summarizing meeting transcripts. Provide a clear and concise summary of the following conversation, avoiding interpretation and unnecessary details. Focus on the main discussion points only. Do not include any action items. Respond with only the summary as plain text — no headings, formatting, or explanations.")
        self.user_prompt_actions = user_prompt_actions or ( "Extract all action items from the following meeting transcript. Identify individual and team-wide action items in the following format: {'individual_actions': {'Alice': ['Task 1', 'Task 2'],'Bob': ['Task 1'] }, 'team_actions': ['Task 1', 'Task 2'], 'entities': ['Alice', 'Bob']} Only include what is explicitly mentioned. Do not infer. You must respond strictly in valid JSON format — no extra text or commentary. ")

    def summarize(self, transcript: str):
        summary = self.summary(transcript)
        action_items = self.action_items(transcript)
        return summary, action_items
    
    def summary(self, transcript: str):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.user_prompt_summary},
                {"role": "user", "content": transcript},
            ],
        )
        return response.choices[0].message.content.strip()
    
    def action_items(self, transcript: str):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.user_prompt_actions},
                    {"role": "user", "content": transcript},
                ],
            )
            action_items =  response.choices[0].message.content.strip()
            clean_output = re.sub(r"^```json|```$", "", action_items, flags=re.MULTILINE).strip()
            #print(action_items)
            try:
                return json.loads(clean_output)
            except json.JSONDecodeError:
                return {"error": "Invalid JSON returned from model", "raw_output": action_items}
        except Exception as e:
            print(f"Error generating action items: {e}")
            return {"error": f"API call failed: {e}", "raw_output": ""}
