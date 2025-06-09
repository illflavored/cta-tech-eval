from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Morgan Sveen - CTA DevOps Tech Evaluation"}

@app.get("/standings")
async def get_standings():
    url = "https://statsapi.mlb.com/api/v1/standings?leagueId=104"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    data = response.json()

    standings = []
    for record in data.get("records", []):
        for team_record in record.get("teamRecords", []):
            team = team_record["team"]["name"]
            wins = team_record["wins"]
            losses = team_record["losses"]
            pct = team_record["winningPercentage"]
            standings.append({
                "team": team,
                "wins": wins,
                "losses": losses,
                "pct": pct
            })

    return {"standings": standings}
