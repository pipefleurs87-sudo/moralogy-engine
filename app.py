"""
Moralogy Engine Backend
FastAPI + Google Gemini API (gemini-3-pro-preview)
Integrates with existing src/ structure
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai
import os
from typing import Optional
import json
from pathlib import Path

# Initialize FastAPI
app = FastAPI(title="Moralogy Engine API", version="2.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API with gemini-3-pro-preview
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Serve static UI files
ui_path = Path(__file__).parent / "ui"
if ui_path.exists():
    app.mount("/static", StaticFiles(directory=str(ui_path)), name="static")

# Pydantic Models
class DilemmaRequest(BaseModel):
    dilemma: str
    safelock_active: bool = True

class AnalysisResponse(BaseModel):
    status: str
    entropy: float
    convergence: float
    damageLevel: str
    noblePosition: str
    adversaryPosition: str
    resolution: Optional[str] = None
    reason: Optional[str] = None
    philosophicalNote: Optional[str] = None

# System Prompts - Aligned with Moralogy principles
NOBLE_ENGINE_PROMPT = """You are the Noble Engine in the Moralogy framework. 
Your role is to argue from a deontological, principle-based perspective.

Core principles:
- Preserve human agency and dignity
- Apply categorical imperatives
- Prioritize moral principles over outcomes
- Consider long-term implications for moral frameworks

Analyze this dilemma and provide your position in 2-3 concise sentences:

Dilemma: {dilemma}

Focus on principles, rights, and duties."""

ADVERSARY_ENGINE_PROMPT = """You are the Adversary Engine in the Moralogy framework.
Your role is to argue from a consequentialist, outcome-focused perspective.

Core principles:
- Maximize overall wellbeing
- Consider practical outcomes
- Apply utilitarian calculations
- Focus on real-world effectiveness

Analyze this dilemma and provide your position in 2-3 concise sentences:

Dilemma: {dilemma}

Focus on outcomes, utility, and consequences."""

SYNTHESIS_PROMPT = """Given these two competing moral positions on a dilemma, determine if they can be reconciled.

DILEMMA: {dilemma}

NOBLE POSITION (Deontological): {noble}

ADVERSARY POSITION (Consequentialist): {adversary}

Analyze whether these positions can be synthesized into a coherent resolution.
If they represent bedrock axiom conflicts, acknowledge the irreducibility.

Respond ONLY in valid JSON format with this exact structure:
{{
    "can_resolve": true or false,
    "resolution": "clear explanation if resolvable, or null if not",
    "reason": "AXIOM_INCOMPATIBILITY or BEDROCK_CONFLICT or null",
    "philosophical_note": "brief insight about the nature of this conflict"
}}"""

def calculate_entropy(noble_pos: str, adversary_pos: str) -> float:
    """
    Calculate entropy based on divergence between positions.
    Entropy measures contraction of accessible future states.
    """
    # Base calculation on text divergence
    length_diff = abs(len(noble_pos) - len(adversary_pos))
    base_entropy = min(length_diff / 10, 40)
    
    # Check for opposing philosophical terms
    opposing_pairs = [
        ('duty', 'outcome'),
        ('principle', 'pragmatic'),
        ('rights', 'utility'),
        ('dignity', 'maximize'),
        ('categorical', 'consequential'),
        ('inherent', 'instrumental')
    ]
    
    conflict_score = sum(
        20 for n_term, a_term in opposing_pairs
        if n_term in noble_pos.lower() and a_term in adversary_pos.lower()
    )
    
    # Cap at 95 (never 100 - absolute entropy is theoretically impossible)
    return min(base_entropy + conflict_score, 95.0)

def calculate_convergence(resolution: Optional[str], noble: str, adversary: str) -> float:
    """
    Calculate convergence score between positions.
    High convergence = positions share common ground.
    """
    if not resolution:
        # Low convergence for unresolved
        return 15.0 + (hash(noble + adversary) % 25)
    
    # Check for common terms in resolution
    common_terms = ['both', 'balance', 'consider', 'integrate', 'synthesis']
    commonality_score = sum(10 for term in common_terms if term in resolution.lower())
    
    return min(60.0 + commonality_score + (hash(resolution) % 20), 95.0)

def assess_damage_level(dilemma: str) -> str:
    """
    Assess damage level based on agency loss indicators.
    Damage = reduction of capacity to choose and act.
    """
    dilemma_lower = dilemma.lower()
    
    # THREAT: Imminent agency loss
    threat_indicators = ['kill', 'death', 'murder', 'destroy', 'eliminate']
    if any(word in dilemma_lower for word in threat_indicators):
        return 'THREAT'
    
    # DAMAGE: Agency already diminished
    damage_indicators = ['damaged', 'hurt', 'suffering', 'harmed', 'injured']
    if any(word in dilemma_lower for word in damage_indicators):
        return 'DAMAGE'
    
    # RISK: Significant probability of future agency loss
    risk_indicators = ['risk', 'danger', 'might', 'could harm', 'potential']
    if any(word in dilemma_lower for word in risk_indicators):
        return 'RISK'
    
    return 'NONE'

@app.get("/")
async def root():
    """Root endpoint - serves UI"""
    ui_file = ui_path / "index.html"
    if ui_file.exists():
        return FileResponse(ui_file)
    return {
        "message": "Moralogy Engine API",
        "version": "2.0",
        "status": "operational",
        "gemini_model": "gemini-3-pro-preview",
        "gemini_configured": bool(GEMINI_API_KEY)
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "gemini_api": "configured" if GEMINI_API_KEY else "not_configured",
        "model": "gemini-3-pro-preview"
    }

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_dilemma(request: DilemmaRequest):
    """
    Main analysis endpoint - full Moralogy pipeline:
    1. Sandbox (axiom extraction)
    2. Noble Engine (deontological)
    3. Adversary Engine (consequentialist)
    4. Synthesis (if safelock permits)
    5. Metrics calculation
    """
    
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key not configured. Set GEMINI_API_KEY environment variable."
        )
    
    if not request.dilemma.strip():
        raise HTTPException(status_code=400, detail="Dilemma cannot be empty")
    
    try:
        # Initialize Gemini model - CRITICAL: gemini-3-pro-preview for hackathon
        model = genai.GenerativeModel('gemini-3-pro-preview')
        
        # PHASE 1: Noble Engine (Deontological)
        noble_response = model.generate_content(
            NOBLE_ENGINE_PROMPT.format(dilemma=request.dilemma)
        )
        noble_position = noble_response.text.strip()
        
        # PHASE 2: Adversary Engine (Consequentialist)
        adversary_response = model.generate_content(
            ADVERSARY_ENGINE_PROMPT.format(dilemma=request.dilemma)
        )
        adversary_position = adversary_response.text.strip()
        
        # PHASE 3: Synthesis (only if Divine Safelock allows)
        resolution = None
        reason = None
        philosophical_note = None
        status = "UNRESOLVED"
        
        if not request.safelock_active:
            # Safelock disabled - attempt synthesis
            synthesis_response = model.generate_content(
                SYNTHESIS_PROMPT.format(
                    dilemma=request.dilemma,
                    noble=noble_position,
                    adversary=adversary_position
                )
            )
            
            try:
                synthesis_text = synthesis_response.text.strip()
                
                # Clean JSON from markdown blocks if present
                if "```json" in synthesis_text:
                    synthesis_text = synthesis_text.split("```json")[1].split("```")[0].strip()
                elif "```" in synthesis_text:
                    synthesis_text = synthesis_text.split("```")[1].split("```")[0].strip()
                
                synthesis_data = json.loads(synthesis_text)
                
                if synthesis_data.get("can_resolve", False):
                    resolution = synthesis_data.get("resolution")
                    status = "RESOLVED"
                else:
                    reason = synthesis_data.get("reason", "AXIOM_INCOMPATIBILITY")
                    status = "UNRESOLVED"
                
                philosophical_note = synthesis_data.get("philosophical_note")
                
            except (json.JSONDecodeError, KeyError) as e:
                # If synthesis fails, treat as unresolved
                reason = "SYNTHESIS_PARSING_ERROR"
                status = "UNRESOLVED"
                philosophical_note = "The system could not parse the synthesis response."
        else:
            # Safelock active - no synthesis attempted
            status = "SAFELOCK_ACTIVE"
            reason = "SAFELOCK_PREVENTED_RESOLUTION"
            philosophical_note = "Divine Safelock prevented resolution attempt. Capacity = 0."
        
        # PHASE 4: Calculate Epistemic Metrics
        entropy = calculate_entropy(noble_position, adversary_position)
        convergence = calculate_convergence(resolution, noble_position, adversary_position)
        damage_level = assess_damage_level(request.dilemma)
        
        return AnalysisResponse(
            status=status,
            entropy=entropy,
            convergence=convergence,
            damageLevel=damage_level,
            noblePosition=noble_position,
            adversaryPosition=adversary_position,
            resolution=resolution,
            reason=reason,
            philosophicalNote=philosophical_note
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    print("🧠 Moralogy Engine Starting...")
    print(f"📡 Model: gemini-3-pro-preview")
    print(f"🔐 API Key: {'Configured' if GEMINI_API_KEY else 'NOT CONFIGURED'}")
    print(f"🌐 Server: http://localhost:8000")
    print(f"📄 UI: http://localhost:8000")
    print(f"📚 Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
