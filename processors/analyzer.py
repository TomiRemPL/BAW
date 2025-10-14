"""AI-powered document analysis module."""
import logging
import json
from typing import List, Dict, Optional, Any
from enum import Enum

from pydantic import BaseModel
import anthropic

from config import Config
from .comparator import DiffResult, ModifiedParagraph


logger = logging.getLogger(__name__)


class Severity(str, Enum):
    """Change severity levels."""
    MINOR = "MINOR"
    MODERATE = "MODERATE"
    MAJOR = "MAJOR"


class ImpactLevel(str, Enum):
    """Compliance impact levels."""
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ChangeAnalysis(BaseModel):
    """Analysis of a single change."""
    severity: Severity
    summary: str
    reasoning: str
    old_text: str
    new_text: str


class ComplianceImpact(BaseModel):
    """Impact on a specific regulation."""
    regulation: str
    impact_level: ImpactLevel
    potential_issues: List[str]
    recommendations: List[str]


class ComplianceReport(BaseModel):
    """Complete compliance analysis report."""
    overall_risk: ImpactLevel
    impacts: List[ComplianceImpact]
    summary: str


class AIAnalysisResult(BaseModel):
    """Complete AI analysis result."""
    mode: str  # "basic" or "advanced"
    change_analyses: List[ChangeAnalysis]
    overall_summary: str
    compliance_report: Optional[ComplianceReport] = None
    ai_available: bool = True


class AIAnalyzer:
    """Analyzes document changes using AI."""

    def __init__(self):
        """Initialize the AIAnalyzer."""
        self.anthropic_client = None
        self.google_client = None

        # Initialize Anthropic client
        if Config.ANTHROPIC_API_KEY:
            try:
                self.anthropic_client = anthropic.Anthropic(
                    api_key=Config.ANTHROPIC_API_KEY
                )
                logger.info("Anthropic client initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic client: {e}")

        # Initialize Google client as fallback
        if Config.GOOGLE_API_KEY and not self.anthropic_client:
            try:
                import google.generativeai as genai
                genai.configure(api_key=Config.GOOGLE_API_KEY)
                self.google_client = genai.GenerativeModel('gemini-pro')
                logger.info("Google Gemini client initialized as fallback")
            except Exception as e:
                logger.warning(f"Failed to initialize Google client: {e}")

    def analyze_basic(self, diff_result: DiffResult) -> AIAnalysisResult:
        """
        Perform basic AI analysis of document changes.

        Args:
            diff_result: Result from DocumentComparator

        Returns:
            AIAnalysisResult with basic analysis
        """
        logger.info("Starting basic AI analysis")

        if not self.anthropic_client and not self.google_client:
            logger.warning("No AI client available, returning placeholder analysis")
            return AIAnalysisResult(
                mode="basic",
                change_analyses=[],
                overall_summary="Analiza AI niedostępna - brak klucza API",
                ai_available=False
            )

        change_analyses = []

        # Analyze modified paragraphs
        for mod_para in diff_result.modified_paragraphs[:10]:  # Limit to first 10 for POC
            try:
                analysis = self._analyze_change(
                    mod_para.old_text,
                    mod_para.new_text
                )
                change_analyses.append(analysis)
            except Exception as e:
                logger.error(f"Error analyzing change: {e}")

        # Analyze added paragraphs
        for idx, text in diff_result.added_paragraphs[:5]:
            try:
                analysis = self._analyze_change(
                    "",
                    text
                )
                change_analyses.append(analysis)
            except Exception as e:
                logger.error(f"Error analyzing addition: {e}")

        # Analyze removed paragraphs
        for idx, text in diff_result.removed_paragraphs[:5]:
            try:
                analysis = self._analyze_change(
                    text,
                    ""
                )
                change_analyses.append(analysis)
            except Exception as e:
                logger.error(f"Error analyzing removal: {e}")

        # Generate overall summary
        overall_summary = self._generate_overall_summary(change_analyses)

        logger.info(f"Basic analysis complete: {len(change_analyses)} changes analyzed")

        return AIAnalysisResult(
            mode="basic",
            change_analyses=change_analyses,
            overall_summary=overall_summary,
            ai_available=True
        )

    def analyze_advanced(self, diff_result: DiffResult) -> AIAnalysisResult:
        """
        Perform advanced AI analysis including compliance checks.

        Args:
            diff_result: Result from DocumentComparator

        Returns:
            AIAnalysisResult with advanced analysis
        """
        logger.info("Starting advanced AI analysis")

        # First do basic analysis
        basic_result = self.analyze_basic(diff_result)

        if not basic_result.ai_available:
            return basic_result

        # Add compliance analysis
        compliance_report = self._analyze_compliance(basic_result.change_analyses)

        logger.info("Advanced analysis complete")

        return AIAnalysisResult(
            mode="advanced",
            change_analyses=basic_result.change_analyses,
            overall_summary=basic_result.overall_summary,
            compliance_report=compliance_report,
            ai_available=True
        )

    def _analyze_change(self, old_text: str, new_text: str) -> ChangeAnalysis:
        """
        Analyze a single change using AI.

        Args:
            old_text: Original text
            new_text: Modified text

        Returns:
            ChangeAnalysis with severity and reasoning
        """
        prompt = f"""Przeanalizuj następującą zmianę w dokumencie bankowym.

Stara wersja: {old_text if old_text else "[BRAK - nowy tekst]"}

Nowa wersja: {new_text if new_text else "[BRAK - tekst usunięty]"}

Klasyfikuj jako:
- MINOR: kosmetyczne zmiany (literówki, formatowanie)
- MODERATE: istotne ale nie krytyczne (doprecyzowania, drobne zmiany treści)
- MAJOR: wymaga przeglądu prawnego (zmiany w warunkach, obowiązkach, regulacjach)

Zwróć odpowiedź TYLKO w formacie JSON:
{{
  "severity": "MINOR|MODERATE|MAJOR",
  "summary": "krótkie podsumowanie zmiany (1-2 zdania)",
  "reasoning": "uzasadnienie klasyfikacji"
}}"""

        try:
            response_text = self._call_llm(prompt)

            # Parse JSON response
            # Clean response if it contains markdown code blocks
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            result = json.loads(response_text)

            return ChangeAnalysis(
                severity=Severity[result["severity"]],
                summary=result["summary"],
                reasoning=result["reasoning"],
                old_text=old_text[:200],  # Truncate for storage
                new_text=new_text[:200]
            )

        except Exception as e:
            logger.error(f"Error parsing AI response: {e}")
            # Fallback
            return ChangeAnalysis(
                severity=Severity.MODERATE,
                summary="Zmiana wymagająca przeglądu",
                reasoning="Automatyczna analiza niedostępna",
                old_text=old_text[:200],
                new_text=new_text[:200]
            )

    def _analyze_compliance(self, changes: List[ChangeAnalysis]) -> ComplianceReport:
        """
        Analyze compliance impact of changes.

        Args:
            changes: List of analyzed changes

        Returns:
            ComplianceReport with regulatory impact
        """
        # Create summary of changes for compliance analysis
        changes_summary = "\n".join([
            f"- {c.severity.value}: {c.summary}"
            for c in changes[:20]  # Limit to avoid token limits
        ])

        prompt = f"""Oceń wpływ następujących zmian w dokumencie bankowym na zgodność z regulacjami.

Zmiany:
{changes_summary}

Oceń wpływ na następujące regulacje:
1. DORA (Digital Operational Resilience Act) - odporność operacyjna
2. KYC (Know Your Customer) - weryfikacja klienta
3. AML (Anti Money Laundering) - przeciwdziałanie praniu pieniędzy

Dla każdej regulacji zwróć JSON:
{{
  "impacts": [
    {{
      "regulation": "DORA|KYC|AML",
      "impact_level": "NONE|LOW|MEDIUM|HIGH",
      "potential_issues": ["lista potencjalnych problemów"],
      "recommendations": ["lista rekomendacji"]
    }}
  ],
  "overall_risk": "NONE|LOW|MEDIUM|HIGH",
  "summary": "ogólne podsumowanie wpływu na compliance"
}}"""

        try:
            response_text = self._call_llm(prompt)

            # Clean response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            result = json.loads(response_text)

            impacts = [
                ComplianceImpact(
                    regulation=imp["regulation"],
                    impact_level=ImpactLevel[imp["impact_level"]],
                    potential_issues=imp["potential_issues"],
                    recommendations=imp["recommendations"]
                )
                for imp in result["impacts"]
            ]

            return ComplianceReport(
                overall_risk=ImpactLevel[result["overall_risk"]],
                impacts=impacts,
                summary=result["summary"]
            )

        except Exception as e:
            logger.error(f"Error analyzing compliance: {e}")
            # Fallback
            return ComplianceReport(
                overall_risk=ImpactLevel.LOW,
                impacts=[],
                summary="Automatyczna analiza compliance niedostępna"
            )

    def _generate_overall_summary(self, changes: List[ChangeAnalysis]) -> str:
        """
        Generate overall summary of all changes.

        Args:
            changes: List of analyzed changes

        Returns:
            Summary text
        """
        if not changes:
            return "Nie znaleziono zmian do analizy."

        # Count by severity
        severity_counts = {
            Severity.MINOR: 0,
            Severity.MODERATE: 0,
            Severity.MAJOR: 0
        }

        for change in changes:
            severity_counts[change.severity] += 1

        summary_parts = [
            f"Znaleziono {len(changes)} zmian do przeglądu:",
            f"- {severity_counts[Severity.MAJOR]} zmian MAJOR (wymagają przeglądu prawnego)",
            f"- {severity_counts[Severity.MODERATE]} zmian MODERATE (istotne zmiany)",
            f"- {severity_counts[Severity.MINOR]} zmian MINOR (kosmetyczne)"
        ]

        # Get summaries of major changes
        major_changes = [c for c in changes if c.severity == Severity.MAJOR]
        if major_changes:
            summary_parts.append("\nNajważniejsze zmiany:")
            for i, change in enumerate(major_changes[:3], 1):
                summary_parts.append(f"{i}. {change.summary}")

        return "\n".join(summary_parts)

    def _call_llm(self, prompt: str) -> str:
        """
        Call LLM with retry logic.

        Args:
            prompt: Prompt text

        Returns:
            Response text
        """
        for attempt in range(Config.MAX_RETRIES):
            try:
                if self.anthropic_client:
                    return self._call_anthropic(prompt)
                elif self.google_client:
                    return self._call_google(prompt)
                else:
                    raise ValueError("No AI client available")
            except Exception as e:
                logger.warning(f"LLM call attempt {attempt + 1} failed: {e}")
                if attempt == Config.MAX_RETRIES - 1:
                    raise

        raise ValueError("All LLM call attempts failed")

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API."""
        message = self.anthropic_client.messages.create(
            model=Config.CLAUDE_MODEL,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def _call_google(self, prompt: str) -> str:
        """Call Google Gemini API."""
        response = self.google_client.generate_content(prompt)
        return response.text
