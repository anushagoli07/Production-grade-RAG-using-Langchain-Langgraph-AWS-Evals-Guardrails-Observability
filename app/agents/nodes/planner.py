import logfire
from app.agents.state import AgentState
from app.gateway import get_groq_completion


def planner_node(state: AgentState):
    """
    Classifies the incoming query as either CONVERSATIONAL (small talk,
    greetings, follow-ups answerable from history) or TECHNICAL (requires
    document retrieval). Sets current_query accordingly for routing.
    """
    query = state["current_query"]

    with logfire.span("🧭 Query Planning"):
        logfire.info(f"Classifying query: {query}")

        classification_prompt = f"""
        Classify the following user query as either CONVERSATIONAL or TECHNICAL.

        CONVERSATIONAL: greetings, small talk, thanks, or questions answerable
        purely from prior conversation history without needing new documents.
        TECHNICAL: questions requiring lookup of specific technical/enterprise
        documentation, facts, or details not already in the conversation.

        Respond with exactly one word: CONVERSATIONAL or TECHNICAL.

        USER QUERY: "{query}"
        """

        try:
            response, _ = get_groq_completion(
                messages=[{"role": "user", "content": classification_prompt}],
                temperature=0.0
            )
            label = response.choices[0].message.content.strip().upper()

            if "CONVERSATIONAL" in label:
                logfire.info("Routed as CONVERSATIONAL.")
                return {
                    "current_query": "CONVERSATIONAL",
                    "status": "Classified as conversational.",
                    "plan": state["plan"] + ["Intent: Conversational"]
                }
            else:
                logfire.info("Routed as TECHNICAL.")
                return {
                    "status": "Classified as technical.",
                    "plan": state["plan"] + ["Intent: Technical"]
                }

        except Exception as e:
            logfire.error(f"Planner classification failed: {e}")
            # Fail safe: default to technical retrieval path
            return {
                "status": "Planner error, defaulting to retrieval.",
                "plan": state["plan"] + ["Intent: Default (error fallback)"]
            }