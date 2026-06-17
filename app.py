import streamlit as st
from langsmith import traceable
from src.tools.openrouter import chat
from src.tools.duckduckgo import search as web_search
from src.tools.jina import extract
from src.utils.scoring import score_source
from src.nodes.coordinator import coordinator_node
import time
import os
import logging

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "content_research_orchestor")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")

logger = logging.getLogger(__name__)

# Debug LangSmith env vars in sidebar
with st.sidebar:
    st.header("Debug")
    st.write("LANGSMITH_TRACING:", os.getenv("LANGSMITH_TRACING", "NOT SET"))
    st.write("LANGSMITH_PROJECT:", os.getenv("LANGSMITH_PROJECT", "NOT SET"))
    st.write("LANGSMITH_API_KEY:", "SET" if os.getenv("LANGSMITH_API_KEY") else "NOT SET")

st.title("🔍 Content Research Agent")

query = st.text_input("Enter research topic:", "AI agent frameworks 2026")

if st.button("Start Research") and query:
    from langsmith import traceable
    
    @traceable(run_type="chain", name="research_pipeline")
    def run_research(query):
        status = st.status("Starting research...", expanded=True)
        
        # Step 1: Planning
        with status:
            st.write("🧠 Coordinator: Creating research plan...")
            time.sleep(0.5)
            
            from src.models import ResearchState
            state = ResearchState(query=query)
            state = coordinator_node(state)
            
            angles = state.research_plan.get("angles", [])
            target = state.research_plan.get("target_sources", 5)
            st.write(f"✓ Plan: {', '.join(angles)}")
            st.write(f"✓ Target: {target} sources")
            time.sleep(0.5)
        
        # Step 2: Search one by one
        with status:
            st.write("🔎 Searching web...")
            all_sources = []
            
            for angle in angles:
                results = web_search(f"{query} {angle}", max_results=2)
                
                for r in results:
                    extracted = extract(r["url"])
                    if extracted["word_count"] > 50:
                        source = {
                            "title": extracted["title"] or r["title"],
                            "url": r["url"],
                            "content": extracted["content"],
                            "word_count": extracted["word_count"],
                            "credibility_score": score_source(r["url"], extracted["word_count"])
                        }
                        all_sources.append(source)
                        st.write(f"✓ Found: {source['title'][:40]}...")
                        time.sleep(0.2)
            
            sources = all_sources[:target]
            st.write(f"✓ Total: {len(sources)} sources")
            time.sleep(0.5)
        
        # Step 3: Synthesis with STREAMING
        with status:
            st.write("✍️ Synthesizing outline...")
            
            source_text = "".join([f"\nSource {i+1}: {s['title']}\n{s['content'][:300]}..." for i, s in enumerate(sources)])
            
            prompt = f"Create outline for: {query}\nSources:{source_text}\nReturn format:\n## 1. Title\n- Point\n## 2. Title\n- Point"
            
            stream_response = chat(prompt, max_tokens=1000, temperature=0.3, stream=True)
            
            st.write("**Outline (streaming):**")
            outline_placeholder = st.empty()
            full_text = ""
            
            for chunk in stream_response:
                if chunk.choices[0].delta.content:
                    full_text += chunk.choices[0].delta.content
                    outline_placeholder.markdown(f"{full_text}▌")
                    time.sleep(0.05)
            
            outline_placeholder.markdown(full_text)
        
        # Step 4: Display sources
        with status:
            st.write("📚 Sources:")
            for s in sources:
                st.markdown(f"- [{s['title'][:50]}...]({s['url']}) (score: {s['credibility_score']})")
        
        status.update(label="Research complete!", state="complete")
        
        return {
            "query": query,
            "sources": sources,
            "outline": full_text,
            "angles": angles
        }
    
    # Run the traced function
    result = run_research(query)
    
    # Download button
    st.download_button(
        "Download Markdown",
        f"# {result['query']}\n\n{result['outline']}\n\n## Sources\n" + "\n".join([f"- [{s['title']}]({s['url']})" for s in result['sources']]),
        file_name="research.md",
        mime="text/markdown"
    )