import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from lib.db import engine
from models.autocomplete import Autocomplete, Base

LENGTHY_WORDS = [
    "appreciation", "beneficial", "collaborate", "determination", "excellence",
    "flexibility", "generosity", "humanitarian", "innovation", "justification",
    "knowledge", "leadership", "motivation", "negotiation", "opportunity",
    "productivity", "questionnaire", "responsibility", "sustainability", "transparency",
    "understanding", "versatility", "workforce", "xenophobia", "youthfulness",
    "zealousness", "accountability", "breakthrough", "complexity", "development",
    "empowerment", "functionality", "globalization", "hospitality", "integration",
    "journeying", "kindness", "longevity", "methodology", "nationalism",
    "organization", "performance", "qualification", "reliability", "significance",
    "transformation", "utilization", "validation", "wellness", "xeniality",
    "yearning", "zestfulness", "adaptability", "brilliance", "creativity",
    "distinction", "enthusiasm", "foundation", "governance", "humility",
    "inspiration", "joviality", "keenness", "luminosity", "mentorship",
    "nourishment", "optimism", "perseverance", "quintessential", "resilience",
    "simplicity", "tenacity", "uniqueness", "vibrancy", "wisdom",
    "xenodochial", "youthful", "zealotry", "abundance", "benevolence",
    "consistency", "diligence", "eloquence", "frequency", "gratitude",
    "harmony", "integrity", "justice", "knowledgeably", "legitimacy",
    "mindfulness", "novelty", "openness", "pragmatism", "quantitative",
    "rationality", "serenity", "tranquility", "unity", "valor",
    "willingness", "xylophone", "yearnings", "zookeeper", "aggregation",
    "benchmarking", "customization", "differentiation", "evaluation",
    "forecasting", "gratification", "headquarters", "identification", "juxtaposition",
    "kinship", "legislation", "modernization", "normalization", "optimization",
    "prioritization", "questioning", "revitalization", "standardization", "troubleshooting",
    "universalism", "virtualization", "wonderment", "xenophobic", "yielding",
    "zealously", "accreditation", "bioavailability", "conceptualization", "decentralization",
    "entrepreneurship", "fragmentation", "generalization", "hybridization", "implementation",
    "journalistic", "kindheartedness", "localization", "materialization", "naturalization",
    "overwhelming", "polarization", "quadrilateral", "representation", "simplification",
    "territoriality", "unfamiliarity", "visualization", "willpower", "xerography",
    "yesteryear", "zeitgeist", "accumulation", "biotechnology", "commercialization",
    "deliberation", "electrification", "fertilization", "gastrointestinal", "galvanization",
    "historiography", "intensification", "jurisprudence", "kleptocracy", "legitimization",
    "militarization", "nationalization", "operationalization", "personalization", "quantification",
    "rationalization", "securitization", "territorialization", "urbanization", "verbalization",
    "westernization", "xenotransplant", "youngster", "zombification", "amelioration",
    "bifurcation", "circumnavigation", "disambiguation", "encapsulation", "formalization",
    "gesticulation", "homogenization", "ideation", "judgmental", "kindergarten",
    "liberalization", "mobilization", "neutralization", "oscillation", "photolithography",
    "quarantine"
]

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as session:
        await session.execute(text('DELETE FROM autocomplete'))
        await session.commit()

        for word in LENGTHY_WORDS:
            session.add(Autocomplete(text=word))
        await session.commit()

print(__name__, "__name__")
if __name__ == "__main__":
    asyncio.run(main())
