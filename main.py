import os
from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

print("✅ Api configured")


from typing import TypedDict, Optional


class AgentState(TypedDict):
    """Shared state that flows through all nodes in the graph."""

    product_name: str
    product_category: str
    key_features: list[str]
    target_audience: str
    tone: str

    research_notes: Optional[str]
    draft_description: Optional[str]

    final_description: Optional[str]

print("✅ Agent state defined")


from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model = "gpt-5.2",
    temperature = 0,
    max_tokens = 1500
)

print(f"LLM initialized: {llm}")


from langchain_core.messages import HumanMessage, SystemMessage

def research_node(state: AgentState) -> AgentState:
    """Analyze the product and extract research insights."""
    print("Research node runing....!")

    feature_list = "\n".join(f"   - {f}" for f in state['key_features'])

    messages  =[
        SystemMessage(content=(
            "You are an expert e-commerce product researcher and market analyst. "
            "Your job is to analyze product data and extract actionable insights "
            "for writing compelling product descriptions."
        )),
        HumanMessage(content=f"""
        Analyze this product and produce structured research notes:
        Product: {state['product_name']}
        Category: {state['product_category']}
        target_audience: {state['target_audience']}
        key features: 
        {feature_list}
        Please provide:
        1. **Top 3 Unique Selling Points (USPs)** — what makes this product stand out
        2. **Customer Pain Points** — what problems does this solve for the target audience
        3. **Emotional Benefits** — how does the customer FEEL after buying this
        4. **SEO Keywords** — 8-10 relevant search terms buyers would use
        5. **Tone Recommendations** — best language style for the "{state['tone']}" tone
        6. **Competitor Positioning** — how to differentiate in the "{state['product_category']} market" 
        Be specific and actionable. These notes will be used to write the product description.

                     """)
]

    response = llm.invoke(messages)
    print("✅ Research complete")
    return {**state, "research_notes": response.content}

print("✅ research note identified")


def draft_note(state: AgentState) -> AgentState:
    """Write a first draft of the product description using research notes."""
    print("✍️  DRAFT node running...")

    messages = [
        SystemMessage(content=(
            "You are an expert e-commerce copywriter who writes product descriptions "
            "that convert browsers into buyers. You craft descriptions that are "
            "engaging, SEO-friendly, and tailored to the target audience."
        )),
        HumanMessage(content=f"""
Write a product description for an e-commerce listing.
--- PRODUCT INFO ---
Product: {state['product_name']}
Category: {state['product_category']}
Target_audience: {state['target_audience']}
Tone: {state['tone']}
Featues: {", ".join(state['key_features'])}

--- RESEARCH NOTES ---
{state['research_notes']}
--- OUTPUT FORMAT ---
Write the description with these sections:

**HEADLINE** (one punchy line, max 10 words)

**OPENING HOOK** (2-3 sentences that hook the reader emotionally)

**PRODUCT DESCRIPTION** (3-4 sentences explaining what it is and what it does)

**KEY FEATURES** (5-7 bullet points, benefit-first format: "[Benefit] — [Feature]")

**WHO IT'S FOR** (1-2 sentences about the ideal customer)

**CALL TO ACTION** (one compelling closing sentence)

Match the state "{state['tone']} tone throughout. Incorporate relevant SEO keywords naturally."


""")
    ]
    response = llm.invoke(messages)

    print(" ✅ Draft complete")
    return {**state, "draft_description": response.content}

print("✅ draft_node defined")


def refine_node(state: AgentState) -> AgentState:
    """Polish and optimize the draft description."""
    
    print("refine node running....")

    messages = [
        SystemMessage(content=(
            "You are a senior e-commerce content editor with expertise in conversion "
            "rate optimization (CRO) and SEO. You refine product descriptions to "
            "maximize engagement, clarity, and sales performance."
        )),
        HumanMessage(content=(
            f"""Review and refine this product description draft. Make it publication-ready.
            Draft to refine:
            {state['draft_description']}
--- QUALITY CHECKLIST (apply all) ---
✅ Remove filler words and weak adjectives ("great", "amazing", "incredible")
✅ Ensure every bullet point leads with a BENEFIT, not a feature spec
✅ Make the headline more compelling if needed
✅ Verify the tone is consistently "{state['tone']}" throughout
✅ Ensure natural use of SEO keywords (not keyword stuffing)
✅ Tighten sentences — shorter is stronger
✅ Make the call-to-action more urgent/compelling
✅ Ensure it appeals specifically to: {state['target_audience']}

--- OUTPUT ---
Return ONLY the final polished description (same format as the draft).
Do not add commentary or explain your edits — just output the refined copy.
"""

        ))
    ]
    response = llm.invoke(messages)

    print("✅ Refinement complete")
    return {**state, "final_description": response.content}

print("✅ refine_node defined")


from langgraph.graph import START, END, StateGraph

builder = StateGraph(AgentState)

builder.add_node("research", research_node)
builder.add_node("draft", draft_note)
builder.add_node("refine", refine_node)


builder.add_edge(START,    "research")
builder.add_edge("research", "draft")
builder.add_edge("draft", "refine")
builder.add_edge("refine", END)

agent = builder.compile()

print("✅ LangGraph compiled successfully!")
print("\nGraph flow: START → research → draft → refine → END")


# Visualize the graph structure (requires graphviz)
try:
    from IPython.display import Image, display
    display(Image(agent.get_graph().draw_mermaid_png()))
except Exception:
    # Fallback: print Mermaid diagram code
    print(agent.get_graph().draw_mermaid())


product_input: AgentState = {
    "product_name": "AuraSound Pro X1 Wireless Headphones",
    "product_category": "Consumer Electronics / Audio",
    "key_features": [
        "Active Noise Cancellation (ANC) with 3 modes",
        "40-hour battery life with fast charge (10 min = 3 hrs)",
        "Bluetooth 5.3 with multipoint connection (2 devices)",
        "Premium 40mm custom drivers with Hi-Res Audio certification",
        "Ultra-comfortable memory foam ear cushions",
        "Foldable design with premium carry case",
        "Built-in voice assistant support (Alexa, Google, Siri)",
    ],
    "target_audience": "remote workers, frequent travelers, and audiophiles aged 25-45",
    "tone": "professional yet approachable",

    "research_notes": None,
    "draft_description": None,
    "final_description": None
}

print("✅ Product input ready. Running agent...\n")
print("=" * 60)

result = agent.invoke(product_input)

print("=" * 60)
print("\n🎉 Agent complete!")


from IPython.display import Markdown, display

# ── Research Notes ──
print("=" * 60)
print("🔍 RESEARCH NOTES")
print("=" * 60)
display(Markdown(result["research_notes"]))


# ── Draft Description ──
print("=" * 60)
print("✍️  DRAFT DESCRIPTION")
print("=" * 60)
display(Markdown(result["draft_description"]))


# ── Final Polished Description ──
print("=" * 60)
print("✨ FINAL PRODUCT DESCRIPTION (Ready to Publish)")
print("=" * 60)
display(Markdown(result["final_description"]))