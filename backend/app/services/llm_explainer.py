
from typing import Dict
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def explain_risk(incident_data: Dict) -> Dict:
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        # Fallback to mock explanation
        return {
            "risk": "Cross-platform privilege abuse potential",
            "evidence": "User has high privileges across multiple platforms (AD, AWS, and Okta, which creates a large blast radius if compromised",
            "mitre_mapping": ["T1078 - Valid Accounts", "T1098 - Account Manipulation"],
            "remediation": [
                "Implement just-in-time (JIT) access for AWS AdministratorAccess",
                "Review Okta Admin group membership",
                "Enforce MFA on all admin accounts",
                "Run a full access review within the next 7 days"
            ]
        }
    
    try:
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        You are a security analyst. Analyze the following identity risk incident and provide a structured explanation.
        
        Incident Details:
        {incident_data}
        
        Return your response in the following JSON format:
        {{
            "risk": "Brief description of the risk",
            "evidence": "Supporting evidence from the incident data",
            "mitre_mapping": ["MITRE ATT&CK tactic and technique IDs"],
            "remediation": ["Step-by-step remediation actions"]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        # Fallback to mock explanation
        return {
            "risk": "Cross-platform privilege abuse potential",
            "evidence": "User has high privileges across multiple platforms (AD, AWS, and Okta, which creates a large blast radius if compromised",
            "mitre_mapping": ["T1078 - Valid Accounts", "T1098 - Account Manipulation"],
            "remediation": [
                "Implement just-in-time (JIT) access for AWS AdministratorAccess",
                "Review Okta Admin group membership",
                "Enforce MFA on all admin accounts",
                "Run a full access review within the next 7 days"
            ]
        }

